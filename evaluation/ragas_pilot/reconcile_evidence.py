from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluation.ragas_pilot.dataset import (
    ControlledCaseSpec,
    build_controlled_case_specs,
)
from evaluation.ragas_pilot.evidence_io import read_jsonl, write_jsonl
from evaluation.ragas_pilot.retrieval import evaluate_retrieval_spec
from evaluation.ragas_pilot.summaries import (
    summarize_answer_samples,
    summarize_rag_samples,
)


def reconcile_rag_samples(
    rows: list[dict[str, Any]],
    specs: list[ControlledCaseSpec],
    catalog_path: Path,
) -> tuple[list[dict[str, Any]], int]:
    if len(rows) != len(specs):
        raise ValueError("RAG sample/spec counts must match")
    reconciled: list[dict[str, Any]] = []
    corrected_count = 0
    for row, spec in zip(rows, specs, strict=True):
        expected_sample_id = "rag-" + spec.sample_id.removeprefix("pilot-")
        if row.get("sample_id") != expected_sample_id:
            raise ValueError("RAG sample/spec ordering does not match")
        deterministic = evaluate_retrieval_spec(spec, catalog_path)
        current_text = [item["text"] for item in row["retrieved_contexts"]]
        deterministic_text = [
            item["text"] for item in deterministic["retrieved_contexts"]
        ]
        if current_text != deterministic_text:
            raise ValueError("Retrieval output changed; refusing metadata-only repair")

        updated = deepcopy(row)
        old_reference = deepcopy(updated["controlled_reference"])
        old_topic_ids = [item["topic_id"] for item in updated["retrieved_contexts"]]
        new_topic_ids = [
            item["topic_id"] for item in deterministic["retrieved_contexts"]
        ]
        updated["controlled_reference"] = deterministic["controlled_reference"]
        for current, corrected in zip(
            updated["retrieved_contexts"],
            deterministic["retrieved_contexts"],
            strict=True,
        ):
            current["topic_id"] = corrected["topic_id"]
        if old_reference != updated["controlled_reference"] or old_topic_ids != new_topic_ids:
            corrected_count += 1
            updated.setdefault("post_run_corrections", []).append(
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "scope": "evaluation_metadata_only",
                    "fields": [
                        "retrieved_contexts.topic_id",
                        "controlled_reference",
                    ],
                    "reason": (
                        "Resolve duplicate catalog context text within the selected "
                        "domain; retrieval text, order, latency, and judge votes unchanged."
                    ),
                    "previous_controlled_reference": old_reference,
                }
            )
        reconciled.append(updated)
    return reconciled, corrected_count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconcile deterministic RAG metadata without model calls."
    )
    parser.add_argument(
        "--output-root", type=Path, default=Path("evaluation/ragas_pilot")
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("backend/services/interview_knowledge/catalog.json"),
    )
    args = parser.parse_args()
    sample_path = args.output_root / "rag" / "samples.jsonl"
    rows = read_jsonl(sample_path)
    specs = build_controlled_case_specs(args.catalog, limit=len(rows))
    reconciled, corrected_count = reconcile_rag_samples(rows, specs, args.catalog)
    write_jsonl(sample_path, reconciled)
    summary = summarize_rag_samples(reconciled)
    (args.output_root / "rag" / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    manifest_path = args.output_root / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    corrections = manifest.setdefault("post_run_corrections", [])
    if corrected_count:
        corrections.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "scope": "evaluation_metadata_only",
                "corrected_sample_count": corrected_count,
                "model_calls": 0,
                "production_behavior_changed": False,
                "reason": "Domain-scoped catalog topic-ID resolution for duplicate context text.",
            }
        )

    answer_rows = read_jsonl(args.output_root / "answer_evaluation" / "samples.jsonl")
    answer_summary = summarize_answer_samples(answer_rows)
    (args.output_root / "answer_evaluation" / "summary.json").write_text(
        json.dumps(answer_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["answer_evaluation_controlled_set_validation"] = answer_summary[
        "controlled_answer_set_validation"
    ]
    manifest["status"] = "smoke_completed_with_limitations"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Reconciled {corrected_count} RAG samples; "
        "reviewed answer ladder; model calls: 0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
