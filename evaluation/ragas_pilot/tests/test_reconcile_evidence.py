from __future__ import annotations

from pathlib import Path

from evaluation.ragas_pilot.dataset import build_controlled_case_specs
from evaluation.ragas_pilot.reconcile_evidence import reconcile_rag_samples
from evaluation.ragas_pilot.retrieval import evaluate_retrieval_spec


CATALOG_PATH = Path("backend/services/interview_knowledge/catalog.json")


def test_reconcile_repairs_only_domain_scoped_metadata() -> None:
    spec = build_controlled_case_specs(CATALOG_PATH, limit=10)[3]
    original = evaluate_retrieval_spec(spec, CATALOG_PATH)
    original["retrieved_contexts"][2]["topic_id"] = (
        "Data_Scientist::Python Programming::Functions::`**kwargs`"
    )
    original["controlled_reference"].update(
        {"expected_topic_rank": None, "hit_at_8": False, "recall_at_8": 0.0, "mrr_at_8": 0.0}
    )

    rows, corrected_count = reconcile_rag_samples(
        [original], [spec], CATALOG_PATH
    )

    assert corrected_count == 1
    assert rows[0]["controlled_reference"]["expected_topic_rank"] == 1
    assert rows[0]["controlled_reference"]["hit_at_8"] is True
    assert rows[0]["retrieved_contexts"][2]["topic_id"] == spec.expected_topic_id
    assert rows[0]["post_run_corrections"][0]["scope"] == "evaluation_metadata_only"
