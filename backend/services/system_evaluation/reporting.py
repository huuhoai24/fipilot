from __future__ import annotations

import json
from pathlib import Path

from services.system_evaluation.schemas import (
    CVAccuracyMetrics,
    DatasetValidationSummary,
    SystemEvaluationReport,
)


def write_dataset_validation(
    validation: DatasetValidationSummary,
    output_directory: str | Path,
) -> Path:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    path = output / "dataset_validation.json"
    path.write_text(
        json.dumps(validation.model_dump(mode="json"), indent=2, ensure_ascii=True)
        + "\n",
        encoding="utf-8",
    )
    return path


def write_evaluation_reports(
    report: SystemEvaluationReport,
    output_directory: str | Path,
) -> tuple[Path, Path]:
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "evaluation_report.json"
    markdown_path = output / "evaluation_report.md"
    json_path.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(_render_markdown(report), encoding="utf-8")
    return json_path, markdown_path


def _display(value: float | None, *, percent: bool = False) -> str:
    if value is None:
        return "N/A"
    if percent:
        return f"{value * 100:.2f}%"
    return f"{value:.2f}"


def _cv_rows(metrics: CVAccuracyMetrics) -> str:
    return "\n".join(
        (
            f"| Sample count | {metrics.sample_count} |",
            f"| Extraction failures | {metrics.failure_count} |",
            f"| Field accuracy | {_display(metrics.profile_field_accuracy, percent=True)} |",
            f"| Skill precision | {_display(metrics.skill_precision, percent=True)} |",
            f"| Skill recall | {_display(metrics.skill_recall, percent=True)} |",
            f"| Skill F1 | {_display(metrics.skill_f1, percent=True)} |",
            f"| Processing latency (ms) | {_display(metrics.processing_latency_ms)} |",
        )
    )


def _render_markdown(report: SystemEvaluationReport) -> str:
    summary = report.dataset_summary
    validation = report.dataset_validation
    cv = report.cv_accuracy
    pdf = report.cv_by_format.get("pdf", CVAccuracyMetrics())
    docx = report.cv_by_format.get("docx", CVAccuracyMetrics())
    stt = report.stt
    tts = report.tts
    question = report.llm.question_generator
    evaluator = report.llm.evaluator
    voice = report.voice_turn
    language_distribution = ", ".join(
        f"{language}: {count}"
        for language, count in summary.language_distribution.items()
    ) or "None"
    stt_category_rows = "\n".join(
        "| "
        f"{_category_label(category)} | {metrics.sample_count} | "
        f"{_display(metrics.wer, percent=True)} | "
        f"{_display(metrics.cer, percent=True)} | "
        f"{_display(metrics.latency_ms)} |"
        for category, metrics in stt.by_category.items()
    ) or "| No valid speech samples | 0 | N/A | N/A | N/A |"
    validation_rows = "\n".join(
        f"| {section} | {values.total_samples} | {values.valid_samples} | "
        f"{values.invalid_samples} | {values.skipped_samples} |"
        for section, values in validation.sections.items()
    ) or "| No dataset sections | 0 | 0 | 0 | 0 |"
    issue_rows = "\n".join(
        f"| {issue.replace('_', ' ').title()} | {count} |"
        for issue, count in validation.issue_counts.items()
    ) or "| None | 0 |"
    limitations = "\n".join(f"- {value}" for value in report.limitations)
    if not limitations:
        limitations = "- No additional limitations were recorded."

    return f"""# AI Interview Platform Evaluation Report

- Dataset: `{report.dataset_name}`
- Status: `{report.status}`
- Generated at: `{report.generated_at.isoformat()}`

## Benchmark Dataset Summary

| Measure | Value |
| --- | ---: |
| Total CV samples | {summary.total_cv_samples} |
| Valid CV samples | {summary.valid_cv_samples} |
| Invalid CV samples | {summary.invalid_cv_samples} |
| Total speech samples | {summary.total_speech_samples} |
| Valid speech samples | {summary.valid_speech_samples} |
| Invalid speech samples | {summary.invalid_speech_samples} |
| Language distribution | {language_distribution} |
| Average audio duration (seconds) | {_display(summary.average_audio_duration_seconds)} |
| Average transcript length (words) | {_display(summary.average_transcript_length_words)} |

## CV Extraction

### Overall CV extraction performance

| Metric | Score |
| --- | ---: |
{_cv_rows(cv)}

### PDF extraction performance

| Metric | Score |
| --- | ---: |
{_cv_rows(pdf)}

### DOCX extraction performance

| Metric | Score |
| --- | ---: |
{_cv_rows(docx)}

Parsing failures: PDF {validation.cv_parsing_failures_by_format.get('pdf', 0)}, DOCX {validation.cv_parsing_failures_by_format.get('docx', 0)}.

## Speech Recognition

| Language | Samples | WER | CER | Latency (ms) |
| --- | ---: | ---: | ---: | ---: |
{stt_category_rows}

Overall: WER {_display(stt.wer, percent=True)}, CER {_display(stt.cer, percent=True)}, latency {_display(stt.latency_ms)} ms, failures {stt.failure_count}.

## Text To Speech

| Metric | Value |
| --- | ---: |
| Sample count | {tts.sample_count} |
| Failures | {tts.failure_count} |
| First audio latency (ms) | {_display(tts.first_audio_ms)} |
| Generation duration (ms) | {_display(tts.generation_duration_ms)} |
| Generated audio duration (ms) | {_display(tts.generated_audio_duration_ms)} |
| Real time factor (RTF) | {_display(tts.real_time_factor)} |

RTF below 1 means synthesis is faster than realtime. Subjective MOS is not estimated automatically.

## LLM Interview Intelligence

| Metric | Score |
| --- | ---: |
| Sample count | {question.sample_count} |
| CV alignment | {_display(question.cv_alignment, percent=True)} |
| Relevance | {_display(question.relevance_score, percent=True)} |
| Difficulty alignment | {_display(question.difficulty_alignment, percent=True)} |
| Failures | {question.failure_count} |

## Evaluator Accuracy

| Metric | Value |
| --- | ---: |
| Sample count | {evaluator.sample_count} |
| Repetitions | {evaluator.repetitions} |
| MAE against human score | {_display(evaluator.mae_against_human)} |
| Repeated evaluation consistency | {_display(evaluator.score_consistency, percent=True)} |
| Score mean absolute deviation | {_display(evaluator.score_mean_absolute_deviation)} |
| Failures | {evaluator.failure_count} |

## Voice Realtime Performance

| Metric | Value |
| --- | ---: |
| Sample count | {voice.sample_count} |
| Average latency (ms) | {_display(voice.average_latency_ms)} |
| p50 latency (ms) | {_display(voice.p50_latency_ms)} |
| p95 latency (ms) | {_display(voice.p95_latency_ms)} |
| Failure rate | {_display(voice.failure_rate, percent=True)} |

## Dataset Validation

| Section | Total | Valid | Invalid | Skipped |
| --- | ---: | ---: | ---: | ---: |
{validation_rows}

| Validation issue | Count |
| --- | ---: |
{issue_rows}

- Invalid files: {validation.invalid_files}
- Skipped samples: {validation.skipped_samples}
- Missing annotations: {validation.missing_annotations}
- Duplicate IDs: {validation.duplicate_ids}

## Limitations

{limitations}

This report contains aggregate metrics only. Candidate names, email addresses,
Resume content, transcripts, audio, candidate answers, prompts, and tokens are
intentionally excluded.
"""


def _category_label(category: str) -> str:
    return {
        "vi": "Vietnamese",
        "en": "English",
        "mixed_technical": "Mixed technical",
    }.get(category, category)
