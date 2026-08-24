from __future__ import annotations

import json
from pathlib import Path

import pymupdf

from evaluation.cv_question_rag.dataset import prepare_dataset
from evaluation.cv_question_rag.retrieval import run_retrieval


REPO_ROOT = Path(__file__).resolve().parents[3]


def _write_pdf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(path)
    document.close()


def test_run_retrieval_records_rank_latency_and_source_derived_metrics(tmp_path: Path) -> None:
    corpus = tmp_path / "resumes"
    _write_pdf(
        corpus / "software-development" / "CHON_LOC_CV" / "private-name.pdf",
        "Private Candidate private@example.com. FastAPI Python backend API production.",
    )
    dataset_dir = tmp_path / "dataset"
    prepare_dataset(
        corpus_dir=corpus,
        catalog_path=REPO_ROOT / "backend/services/interview_knowledge/catalog.json",
        output_dir=dataset_dir,
        sample_size=1,
        development_ratio=0.7,
        seed=20260820,
    )

    output_dir = tmp_path / "retrieval-run"
    metrics = run_retrieval(
        repo_root=REPO_ROOT,
        dataset_path=dataset_dir / "corpus_manifest.jsonl",
        output_dir=output_dir,
        seed=20260820,
    )

    rows = [
        json.loads(line)
        for line in (output_dir / "retrieval.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(rows) == 1
    assert rows[0]["resume_id"].startswith("CV-")
    assert rows[0]["system"] == "production_lexical"
    assert rows[0]["expected_topic_ids"]
    assert rows[0]["retrieved_topics"]
    assert rows[0]["latency_ms"] >= 0
    assert rows[0]["hit_at_8"] is True
    assert metrics["sample_count"] == 1
    assert metrics["hit_rate_at_8"] == 1.0
    assert metrics["label_source"] == "resume_exact_catalog_title"
    assert metrics["human_relevance_labels"] is False

    serialized = (output_dir / "retrieval.jsonl").read_text(encoding="utf-8")
    assert "private-name.pdf" not in serialized
    assert "private@example.com" not in serialized
