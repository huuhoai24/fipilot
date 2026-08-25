from __future__ import annotations

import pytest

from evaluation.ragas_pilot.evidence_io import read_jsonl, write_jsonl
from evaluation.ragas_pilot.metrics import (
    context_precision_without_reference,
    is_strictly_monotonic,
    latency_summary,
    repeatability_summary,
)


def test_context_precision_rewards_useful_contexts_ranked_early() -> None:
    score = context_precision_without_reference(
        ["relevant", "irrelevant", "relevant"]
    )

    assert score == pytest.approx(5 / 6)


def test_monotonicity_requires_every_quality_tier_to_score_higher() -> None:
    assert is_strictly_monotonic([1.0, 4.0, 7.0, 9.0]) is True
    assert is_strictly_monotonic([1.0, 4.0, 4.0, 9.0]) is False


def test_jsonl_evidence_preserves_every_sample(tmp_path) -> None:
    path = tmp_path / "samples.jsonl"
    samples = [
        {"sample_id": "rag-001", "query": "FastAPI authentication"},
        {"sample_id": "rag-002", "query": "Kubernetes rollout"},
    ]

    write_jsonl(path, samples)

    assert read_jsonl(path) == samples


def test_latency_summary_uses_linear_p95() -> None:
    assert latency_summary([10.0, 20.0, 30.0, 40.0]) == {
        "mean_ms": 25.0,
        "median_ms": 25.0,
        "p95_ms": 38.5,
        "min_ms": 10.0,
        "max_ms": 40.0,
    }


def test_repeatability_reports_range_threshold_and_population_stddev() -> None:
    summary = repeatability_summary([[7.0, 8.0, 7.0], [4.0, 6.0, 5.0]])

    assert summary["sample_count"] == 2
    assert summary["range_le_one_rate"] == 0.5
    assert summary["mean_score_stddev"] == pytest.approx(0.64395, abs=0.00001)
