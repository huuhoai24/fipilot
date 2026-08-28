from __future__ import annotations

import argparse
import asyncio
from dataclasses import replace
from pathlib import Path
import sys

from dotenv import load_dotenv


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
from core.settings import get_settings
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
from services.system_evaluation.reporting import (
    write_dataset_validation,
    write_evaluation_reports,
)
from services.system_evaluation.runner import SystemEvaluationRunner


BENCHMARK_SECTIONS = ("cv", "stt", "tts", "question", "evaluator", "voice")


class _UnavailableCloudBenchmark:
    def __init__(self, reason: str) -> None:
        self._reason = reason

    async def extract_profile(self, resume_text):
        raise RuntimeError(self._reason)

    async def generate_question(self, *args):
        raise RuntimeError(self._reason)

    async def score_question(self, *args):
        raise RuntimeError(self._reason)

    async def evaluate_answer(self, *args):
        raise RuntimeError(self._reason)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run privacy-safe offline system benchmarks."
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to an evaluation dataset directory or legacy manifest JSON.",
    )
    parser.add_argument("--output-dir", default=".", help="Report output directory.")
    parser.add_argument(
        "--evaluator-repetitions",
        type=int,
        default=3,
        help="Repeated evaluator calls per human-labelled case (minimum 2).",
    )
    parser.add_argument(
        "--sections",
        nargs="+",
        choices=BENCHMARK_SECTIONS,
        default=list(BENCHMARK_SECTIONS),
        help="Benchmark sections to run (default: all sections).",
    )
    return parser.parse_args()


async def _run(arguments: argparse.Namespace) -> int:
    settings = get_app_settings()
    dataset_path = _resolve_cli_path(arguments.dataset)
    output_directory = _resolve_cli_path(arguments.output_dir, must_exist=False)
    dataset = load_evaluation_dataset(dataset_path, get_document_service())
    validation_path = write_dataset_validation(dataset.validation, output_directory)
    selected_sections = set(arguments.sections)
    benchmark_dataset = _select_benchmark_sections(dataset, selected_sections)
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
    runtime_limitations: list[str] = []
    if settings.google_cloud_project:
        profile_extractor = get_resume_agent()
        question_generator = get_question_generator_agent()
        question_judge = GeminiQuestionQualityJudge(get_llm_service())
        answer_evaluator = get_evaluator_agent()
    else:
        unavailable = _UnavailableCloudBenchmark(
            "Google Cloud model configuration is unavailable for this benchmark run."
        )
        profile_extractor = unavailable
        question_generator = unavailable
        question_judge = unavailable
        answer_evaluator = unavailable
        runtime_limitations.append(
            "Cloud-backed CV, LLM judge, and evaluator metrics are N/A because "
            "GOOGLE_CLOUD_PROJECT was not configured."
        )
    runner = SystemEvaluationRunner(
        cv_benchmark=CVBenchmark(profile_extractor),
        stt_benchmark=STTBenchmark(stt_factory),
        tts_benchmark=TTSBenchmark(get_streaming_tts_service()),
        question_benchmark=QuestionGeneratorBenchmark(
            question_generator,
            question_judge,
            regenerate_existing=True,
        ),
        evaluator_benchmark=AnswerEvaluatorBenchmark(
            answer_evaluator,
            repetitions=arguments.evaluator_repetitions,
        ),
    )
    report = await runner.run(benchmark_dataset)
    skipped_sections = [
        section for section in BENCHMARK_SECTIONS if section not in selected_sections
    ]
    if skipped_sections:
        runtime_limitations.append(
            "Sections excluded from this targeted run: " + ", ".join(skipped_sections) + "."
        )
    if runtime_limitations:
        report = report.model_copy(
            update={"limitations": report.limitations + runtime_limitations}
        )
    json_path, markdown_path = write_evaluation_reports(
        report,
        output_directory,
    )
    print(f"status={report.status}")
    print(f"dataset_validation={validation_path.resolve()}")
    print(f"json_report={json_path.resolve()}")
    print(f"markdown_report={markdown_path.resolve()}")
    return 0 if report.status != "no_data" else 2


def _resolve_cli_path(value: str | Path, *, must_exist: bool = True) -> Path:
    path = Path(value)
    candidates = [path] if path.is_absolute() else [Path.cwd() / path, BACKEND_ROOT.parent / path]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    resolved = candidates[0].resolve()
    if must_exist:
        raise FileNotFoundError(f"Evaluation dataset was not found: {resolved}")
    return resolved


def _load_benchmark_environment(env_path: Path | None = None) -> None:
    """Load local benchmark configuration without overriding process variables."""

    load_dotenv(env_path or BACKEND_ROOT / ".env", override=False)
    get_settings.cache_clear()
    get_app_settings.cache_clear()


def _select_benchmark_sections(dataset, selected_sections: set[str]):
    """Return a dataset view containing only the requested benchmark cases."""

    return replace(
        dataset,
        cv_cases=dataset.cv_cases if "cv" in selected_sections else (),
        stt_cases=dataset.stt_cases if "stt" in selected_sections else (),
        tts_cases=dataset.tts_cases if "tts" in selected_sections else (),
        question_cases=(
            dataset.question_cases if "question" in selected_sections else ()
        ),
        evaluator_cases=(
            dataset.evaluator_cases if "evaluator" in selected_sections else ()
        ),
        voice_turns=dataset.voice_turns if "voice" in selected_sections else (),
    )


def main() -> int:
    _load_benchmark_environment()
    return asyncio.run(_run(_arguments()))


if __name__ == "__main__":
    raise SystemExit(main())
