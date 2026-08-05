from __future__ import annotations

from services.system_evaluation.cases import EvaluationDataset
from services.system_evaluation.evaluators import (
    AnswerEvaluatorBenchmark,
    CVBenchmark,
    QuestionGeneratorBenchmark,
    STTBenchmark,
    TTSBenchmark,
    VoiceTurnBenchmark,
)
from services.system_evaluation.schemas import LLMMetrics, SystemEvaluationReport


class SystemEvaluationRunner:
    def __init__(
        self,
        *,
        cv_benchmark: CVBenchmark,
        stt_benchmark: STTBenchmark,
        tts_benchmark: TTSBenchmark,
        question_benchmark: QuestionGeneratorBenchmark,
        evaluator_benchmark: AnswerEvaluatorBenchmark,
        voice_benchmark: VoiceTurnBenchmark | None = None,
    ) -> None:
        self._cv = cv_benchmark
        self._stt = stt_benchmark
        self._tts = tts_benchmark
        self._question = question_benchmark
        self._evaluator = evaluator_benchmark
        self._voice = voice_benchmark or VoiceTurnBenchmark()

    async def run(self, dataset: EvaluationDataset) -> SystemEvaluationReport:
        cv = await self._cv.evaluate(dataset.cv_cases)
        stt = await self._stt.evaluate(dataset.stt_cases)
        tts = await self._tts.evaluate(dataset.tts_cases)
        question = await self._question.evaluate(dataset.question_cases)
        evaluator = await self._evaluator.evaluate(dataset.evaluator_cases)
        voice = self._voice.evaluate(dataset.voice_turns)
        section_statuses = {
            cv.status,
            stt.status,
            tts.status,
            question.status,
            evaluator.status,
            voice.status,
        }
        if section_statuses == {"no_data"}:
            status = "no_data"
        elif "partial" in section_statuses:
            status = "partial"
        else:
            status = "completed"
        return SystemEvaluationReport(
            dataset_name=dataset.name,
            status=status,
            cv_accuracy=cv,
            stt=stt,
            tts=tts,
            llm=LLMMetrics(
                question_generator=question,
                evaluator=evaluator,
            ),
            voice_turn=voice,
        )
