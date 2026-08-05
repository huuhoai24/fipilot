from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from core.dependencies import (
    get_app_settings,
    get_document_service,
    get_evaluator_agent,
    get_llm_service,
    get_question_generator_agent,
    get_resume_agent,
    get_streaming_tts_service,
)
from infrastructure.speech.stt.faster_whisper import FasterWhisperSTTFactory
from services.system_evaluation.dataset import load_evaluation_dataset
from services.system_evaluation.evaluators import (
    AnswerEvaluatorBenchmark,
    CVBenchmark,
    QuestionGeneratorBenchmark,
    STTBenchmark,
    TTSBenchmark,
)
from services.system_evaluation.judges import GeminiQuestionQualityJudge
from services.system_evaluation.reporting import write_evaluation_reports
from services.system_evaluation.runner import SystemEvaluationRunner


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run privacy-safe offline system benchmarks."
    )
    parser.add_argument("--dataset", required=True, help="Path to evaluation manifest JSON.")
    parser.add_argument("--output-dir", default=".", help="Report output directory.")
    parser.add_argument(
        "--evaluator-repetitions",
        type=int,
        default=3,
        help="Repeated evaluator calls per human-labelled case (minimum 2).",
    )
    return parser.parse_args()


async def _run(arguments: argparse.Namespace) -> int:
    settings = get_app_settings()
    dataset = load_evaluation_dataset(arguments.dataset, get_document_service())
    stt_factory = FasterWhisperSTTFactory(
        model_name=settings.stt_model,
        device=settings.stt_device,
        compute_type=settings.stt_compute_type,
        language=settings.stt_language,
        partial_interval_ms=settings.stt_partial_interval_ms,
        vocabulary_profile=settings.stt_vocabulary_profile,
        custom_hotwords=settings.stt_hotwords,
        partial_max_audio_ms=settings.stt_partial_max_audio_ms,
        final_beam_size=settings.stt_final_beam_size,
    )
    runner = SystemEvaluationRunner(
        cv_benchmark=CVBenchmark(get_resume_agent()),
        stt_benchmark=STTBenchmark(stt_factory),
        tts_benchmark=TTSBenchmark(get_streaming_tts_service()),
        question_benchmark=QuestionGeneratorBenchmark(
            get_question_generator_agent(),
            GeminiQuestionQualityJudge(get_llm_service()),
        ),
        evaluator_benchmark=AnswerEvaluatorBenchmark(
            get_evaluator_agent(),
            repetitions=arguments.evaluator_repetitions,
        ),
    )
    report = await runner.run(dataset)
    json_path, markdown_path = write_evaluation_reports(
        report,
        Path(arguments.output_dir),
    )
    print(f"status={report.status}")
    print(f"json_report={json_path.resolve()}")
    print(f"markdown_report={markdown_path.resolve()}")
    return 0 if report.status == "completed" else 2


def main() -> int:
    return asyncio.run(_run(_arguments()))


if __name__ == "__main__":
    raise SystemExit(main())
