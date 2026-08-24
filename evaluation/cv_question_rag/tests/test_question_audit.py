from __future__ import annotations

import json
from pathlib import Path

from evaluation.cv_question_rag.question_audit import write_question_audit


def _row(question_id: str, question: str, *, unsupported: bool = False) -> dict:
    return {
        "question_id": question_id,
        "resume_id": f"CV-{question_id}",
        "category": "software-development",
        "domain": "Backend_Developer",
        "language": "vi",
        "target_topic": "FastAPI",
        "question": {"question": question},
        "unsupported_experience_assumption": unsupported,
    }


def test_write_question_audit_explains_all_three_rates(tmp_path: Path) -> None:
    rows = [
        _row("Q1", "You have used FastAPI in which project?", unsupported=True),
        _row("Q2", "You have used FastAPI in which project?", unsupported=True),
        _row("Q3", "You have used FastAPI to handle errors?", unsupported=True),
        _row("Q4", "Explain dependency injection in FastAPI."),
    ]

    summary = write_question_audit(rows=rows, output_dir=tmp_path)

    assert summary["sample_count"] == 4
    assert summary["exact_duplicate_excess_count"] == 1
    assert summary["normalized_exact_duplicate_rate"] == 0.25
    assert summary["opening_repetition_excess_count"] == 2
    assert summary["opening_phrase_repetition_rate"] == 0.5
    assert summary["unsupported_experience_assumption_count"] == 3
    assert summary["unsupported_experience_assumption_rate"] == 0.75

    duplicate = [
        json.loads(line)
        for line in (tmp_path / "exact_duplicate_groups.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    assert duplicate[0]["question_ids"] == ["Q1", "Q2"]
    assert duplicate[0]["excess_count"] == 1

    openings = [
        json.loads(line)
        for line in (tmp_path / "opening_repetition_groups.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    assert openings[0]["opening"] == "you have used fastapi"
    assert openings[0]["count"] == 3

    assumptions = [
        json.loads(line)
        for line in (tmp_path / "unsupported_experience_assumptions.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    assert len(assumptions) == 3
    assert assumptions[0]["metric_flag"] is True
