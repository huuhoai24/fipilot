from __future__ import annotations

import csv
import json
from pathlib import Path

from evaluation.cv_question_rag.reporting import build_reports


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def test_build_reports_separates_llm_metrics_from_blinded_human_review(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "dataset"
    run_dir = tmp_path / "run"
    docs_dir = tmp_path / "docs"
    _write_json(
        dataset_dir / "DATASET_MANIFEST.json",
        {
            "dataset": {"selected": 2, "development": 1, "holdout": 1},
            "inventory": {"source_pdf_files": 20, "pdf_files": 5},
            "privacy": {"filenames_recorded": False},
        },
    )
    _write_json(
        run_dir / "RETRIEVAL_METRICS.json",
        {
            "sample_count": 2,
            "hit_rate_at_1": 0.5,
            "hit_rate_at_3": 1.0,
            "hit_rate_at_5": 1.0,
            "hit_rate_at_8": 1.0,
            "recall_at_5": 0.75,
            "recall_at_8": 1.0,
            "mrr_at_8": 0.75,
            "latency_ms": {"mean": 6.0, "p95": 9.0},
            "human_relevance_labels": False,
        },
    )
    _write_jsonl(run_dir / "retrieval.jsonl", [{"resume_id": "CV-ONE"}])
    _write_json(
        run_dir / "QUESTION_METRICS.json",
        {
            "sample_count": 1,
            "technical_validity_rate": 1.0,
            "cv_alignment_rate": 1.0,
            "mean_rag_grounding": 1.5,
            "human_review_status": "NOT_COMPLETED",
        },
    )
    _write_jsonl(
        run_dir / "questions.jsonl",
        [
            {
                "question_id": "QUESTION-1",
                "resume_id": "CV-ONE",
                "category": "software-development",
                "domain": "Backend_Developer",
                "level": "Middle",
                "language": "vi",
                "target_topic": "FastAPI",
                "question": {"question": "Bạn xử lý FastAPI dependency failure thế nào?"},
                "usage": {"input_tokens": 100, "output_tokens": 50},
            }
        ],
    )
    _write_jsonl(
        run_dir / "judgments.jsonl",
        [
            {
                "question_id": "QUESTION-1",
                "resume_id": "CV-ONE",
                "judgment": {"technical_validity": 1, "cv_alignment": 1},
                "usage": {"input_tokens": 200, "output_tokens": 40},
            }
        ],
    )

    result = build_reports(
        dataset_dir=dataset_dir,
        run_dir=run_dir,
        docs_dir=docs_dir,
        review_sample_size=1,
        seed=20260820,
    )

    assert result["status"] == "PARTIAL_PENDING_HUMAN_REVIEW"
    report = (docs_dir / "CV_QUESTION_RAG_REPORT.md").read_text(encoding="utf-8")
    assert "Resume subset scanned: 5 / 20" in report
    assert "LLM-as-judge" in report
    assert "human-labelled" in report
    assert "Unsupported experience-assumption rate" in report

    with (docs_dir / "HUMAN_REVIEW_TEMPLATE.csv").open(encoding="utf-8", newline="") as handle:
        review_rows = list(csv.DictReader(handle))
    assert review_rows[0]["question"] == "Bạn xử lý FastAPI dependency failure thế nào?"
    assert review_rows[0]["technical_validity"] == ""
    assert "model_technical_validity" not in review_rows[0]

    mapping = json.loads((docs_dir / "HUMAN_REVIEW_MAPPING.json").read_text(encoding="utf-8"))
    assert mapping[0]["review_id"].startswith("REVIEW-")
    assert mapping[0]["question_id"] == "QUESTION-1"
    assert "resume_id" not in mapping[0]
    assert (docs_dir / "COST_REPORT.json").exists()
    assert (run_dir / "QUESTION_PATTERN_AUDIT.json").exists()
    assert (run_dir / "exact_duplicate_groups.jsonl").exists()
    assert (run_dir / "opening_repetition_groups.jsonl").exists()
    assert (run_dir / "unsupported_experience_assumptions.jsonl").exists()
