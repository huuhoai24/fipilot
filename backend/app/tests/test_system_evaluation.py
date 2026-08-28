from __future__ import annotations

import json
import os
import tempfile
import unittest
import wave
from csv import DictWriter
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, patch

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
from scripts.run_system_evaluation import (
    _load_benchmark_environment,
    _select_benchmark_sections,
)
from services.system_evaluation.judges import GeminiQuestionQualityJudge
from core.dependencies import get_app_settings
from core.settings import get_settings
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


class FailingProfileExtractor:
    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        raise RuntimeError("model unavailable")


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


class FakeDeferredSTT(FakeSTT):
    supports_deferred_partials = True

    def __init__(self) -> None:
        self.appended = bytearray()

    async def append_audio(self, audio_bytes: bytes) -> None:
        self.appended.extend(audio_bytes)

    async def process_audio_chunk(self, audio_bytes: bytes) -> TranscriptEvent | None:
        raise AssertionError("Deferred STT must not run partial transcription in benchmark")


class FakeDeferredSTTFactory(StreamingSTTFactory):
    def __init__(self) -> None:
        self.instance = FakeDeferredSTT()

    def create(self) -> StreamingSTT:
        return self.instance


class FakeTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        yield AudioChunk(bytes=b"\x00\x00" * 1600, sample_rate=16_000)


class FakeQuestionGenerator:
    def __init__(self) -> None:
        self.calls = 0

    async def generate_question(self, candidate_profile, interview_round, interview_config):
        self.calls += 1
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
    def test_benchmark_environment_loads_dotenv_without_overriding_process_values(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            env_path = Path(temporary_directory) / ".env"
            env_path.write_text(
                "GOOGLE_CLOUD_PROJECT=dotenv-project\n"
                "GEMINI_SIMPLE_MODEL=dotenv-model\n",
                encoding="utf-8",
            )
            with patch.dict(
                os.environ,
                {"GEMINI_SIMPLE_MODEL": "process-model"},
                clear=True,
            ):
                get_settings.cache_clear()
                get_app_settings.cache_clear()
                self.assertIsNone(get_app_settings().google_cloud_project)
                _load_benchmark_environment(env_path)
                settings = get_app_settings()

        self.assertEqual(settings.google_cloud_project, "dotenv-project")
        self.assertEqual(settings.gemini_simple_model, "process-model")

    def test_targeted_benchmark_excludes_unselected_sections(self):
        dataset = EvaluationDataset(
            cv_cases=(CVEvaluationCase(case_id="cv", resume_text="resume"),),
            stt_cases=(object(),),  # type: ignore[arg-type]
            tts_cases=(object(),),  # type: ignore[arg-type]
            question_cases=(object(),),  # type: ignore[arg-type]
            evaluator_cases=(object(),),  # type: ignore[arg-type]
            voice_turns=(object(),),  # type: ignore[arg-type]
        )

        selected = _select_benchmark_sections(
            dataset,
            {"cv", "question", "evaluator"},
        )

        self.assertEqual(selected.cv_cases, dataset.cv_cases)
        self.assertEqual(selected.question_cases, dataset.question_cases)
        self.assertEqual(selected.evaluator_cases, dataset.evaluator_cases)
        self.assertEqual(selected.stt_cases, ())
        self.assertEqual(selected.tts_cases, ())
        self.assertEqual(selected.voice_turns, ())

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

    def test_directory_dataset_loads_existing_cv_and_24khz_stt_samples(self):
        class FakeDocumentService:
            def __init__(self):
                self.filenames: list[str] = []

            def extract_text(self, file_path: str, filename: str | None = None) -> str:
                assert filename is not None
                self.filenames.append(filename)
                return PRIVATE_RESUME

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            resumes = root / "cv" / "resumes"
            labels = root / "cv" / "ground-truth"
            audio_directory = root / "stt" / "audio"
            resumes.mkdir(parents=True)
            labels.mkdir(parents=True)
            audio_directory.mkdir(parents=True)

            (resumes / "resume_001.pdf").write_bytes(b"pdf")
            (resumes / "resume_001.docx").write_bytes(b"docx")
            (labels / "resume_001.json").write_text(
                json.dumps(
                    {
                        "cv_id": "cv_001",
                        "full_name": "Private Candidate",
                        "email": "private@example.test",
                        "skills": ["Python", "FastAPI"],
                        "experiences": [
                            {
                                "company": "Example",
                                "position": "Backend Engineer",
                                "start_date": "2024",
                                "end_date": "Present",
                                "description": ["Built APIs"],
                            }
                        ],
                        "projects": [],
                        "education": [],
                    }
                ),
                encoding="utf-8",
            )

            with wave.open(str(audio_directory / "sample.wav"), "wb") as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(24_000)
                audio.writeframes(b"\x00\x00" * 2400)
            with (root / "stt" / "metadata.csv").open(
                "w", encoding="utf-8", newline=""
            ) as metadata:
                writer = DictWriter(
                    metadata,
                    fieldnames=["filename", "text", "duration", "language"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "filename": "sample.wav",
                        "text": f"Toi dung FastAPI {PRIVATE_TRANSCRIPT}",
                        "duration": "0.1",
                        "language": "vi",
                    }
                )

            (root / "tts").mkdir()
            (root / "tts" / "cases.json").write_text(
                json.dumps(
                    {
                        "synthetic": True,
                        "cases": [{"case_id": "tts-1", "text": PRIVATE_TTS_TEXT}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "llm").mkdir()
            (root / "llm" / "interview_cases.json").write_text(
                json.dumps(
                    {
                        "synthetic": True,
                        "cases": [
                            {
                                "case_id": "llm-1",
                                "candidate_profile": {
                                    "name": "Candidate",
                                    "skills": ["FastAPI"],
                                },
                                "expected_topics": ["FastAPI"],
                                "expected_level": "junior",
                                "generated_question": "How did you test your API?",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (root / "evaluator").mkdir()
            (root / "evaluator" / "human_labels.json").write_text(
                json.dumps(
                    {
                        "synthetic": True,
                        "cases": [
                            {
                                "case_id": "eval-1",
                                "question": "What is a transaction?",
                                "candidate_answer": PRIVATE_ANSWER,
                                "human_score": 8,
                                "human_feedback_category": "correct",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (root / "voice").mkdir()
            (root / "voice" / "latency_samples.json").write_text(
                json.dumps(
                    {
                        "synthetic": True,
                        "cases": [
                            {
                                "case_id": "voice-1",
                                "success": True,
                                "speech_end_time": 0,
                                "stt_final_time": 0.2,
                                "evaluation_start": 0.3,
                                "question_first_token": 0.8,
                                "tts_first_audio": 1.2,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            document_service = FakeDocumentService()
            dataset = load_evaluation_dataset(root, document_service)

        self.assertEqual(len(dataset.cv_cases), 2)
        self.assertEqual(
            {case.document_format for case in dataset.cv_cases}, {"pdf", "docx"}
        )
        self.assertEqual(document_service.filenames, ["resume_001.docx", "resume_001.pdf"])
        self.assertEqual(len(dataset.stt_cases), 1)
        self.assertEqual(dataset.stt_cases[0].category, "mixed_technical")
        self.assertEqual(sum(map(len, dataset.stt_cases[0].audio_chunks)), 3200)
        self.assertEqual(dataset.summary.total_cv_samples, 2)
        self.assertEqual(dataset.summary.valid_cv_samples, 2)
        self.assertEqual(dataset.summary.total_speech_samples, 1)
        self.assertEqual(dataset.validation.invalid_files, 0)
        self.assertEqual(len(dataset.tts_cases), 1)
        self.assertEqual(len(dataset.question_cases), 1)
        self.assertIsNotNone(dataset.question_cases[0].generated_question)
        self.assertEqual(len(dataset.evaluator_cases), 1)
        self.assertEqual(dataset.voice_turns[0].total_latency_ms, 1200.0)
        self.assertEqual(
            dataset.summary.synthetic_sections,
            ["TTS", "LLM question generation", "evaluator", "voice latency"],
        )

    def test_directory_validation_skips_invalid_samples_and_redacts_paths(self):
        class FakeDocumentService:
            def extract_text(self, file_path: str, filename: str | None = None) -> str:
                return PRIVATE_RESUME

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            resumes = root / "cv" / "resumes"
            labels = root / "cv" / "ground_truth"
            audio_directory = root / "stt" / "audio"
            resumes.mkdir(parents=True)
            labels.mkdir(parents=True)
            audio_directory.mkdir(parents=True)
            (resumes / "candidate-private-name.pdf").write_bytes(b"pdf")
            (root / "llm").mkdir()
            (root / "llm" / "interview_cases.json").write_text("{", encoding="utf-8")

            with (root / "stt" / "metadata.csv").open(
                "w", encoding="utf-8", newline=""
            ) as metadata:
                writer = DictWriter(metadata, fieldnames=["filename", "text", "language"])
                writer.writeheader()
                writer.writerow(
                    {"filename": "missing.wav", "text": "", "language": "vi"}
                )
                writer.writerow(
                    {"filename": "missing.wav", "text": "duplicate", "language": "vi"}
                )

            dataset = load_evaluation_dataset(root, FakeDocumentService())
            serialized = dataset.validation.model_dump_json()

        self.assertEqual(dataset.cv_cases, ())
        self.assertEqual(dataset.stt_cases, ())
        self.assertGreaterEqual(dataset.validation.missing_annotations, 1)
        self.assertGreaterEqual(dataset.validation.duplicate_ids, 1)
        self.assertGreaterEqual(dataset.validation.skipped_samples, 3)
        self.assertNotIn("candidate-private-name", serialized)
        self.assertNotIn("missing.wav", serialized)


class SystemEvaluationRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_question_benchmark_can_regenerate_curated_questions(self):
        generator = FakeQuestionGenerator()
        case = QuestionEvaluationCase(
            case_id="question-regenerate",
            candidate_profile=CandidateProfile(name="Candidate", skills=["FastAPI"]),
            interview_round=InterviewRound(
                round_id="round",
                topic="FastAPI",
                objective="Assess API design.",
                difficulty="medium",
            ),
            interview_config=InterviewConfig(
                mode="text",
                language="en",
                experience_level="middle",
            ),
            generated_question=InterviewQuestion(
                question="Curated benchmark question",
                language="en",
                topic="FastAPI",
                difficulty="medium",
            ),
        )
        benchmark = QuestionGeneratorBenchmark(
            generator,
            FakeQuestionJudge(),
            regenerate_existing=True,
        )

        metrics = await benchmark.evaluate((case,))

        self.assertEqual(generator.calls, 1)
        self.assertEqual(metrics.status, "completed")
        self.assertIsNotNone(metrics.generation_latency_ms)

    async def test_question_quality_judge_builds_candidate_prompt(self):
        llm_service = AsyncMock()
        llm_service.generate_json.return_value = QuestionQualityScore(
            relevance_score=0.9,
            difficulty_alignment=0.8,
            cv_alignment=0.85,
        )
        judge = GeminiQuestionQualityJudge(llm_service)

        score = await judge.score_question(
            CandidateProfile(
                candidate_id="private-id",
                name="Candidate",
                skills=["FastAPI"],
            ),
            InterviewRound(
                round_id="round",
                topic="FastAPI",
                objective="Assess API design.",
                difficulty="medium",
            ),
            InterviewConfig(
                mode="text",
                language="en",
                experience_level="middle",
            ),
            InterviewQuestion(
                question="How did you design the API?",
                language="en",
                topic="FastAPI",
                difficulty="medium",
            ),
        )

        self.assertEqual(score.relevance_score, 0.9)
        prompt = llm_service.generate_json.await_args.args[0]
        self.assertNotIn("private-id", prompt)
        self.assertIsNone(
            llm_service.generate_json.await_args.kwargs["thinking_budget"]
        )

    async def test_cv_metrics_are_na_when_every_extraction_fails(self):
        metrics = await CVBenchmark(FailingProfileExtractor()).evaluate(
            (
                CVEvaluationCase(
                    case_id="cv-failure",
                    resume_text=PRIVATE_RESUME,
                    expected_skills=("Python",),
                    document_format="pdf",
                ),
            )
        )

        self.assertEqual(metrics.failure_count, 1)
        self.assertIsNone(metrics.skill_precision)
        self.assertIsNone(metrics.skill_recall)
        self.assertIsNone(metrics.skill_f1)

    async def test_stt_benchmark_uses_deferred_buffering_without_partial_inference(self):
        factory = FakeDeferredSTTFactory()
        metrics = await STTBenchmark(factory).evaluate(
            (
                STTEvaluationCase(
                    case_id="stt-deferred",
                    audio_chunks=(b"one", b"two"),
                    reference_text="xin ban",
                    category="vi",
                ),
            )
        )

        self.assertEqual(metrics.failure_count, 0)
        self.assertEqual(factory.instance.appended, b"onetwo")

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
                    document_format="pdf",
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
        self.assertEqual(report.cv_by_format["pdf"].sample_count, 1)
        self.assertEqual(report.cv_by_format["docx"].sample_count, 0)
        self.assertEqual(report.llm.question_generator.relevance_score, 0.9)
        self.assertEqual(report.llm.evaluator.score_consistency, 0.9)
        self.assertEqual(report.llm.evaluator.mae_against_human, 0.0)
        self.assertEqual(report.voice_turn.average_latency_ms, 4000.0)
        self.assertEqual(report.voice_turn.p50_latency_ms, 4000.0)
        self.assertEqual(report.voice_turn.failure_rate, 1 / 3)
        self.assertEqual(report.tts.generated_audio_duration_ms, 100.0)
        self.assertIsNotNone(report.tts.real_time_factor)

        with tempfile.TemporaryDirectory() as temporary_directory:
            json_path, markdown_path = write_evaluation_reports(
                report,
                temporary_directory,
            )
            output = json_path.read_text(encoding="utf-8") + markdown_path.read_text(
                encoding="utf-8"
            )

        self.assertIn("# AI Interview Platform Evaluation Report", output)
        self.assertIn("## Benchmark Dataset Summary", output)
        self.assertIn("## Dataset Validation", output)
        self.assertIn("## Limitations", output)

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
