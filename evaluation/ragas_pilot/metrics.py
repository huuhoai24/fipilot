from __future__ import annotations

import math
import statistics
from collections.abc import Sequence


RELEVANCE_LABELS = {"relevant", "partially_relevant", "irrelevant"}


def _percentile(values: Sequence[float], percentile: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1 - weight) + ordered[upper] * weight)


def latency_summary(values: Sequence[float]) -> dict[str, float] | None:
    if not values:
        return None
    return {
        "mean_ms": float(statistics.mean(values)),
        "median_ms": float(statistics.median(values)),
        "p95_ms": _percentile(values, 0.95),
        "min_ms": float(min(values)),
        "max_ms": float(max(values)),
    }


def repeatability_summary(score_runs: Sequence[Sequence[float]]) -> dict[str, float | int]:
    if not score_runs:
        return {
            "sample_count": 0,
            "range_le_one_rate": 0.0,
            "mean_score_stddev": 0.0,
        }
    if any(len(scores) < 2 for scores in score_runs):
        raise ValueError("Repeatability requires at least two scores per sample")
    ranges = [max(scores) - min(scores) for scores in score_runs]
    deviations = [statistics.pstdev(scores) for scores in score_runs]
    return {
        "sample_count": len(score_runs),
        "range_le_one_rate": sum(value <= 1.0 for value in ranges) / len(ranges),
        "mean_score_stddev": float(statistics.mean(deviations)),
    }


def is_strictly_monotonic(scores: Sequence[float]) -> bool:
    return len(scores) >= 2 and all(
        earlier < later for earlier, later in zip(scores, scores[1:], strict=False)
    )


def context_precision_without_reference(labels: Sequence[str]) -> float | None:
    """Return AP-style precision from reference-free context judgments.

    Both relevant and partially relevant contexts count as useful for ranking;
    their distinction remains available to the separate relevance-score metric.
    """

    if not labels:
        return None
    unknown = set(labels) - RELEVANCE_LABELS
    if unknown:
        raise ValueError(f"Unknown relevance labels: {sorted(unknown)}")

    relevant_count = 0
    precision_sum = 0.0
    for rank, label in enumerate(labels, start=1):
        if label == "irrelevant":
            continue
        relevant_count += 1
        precision_sum += relevant_count / rank
    return precision_sum / relevant_count if relevant_count else 0.0
