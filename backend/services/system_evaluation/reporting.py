from __future__ import annotations

import json
from pathlib import Path

from services.system_evaluation.schemas import SystemEvaluationReport


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


def _render_markdown(report: SystemEvaluationReport) -> str:
    cv = report.cv_accuracy
    stt = report.stt
    tts = report.tts
    question = report.llm.question_generator
    evaluator = report.llm.evaluator
    voice = report.voice_turn
    stt_category_rows = "\n".join(
        "| "
        f"{category} | {metrics.sample_count} | "
        f"{_display(metrics.wer, percent=True)} | "
        f"{_display(metrics.cer, percent=True)} | "
        f"{_display(metrics.latency_ms)} |"
        for category, metrics in stt.by_category.items()
    ) or "| No category data | 0 | N/A | N/A | N/A |"
    return f"""# AI Interview System Evaluation

- Dataset: `{report.dataset_name}`
- Status: `{report.status}`
- Generated at: `{report.generated_at.isoformat()}`

## CV Evaluation

| Metric | Value |
| --- | ---: |
| Samples | {cv.sample_count} |
| Failures | {cv.failure_count} |
| Skill precision | {_display(cv.skill_precision, percent=True)} |
| Skill recall | {_display(cv.skill_recall, percent=True)} |
| Skill F1 | {_display(cv.skill_f1, percent=True)} |
| Profile field accuracy | {_display(cv.profile_field_accuracy, percent=True)} |
| Processing latency (ms) | {_display(cv.processing_latency_ms)} |

## STT Evaluation

| Metric | Value |
| --- | ---: |
| Samples | {stt.sample_count} |
| Failures | {stt.failure_count} |
| WER | {_display(stt.wer, percent=True)} |
| CER | {_display(stt.cer, percent=True)} |
| Transcription latency (ms) | {_display(stt.latency_ms)} |

### STT Language Categories

| Category | Samples | WER | CER | Latency (ms) |
| --- | ---: | ---: | ---: | ---: |
{stt_category_rows}

## TTS Evaluation

| Metric | Value |
| --- | ---: |
| Samples | {tts.sample_count} |
| Failures | {tts.failure_count} |
| First audio (ms) | {_display(tts.first_audio_ms)} |
| Generation duration (ms) | {_display(tts.generation_duration_ms)} |
| Generation/audio duration ratio | {_display(tts.audio_duration_ratio)} |

## LLM Evaluation

| Metric | Value |
| --- | ---: |
| Question relevance | {_display(question.relevance_score, percent=True)} |
| Difficulty alignment | {_display(question.difficulty_alignment, percent=True)} |
| CV alignment | {_display(question.cv_alignment, percent=True)} |
| Question latency (ms) | {_display(question.generation_latency_ms)} |
| Evaluator consistency | {_display(evaluator.score_consistency, percent=True)} |
| Evaluator MAE vs human | {_display(evaluator.mae_against_human)} |
| Evaluator latency (ms) | {_display(evaluator.evaluation_latency_ms)} |

## End-to-End Voice Evaluation

| Metric | Value |
| --- | ---: |
| Samples | {voice.sample_count} |
| Failures | {voice.failure_count} |
| Average latency (ms) | {_display(voice.average_latency_ms)} |
| p50 latency (ms) | {_display(voice.p50_latency_ms)} |
| p95 latency (ms) | {_display(voice.p95_latency_ms)} |
| Failure rate | {_display(voice.failure_rate, percent=True)} |

This report contains aggregate metrics only. Audio, transcripts, Resume content,
candidate answers, prompts, and tokens are intentionally excluded.
"""
