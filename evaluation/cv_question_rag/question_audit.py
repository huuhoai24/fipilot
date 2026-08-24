from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


TOKENS = re.compile(r"[a-z0-9+#.]+", re.IGNORECASE)


def _normalize(value: str) -> str:
    """Match the frozen M6 duplicate/opening normalization exactly."""
    return " ".join(TOKENS.findall(value.lower()))


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
        ),
        encoding="utf-8",
    )


def _group_id(prefix: str, key: str) -> str:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:12].upper()
    return f"{prefix}-{digest}"


def _question_record(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "question_id": row["question_id"],
        "resume_id": row["resume_id"],
        "category": row["category"],
        "domain": row["domain"],
        "language": row["language"],
        "target_topic": row["target_topic"],
        "question": row["question"]["question"],
    }


def write_question_audit(
    *, rows: list[dict[str, Any]], output_dir: Path
) -> dict[str, Any]:
    exact: dict[str, list[dict[str, Any]]] = defaultdict(list)
    openings: dict[str, list[dict[str, Any]]] = defaultdict(list)
    assumptions: list[dict[str, Any]] = []

    for row in rows:
        record = _question_record(row)
        normalized = _normalize(record["question"])
        exact[normalized].append(record)
        opening = " ".join(normalized.split()[:4])
        openings[opening].append(record)
        if row.get("unsupported_experience_assumption"):
            assumptions.append({**record, "metric_flag": True})

    duplicate_groups = [
        {
            "group_id": _group_id("DUPLICATE", normalized),
            "normalized_question": normalized,
            "count": len(group),
            "excess_count": len(group) - 1,
            "question_ids": [item["question_id"] for item in group],
            "resume_ids": [item["resume_id"] for item in group],
            "questions": [item["question"] for item in group],
        }
        for normalized, group in sorted(exact.items())
        if len(group) > 1
    ]
    opening_groups = [
        {
            "group_id": _group_id("OPENING", opening),
            "opening": opening,
            "count": len(group),
            "excess_count": len(group) - 1,
            "question_ids": [item["question_id"] for item in group],
            "resume_ids": [item["resume_id"] for item in group],
            "questions": [item["question"] for item in group],
        }
        for opening, group in sorted(openings.items())
        if len(group) > 1
    ]
    duplicate_excess = sum(group["excess_count"] for group in duplicate_groups)
    opening_excess = sum(group["excess_count"] for group in opening_groups)
    sample_count = len(rows)
    summary = {
        "schema_version": "cv-question-rag.question-pattern-audit.v1",
        "sample_count": sample_count,
        "normalization": "lowercase ASCII token regex [a-z0-9+#.]+",
        "opening_definition": "first four normalized tokens",
        "rate_denominator": "all generated questions",
        "exact_duplicate_group_count": len(duplicate_groups),
        "exact_duplicate_excess_count": duplicate_excess,
        "normalized_exact_duplicate_rate": (
            duplicate_excess / sample_count if sample_count else 0.0
        ),
        "opening_repetition_group_count": len(opening_groups),
        "opening_repetition_excess_count": opening_excess,
        "opening_phrase_repetition_rate": (
            opening_excess / sample_count if sample_count else 0.0
        ),
        "unsupported_experience_assumption_count": len(assumptions),
        "unsupported_experience_assumption_rate": (
            len(assumptions) / sample_count if sample_count else 0.0
        ),
        "unsupported_assumption_source": (
            "boolean flags frozen in questions.jsonl by the conservative bilingual "
            "pattern audit"
        ),
    }

    _write_jsonl(output_dir / "exact_duplicate_groups.jsonl", duplicate_groups)
    _write_jsonl(output_dir / "opening_repetition_groups.jsonl", opening_groups)
    _write_jsonl(
        output_dir / "unsupported_experience_assumptions.jsonl", assumptions
    )
    _write_json(output_dir / "QUESTION_PATTERN_AUDIT.json", summary)
    return summary

