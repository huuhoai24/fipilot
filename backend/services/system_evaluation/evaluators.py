from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Sequence

from infrastructure.speech.stt.base import StreamingSTTFactory
from infrastructure.speech.tts.base import StreamingTTS
from services.system_evaluation.cases import (
    CVEvaluationCase,
    EvaluatorEvaluationCase,
    QuestionEvaluationCase,
    STTEvaluationCase,
    TTSEvaluationCase,
    VoiceTurnObservation,
)
from services.system_evaluation.interfaces import (
    AnswerEvaluator,
    ProfileExtractor,
    QuestionGenerator,
    QuestionQualityJudge,
)
from services.system_evaluation.metrics import (
    average,
    error_counts,
    mean_absolute_deviation,
    percentile,
    precision_recall_f1,
    profile_field_counts,
    safe_rate,
    skill_counts,
)
from services.system_evaluation.schemas import (
    CVAccuracyMetrics,
    EvaluatorMetrics,
    QuestionGeneratorMetrics,
    STTCategoryMetrics,
    STTMetrics,
    TTSMetrics,
    VoiceTurnMetrics,
)


def _status(sample_count: int, failure_count: int) -> str:
    if sample_count == 0:
        return "no_data"
    return "partial" if failure_count else "completed"


class CVBenchmark:
    def __init__(self, extractor: ProfileExtractor, *, clock=time.perf_counter) -> None:
        self._extractor = extractor
        self._clock = clock

    async def evaluate(self, cases: Sequence[CVEvaluationCase]) -> CVAccuracyMetrics:
        true_positive = predicted_count = expected_count = 0
        correct_fields = total_fields = failures = 0
        latencies: list[float] = []

        for case in cases:
            started = self._clock()
            try:
                profile = await self._extractor.extract_profile(case.resume_text)
            except Exception:
                failures += 1
                continue
            latency_ms = (self._clock() - started) * 1000 + case.document_processing_ms
            latencies.append(max(0.0, latency_ms))
            matched, predicted, expected = skill_counts(
                case.expected_skills,
                profile.skills,
            )
            true_positive += matched
            predicted_count += predicted
            expected_count += expected
            correct, total = profile_field_counts(
                profile.model_dump(mode="python"),
                case.expected_profile_fields,
            )
            correct_fields += correct
            total_fields += total

        precision, recall, f1 = precision_recall_f1(
            true_positive,
            predicted_count,
            expected_count,
        )
        return CVAccuracyMetrics(
            status=_status(len(cases), failures),
            sample_count=len(cases),
            failure_count=failures,
            skill_precision=precision if cases else None,
            skill_recall=recall if cases else None,
            skill_f1=f1 if cases else None,
            profile_field_accuracy=(
                correct_fields / total_fields if total_fields else None
            ),
            processing_latency_ms=average(latencies),
        )


class STTBenchmark:
    def __init__(
        self,
        stt_factory: StreamingSTTFactory,
        *,
        clock=time.perf_counter,
    ) -> None:
        self._stt_factory = stt_factory
        self._clock = clock

    async def evaluate(self, cases: Sequence[STTEvaluationCase]) -> STTMetrics:
        failures = 0
        word_errors = word_units = character_errors = character_units = 0
        latencies: list[float] = []
        categories: dict[str, dict[str, object]] = defaultdict(
            lambda: {
                "samples": 0,
                "word_errors": 0,
                "word_units": 0,
                "character_errors": 0,
                "character_units": 0,
                "latencies": [],
            }
        )

        for case in cases:
            stt = self._stt_factory.create()
            started = self._clock()
            try:
                await stt.start_session()
                for chunk in case.audio_chunks:
                    await stt.process_audio_chunk(chunk)
                final_event = await stt.finish_session()
                if final_event is None:
                    raise RuntimeError("STT did not emit a final transcript.")
            except Exception:
                failures += 1
                continue

            latency_ms = max(0.0, (self._clock() - started) * 1000)
            counts = error_counts(case.reference_text, final_event.text)
            word_errors += counts[0]
            word_units += counts[1]
            character_errors += counts[2]
            character_units += counts[3]
            latencies.append(latency_ms)

            category = categories[case.category]
            category["samples"] = int(category["samples"]) + 1
            category["word_errors"] = int(category["word_errors"]) + counts[0]
            category["word_units"] = int(category["word_units"]) + counts[1]
            category["character_errors"] = int(category["character_errors"]) + counts[2]
            category["character_units"] = int(category["character_units"]) + counts[3]
            category_latencies = category["latencies"]
            assert isinstance(category_latencies, list)
            category_latencies.append(latency_ms)

        by_category = {
            name: STTCategoryMetrics(
                sample_count=int(values["samples"]),
                wer=safe_rate(int(values["word_errors"]), int(values["word_units"])),
                cer=safe_rate(
                    int(values["character_errors"]),
                    int(values["character_units"]),
                ),
                latency_ms=average(values["latencies"]),  # type: ignore[arg-type]
            )
            for name, values in sorted(categories.items())
        }
        successful = len(cases) - failures
        return STTMetrics(
            status=_status(len(cases), failures),
            sample_count=len(cases),
            failure_count=failures,
            wer=safe_rate(word_errors, word_units) if successful else None,
            cer=safe_rate(character_errors, character_units) if successful else None,
            latency_ms=average(latencies),
            by_category=by_category,
        )


class TTSBenchmark:
    def __init__(self, tts: StreamingTTS, *, clock=time.perf_counter) -> None:
        self._tts = tts
        self._clock = clock

    async def evaluate(self, cases: Sequence[TTSEvaluationCase]) -> TTSMetrics:
        failures = 0
        first_audio_latencies: list[float] = []
        generation_durations: list[float] = []
        duration_ratios: list[float] = []

        for case in cases:
            started = self._clock()
            first_audio_ms: float | None = None
            total_bytes = 0
            sample_rate: int | None = None
            try:
                async for chunk in self._tts.synthesize_stream(case.text):
                    if first_audio_ms is None:
                        first_audio_ms = max(0.0, (self._clock() - started) * 1000)
                    if sample_rate is not None and sample_rate != chunk.sample_rate:
                        raise RuntimeError("TTS sample rate changed during synthesis.")
                    sample_rate = chunk.sample_rate
                    total_bytes += len(chunk.bytes)
                if first_audio_ms is None or not sample_rate or total_bytes == 0:
                    raise RuntimeError("TTS did not emit audio.")
            except Exception:
                failures += 1
                continue

            generation_ms = max(0.0, (self._clock() - started) * 1000)
            audio_duration_ms = total_bytes / (sample_rate * 2) * 1000
            first_audio_latencies.append(first_audio_ms)
            generation_durations.append(generation_ms)
            duration_ratios.append(
                generation_ms / audio_duration_ms if audio_duration_ms else 0.0
            )

        return TTSMetrics(
            status=_status(len(cases), failures),
            sample_count=len(cases),
            failure_count=failures,
            first_audio_ms=average(first_audio_latencies),
            generation_duration_ms=average(generation_durations),
            audio_duration_ratio=average(duration_ratios),
        )


class QuestionGeneratorBenchmark:
    def __init__(
        self,
        generator: QuestionGenerator,
        judge: QuestionQualityJudge,
        *,
        clock=time.perf_counter,
    ) -> None:
        self._generator = generator
        self._judge = judge
        self._clock = clock

    async def evaluate(
        self, cases: Sequence[QuestionEvaluationCase]
    ) -> QuestionGeneratorMetrics:
        failures = 0
        relevance: list[float] = []
        difficulty: list[float] = []
        cv_alignment: list[float] = []
        latencies: list[float] = []

        for case in cases:
            started = self._clock()
            try:
                question = await self._generator.generate_question(
                    case.candidate_profile,
                    case.interview_round,
                    case.interview_config,
                )
                generation_ms = max(0.0, (self._clock() - started) * 1000)
                score = await self._judge.score_question(
                    case.candidate_profile,
                    case.interview_round,
                    case.interview_config,
                    question,
                )
            except Exception:
                failures += 1
                continue
            relevance.append(score.relevance_score)
            difficulty.append(score.difficulty_alignment)
            cv_alignment.append(score.cv_alignment)
            latencies.append(generation_ms)

        return QuestionGeneratorMetrics(
            status=_status(len(cases), failures),
            sample_count=len(cases),
            failure_count=failures,
            relevance_score=average(relevance),
            difficulty_alignment=average(difficulty),
            cv_alignment=average(cv_alignment),
            generation_latency_ms=average(latencies),
        )


class AnswerEvaluatorBenchmark:
    def __init__(
        self,
        evaluator: AnswerEvaluator,
        *,
        repetitions: int = 3,
        clock=time.perf_counter,
    ) -> None:
        if repetitions < 2:
            raise ValueError("Evaluator benchmark requires at least two repetitions.")
        self._evaluator = evaluator
        self._repetitions = repetitions
        self._clock = clock

    async def evaluate(
        self, cases: Sequence[EvaluatorEvaluationCase]
    ) -> EvaluatorMetrics:
        failures = 0
        consistency_values: list[float] = []
        deviations: list[float] = []
        human_errors: list[float] = []
        latencies: list[float] = []

        for case in cases:
            scores: list[float] = []
            case_failed = False
            for _ in range(self._repetitions):
                started = self._clock()
                try:
                    evaluation = await self._evaluator.evaluate_answer(
                        case.candidate_profile,
                        case.interview_question,
                        case.candidate_answer,
                        case.interview_config,
                    )
                except Exception:
                    case_failed = True
                    break
                latencies.append(max(0.0, (self._clock() - started) * 1000))
                scores.append(evaluation.overall_score)
            if case_failed or len(scores) != self._repetitions:
                failures += 1
                continue

            deviation = mean_absolute_deviation(scores) or 0.0
            mean_score = average(scores) or 0.0
            deviations.append(deviation)
            consistency_values.append(max(0.0, 1.0 - deviation / 10.0))
            human_errors.append(abs(mean_score - case.human_score))

        return EvaluatorMetrics(
            status=_status(len(cases), failures),
            sample_count=len(cases),
            failure_count=failures,
            repetitions=self._repetitions if cases else 0,
            score_consistency=average(consistency_values),
            score_mean_absolute_deviation=average(deviations),
            mae_against_human=average(human_errors),
            evaluation_latency_ms=average(latencies),
        )


class VoiceTurnBenchmark:
    def evaluate(self, observations: Sequence[VoiceTurnObservation]) -> VoiceTurnMetrics:
        failures = sum(
            1
            for observation in observations
            if not observation.success or observation.total_latency_ms is None
        )
        latencies = [
            observation.total_latency_ms
            for observation in observations
            if observation.success and observation.total_latency_ms is not None
        ]
        return VoiceTurnMetrics(
            status=_status(len(observations), failures),
            sample_count=len(observations),
            failure_count=failures,
            average_latency_ms=average(latencies),
            p50_latency_ms=percentile(latencies, 0.50),
            p95_latency_ms=percentile(latencies, 0.95),
            failure_rate=(failures / len(observations) if observations else None),
        )
