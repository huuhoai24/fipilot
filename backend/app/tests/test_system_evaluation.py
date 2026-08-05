from __future__ import annotations

import json
import tempfile
import unittest
import wave
from datetime import datetime, timezone
from pathlib import Path

from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from services.system_evaluation.cases import (
    CVEvaluationCase,
    EvaluationDataset,
    EvaluatorEvaluationCase,
    QuestionEvaluationCase,
    STTEvaluationCase,
    TTSEvaluationCase,
    VoiceTurnObservation,
)
from services.system_evaluation.evaluators import (
    AnswerEvaluatorBenchmark,
    CVBenchmark,
    QuestionGeneratorBenchmark,
    STTBenchmark,
    TTSBenchmark,
)
from services.system_evaluation.dataset import load_evaluation_dataset
from services.system_evaluation.metrics import (
    error_counts,
    percentile,
    precision_recall_f1,
    skill_counts,
)
from services.system_evaluation.reporting import write_evaluation_reports
from services.system_evaluation.runner import SystemEvaluationRunner
from services.system_evaluation.schemas import QuestionQualityScore
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewQuestion,
    InterviewRound,
)


PRIVATE_RESUME = "PRIVATE_RESUME_SENTINEL"
PRIVATE_TRANSCRIPT = "PRIVATE_TRANSCRIPT_SENTINEL"
PRIVATE_ANSWER = "PRIVATE_ANSWER_SENTINEL"
PRIVATE_TTS_TEXT = "PRIVATE_TTS_SENTINEL"


class FakeProfileExtractor:
    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        return CandidateProfile(
            name="Candidate",
            skills=["Python", "FastAPI"],
            specialization="Backend",
        )


class FakeSTT(StreamingSTT):
    async def start_session(self) -> None:
        return None

    async def process_audio_chunk(self, audio_bytes: bytes) -> TranscriptEvent | None:
        return None

    async def finish_session(self) -> TranscriptEvent | None:
        return TranscriptEvent(
            type=TranscriptEventType.FINAL,
            text="xin ban",
            language="vi",
            confidence=0.9,
            timestamp=datetime.now(timezone.utc),
        )


class FakeSTTFactory(StreamingSTTFactory):
    def create(self) -> StreamingSTT:
        return FakeSTT()


class FakeTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        yield AudioChunk(bytes=b"\x00\x00" * 1600, sample_rate=16_000)


class FakeQuestionGenerator:
    async def generate_question(self, candidate_profile, interview_round, interview_config):
        return InterviewQuestion(
            question="How did you design the FastAPI service?",
            language="en",
            topic=interview_round.topic,
            difficulty=interview_round.difficulty,
        )


class FakeQuestionJudge:
    async def score_question(
        self,
        candidate_profile,
        interview_round,
        interview_config,
        generated_question,
    ) -> QuestionQualityScore:
        return QuestionQualityScore(
            relevance_score=0.9,
            difficulty_alignment=0.8,
            cv_alignment=0.85,
        )


class FakeAnswerEvaluator:
    def __init__(self) -> None:
        self._scores = iter([7.0, 9.0])

    async def evaluate_answer(self, candidate_profile, interview_question, answer, interview_config):
        score = next(self._scores)
        return AnswerEvaluation(turn_id="turn", overall_score=score)


class SystemEvaluationMetricTests(unittest.TestCase):
    def test_error_and_skill_metrics_are_deterministic(self):
        word_errors, word_count, character_errors, character_count = error_counts(
            "xin chao",
            "xin ban",
        )
        self.assertEqual((word_errors, word_count), (1, 2))
        self.assertGreater(character_errors, 0)
        self.assertGreater(character_count, 0)

        matched, predicted, expected = skill_counts(
            ["Python", "SQL"],
            ["python", "FastAPI"],
        )
        self.assertEqual((matched, predicted, expected), (1, 2, 2))
        self.assertEqual(precision_recall_f1(matched, predicted, expected), (0.5, 0.5, 0.5))
        self.assertEqual(percentile([100.0, 200.0, 300.0], 0.5), 200.0)
        self.assertEqual(percentile([100.0, 200.0, 300.0], 0.95), 290.0)

    def test_manifest_loads_private_text_and_pcm_audio_without_serializing_it(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            (directory / "resume.txt").write_text(PRIVATE_RESUME, encoding="utf-8")
            (directory / "reference.txt").write_text(
                PRIVATE_TRANSCRIPT,
                encoding="utf-8",
            )
            with wave.open(str(directory / "sample.wav"), "wb") as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(16_000)
                audio.writeframes(b"\x00\x00" * 3200)
            manifest_path = directory / "dataset.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "dataset_name": "loader-test",
                        "cv_cases": [
                            {
                                "case_id": "cv",
                                "resume_path": "resume.txt",
                                "expected_skills": ["Python"],
                            }
                        ],
                        "stt_cases": [
                            {
                                "case_id": "stt",
                                "audio_path": "sample.wav",
                                "reference_text_path": "reference.txt",
                                "category": "mixed_technical",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            dataset = load_evaluation_dataset(manifest_path, document_service=None)

        self.assertEqual(dataset.cv_cases[0].resume_text, PRIVATE_RESUME)
        self.assertEqual(dataset.stt_cases[0].reference_text, PRIVATE_TRANSCRIPT)
        self.assertEqual(len(dataset.stt_cases[0].audio_chunks), 2)
        self.assertNotIn(PRIVATE_RESUME, repr(dataset.cv_cases[0]))
        self.assertNotIn(PRIVATE_TRANSCRIPT, repr(dataset.stt_cases[0]))


class SystemEvaluationRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_runner_aggregates_all_sections_and_reports_no_private_content(self):
        profile = CandidateProfile(
            name="Candidate",
            skills=["Python", "FastAPI"],
            projects=[{"name": "API", "description": PRIVATE_RESUME}],
        )
        config = InterviewConfig(
            mode="text",
            language="en",
            experience_level="junior",
        )
        interview_round = InterviewRound(
            round_id="round-1",
            topic="FastAPI",
            difficulty="medium",
        )
        question = InterviewQuestion(
            question="Explain FastAPI dependency injection.",
            language="en",
            topic="FastAPI",
            difficulty="medium",
        )
        dataset = EvaluationDataset(
            name="privacy-safe-test",
            cv_cases=(
                CVEvaluationCase(
                    case_id="cv-1",
                    resume_text=PRIVATE_RESUME,
                    expected_skills=("Python", "SQL"),
                    expected_profile_fields={
                        "name": "Candidate",
                        "specialization": "Backend",
                    },
                ),
            ),
            stt_cases=(
                STTEvaluationCase(
                    case_id="stt-1",
                    audio_chunks=(b"\x00\x00" * 160,),
                    reference_text=f"xin chao {PRIVATE_TRANSCRIPT}",
                    category="vi",
                ),
            ),
            tts_cases=(TTSEvaluationCase(case_id="tts-1", text=PRIVATE_TTS_TEXT),),
            question_cases=(
                QuestionEvaluationCase(
                    case_id="question-1",
                    candidate_profile=profile,
                    interview_round=interview_round,
                    interview_config=config,
                ),
            ),
            evaluator_cases=(
                EvaluatorEvaluationCase(
                    case_id="evaluator-1",
                    candidate_profile=profile,
                    interview_question=question,
                    candidate_answer=PRIVATE_ANSWER,
                    interview_config=config,
                    human_score=8.0,
                ),
            ),
            voice_turns=(
                VoiceTurnObservation(total_latency_ms=3000.0, success=True),
                VoiceTurnObservation(total_latency_ms=5000.0, success=True),
                VoiceTurnObservation(total_latency_ms=None, success=False),
            ),
        )
        runner = SystemEvaluationRunner(
            cv_benchmark=CVBenchmark(FakeProfileExtractor()),
            stt_benchmark=STTBenchmark(FakeSTTFactory()),
            tts_benchmark=TTSBenchmark(FakeTTS()),
            question_benchmark=QuestionGeneratorBenchmark(
                FakeQuestionGenerator(),
                FakeQuestionJudge(),
            ),
            evaluator_benchmark=AnswerEvaluatorBenchmark(
                FakeAnswerEvaluator(),
                repetitions=2,
            ),
        )

        report = await runner.run(dataset)

        self.assertEqual(report.status, "partial")
        self.assertEqual(report.cv_accuracy.skill_f1, 0.5)
        self.assertEqual(report.cv_accuracy.profile_field_accuracy, 1.0)
        self.assertEqual(report.llm.question_generator.relevance_score, 0.9)
        self.assertEqual(report.llm.evaluator.score_consistency, 0.9)
        self.assertEqual(report.llm.evaluator.mae_against_human, 0.0)
        self.assertEqual(report.voice_turn.average_latency_ms, 4000.0)
        self.assertEqual(report.voice_turn.p50_latency_ms, 4000.0)
        self.assertEqual(report.voice_turn.failure_rate, 1 / 3)

        with tempfile.TemporaryDirectory() as temporary_directory:
            json_path, markdown_path = write_evaluation_reports(
                report,
                temporary_directory,
            )
            output = json_path.read_text(encoding="utf-8") + markdown_path.read_text(
                encoding="utf-8"
            )

        for sensitive_value in (
            PRIVATE_RESUME,
            PRIVATE_TRANSCRIPT,
            PRIVATE_ANSWER,
            PRIVATE_TTS_TEXT,
        ):
            self.assertNotIn(sensitive_value, output)

    async def test_empty_dataset_reports_no_data_without_loading_models(self):
        runner = SystemEvaluationRunner(
            cv_benchmark=CVBenchmark(FakeProfileExtractor()),
            stt_benchmark=STTBenchmark(FakeSTTFactory()),
            tts_benchmark=TTSBenchmark(FakeTTS()),
            question_benchmark=QuestionGeneratorBenchmark(
                FakeQuestionGenerator(),
                FakeQuestionJudge(),
            ),
            evaluator_benchmark=AnswerEvaluatorBenchmark(
                FakeAnswerEvaluator(),
                repetitions=2,
            ),
        )

        report = await runner.run(EvaluationDataset(name="empty"))

        self.assertEqual(report.status, "no_data")
        self.assertIsNone(report.stt.wer)
        self.assertIsNone(report.tts.first_audio_ms)


if __name__ == "__main__":
    unittest.main()
