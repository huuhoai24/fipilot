from __future__ import annotations

from pathlib import Path

from evaluation.ragas_pilot.dataset import build_controlled_case_specs
from evaluation.ragas_pilot.retrieval import evaluate_retrieval_spec


CATALOG_PATH = Path("backend/services/interview_knowledge/catalog.json")


def test_controlled_retrieval_uses_production_retriever_and_catalog_ids() -> None:
    spec = build_controlled_case_specs(CATALOG_PATH, limit=1)[0]

    sample = evaluate_retrieval_spec(spec, CATALOG_PATH)

    topic_contexts = [
        context
        for context in sample["retrieved_contexts"]
        if context["context_type"] == "topic"
    ]
    assert sample["retrieval_implementation"] == "LocalKnowledgeRetriever"
    assert sample["similarity_metric"] == "weighted_lexical_token_overlap"
    assert all(context["similarity"] is None for context in topic_contexts)
    assert spec.expected_topic_id in {
        context["topic_id"] for context in topic_contexts
    }
    assert sample["controlled_reference"]["hit_at_8"] is True


def test_topic_ids_are_resolved_within_the_selected_domain() -> None:
    specs = build_controlled_case_specs(CATALOG_PATH, limit=10)
    duplicate_context_specs = [specs[3], specs[6]]

    for spec in duplicate_context_specs:
        sample = evaluate_retrieval_spec(spec, CATALOG_PATH)

        assert sample["controlled_reference"]["expected_topic_rank"] == 1
        assert sample["controlled_reference"]["hit_at_8"] is True
        assert spec.expected_topic_id in {
            context["topic_id"] for context in sample["retrieved_contexts"]
        }
