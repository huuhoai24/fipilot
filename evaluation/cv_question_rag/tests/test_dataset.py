from __future__ import annotations

import json
from pathlib import Path

import pymupdf

from evaluation.cv_question_rag.dataset import prepare_dataset


def _write_pdf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(path)
    document.close()


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_prepare_dataset_deduplicates_stratifies_and_omits_resume_pii(tmp_path: Path) -> None:
    corpus = tmp_path / "resumes"
    _write_pdf(
        corpus / "software-development" / "CHON_LOC_CV" / "alice@example.com.pdf",
        "Alice Example alice@example.com +84 900 000 000. Python FastAPI PostgreSQL.",
    )
    duplicate = corpus / "software-development" / "CHON_LOC_CV" / "duplicate-alice.pdf"
    duplicate.parent.mkdir(parents=True, exist_ok=True)
    duplicate.write_bytes(
        (corpus / "software-development" / "CHON_LOC_CV" / "alice@example.com.pdf").read_bytes()
    )
    _write_pdf(
        corpus / "devops-cloud-security" / "CHON_LOC_CV" / "bob-secret.pdf",
        "Bob Secret bob@example.com. Kubernetes Docker Terraform CI CD.",
    )
    _write_pdf(
        corpus / "product-qa" / "CHON_LOC_CV" / "carol-private.pdf",
        "Carol Private. Selenium Playwright test automation quality assurance.",
    )

    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "domains": {
                    "Backend_Developer": [
                        {"title": "FastAPI", "path": ["Python", "Web"], "anchors": ["API"]}
                    ],
                    "DevOps_Engineer": [
                        {"title": "Kubernetes", "path": ["Cloud"], "anchors": ["Containers"]}
                    ],
                    "Tester_QA_QC": [
                        {"title": "Selenium", "path": ["Automation"], "anchors": ["Browser"]}
                    ],
                }
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    output = tmp_path / "dataset"

    summary = prepare_dataset(
        corpus_dir=corpus,
        catalog_path=catalog,
        output_dir=output,
        sample_size=3,
        development_ratio=2 / 3,
        seed=20260820,
    )

    assert summary["inventory"]["pdf_files"] == 4
    assert summary["inventory"]["unique_files"] == 3
    assert summary["inventory"]["duplicate_files"] == 1
    assert summary["dataset"]["selected"] == 3
    assert summary["dataset"]["domains"] == {
        "Backend_Developer": 1,
        "DevOps_Engineer": 1,
        "Tester_QA_QC": 1,
    }

    development = _read_jsonl(output / "development.jsonl")
    holdout = _read_jsonl(output / "holdout.jsonl")
    assert len(development) == 2
    assert len(holdout) == 1
    assert {row["resume_id"] for row in development}.isdisjoint(
        row["resume_id"] for row in holdout
    )

    serialized = "\n".join((output / name).read_text(encoding="utf-8") for name in (
        "corpus_manifest.jsonl",
        "development.jsonl",
        "holdout.jsonl",
        "DATASET_MANIFEST.json",
    ))
    for private_value in (
        "Alice Example",
        "alice@example.com",
        "+84 900 000 000",
        "bob-secret.pdf",
        "carol-private.pdf",
    ):
        assert private_value not in serialized
    assert all(row["resume_id"].startswith("CV-") for row in development + holdout)
    assert all(row["label_source"] == "resume_exact_catalog_title" for row in development + holdout)


def test_prepare_dataset_limits_pdf_reads_to_a_deterministic_stratified_subset(
    tmp_path: Path,
) -> None:
    corpus = tmp_path / "resumes"
    for category, skill in (
        ("software-development", "FastAPI"),
        ("devops-cloud-security", "Kubernetes"),
        ("product-qa", "Selenium"),
    ):
        _write_pdf(
            corpus / category / "CHON_LOC_CV" / f"{skill}.pdf",
            f"Public Resume with {skill} experience.",
        )
    catalog = tmp_path / "catalog.json"
    catalog.write_text(
        json.dumps(
            {
                "domains": {
                    "Backend_Developer": [{"title": "FastAPI", "path": [], "anchors": []}],
                    "DevOps_Engineer": [{"title": "Kubernetes", "path": [], "anchors": []}],
                    "Tester_QA_QC": [{"title": "Selenium", "path": [], "anchors": []}],
                }
            }
        ),
        encoding="utf-8",
    )

    summary = prepare_dataset(
        corpus_dir=corpus,
        catalog_path=catalog,
        output_dir=tmp_path / "limited",
        corpus_limit=2,
        sample_size=2,
        development_ratio=0.5,
        seed=20260820,
    )

    assert summary["inventory"]["source_pdf_files"] == 3
    assert summary["inventory"]["pdf_files"] == 2
    assert summary["inventory"]["corpus_limit"] == 2
    assert summary["dataset"]["selected"] == 2
