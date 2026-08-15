from __future__ import annotations

import statistics
from typing import Any

from evaluation.ragas_pilot.metrics import latency_summary, repeatability_summary


def _mean(values: list[float]) -> float | None:
    return float(statistics.mean(values)) if values else None


def _completed(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if row.get("status") == "completed"]


def _judge_disagreement_rate(rows: list[dict[str, Any]]) -> float | None:
    repeated = [row.get("judge_votes") for row in rows if len(row.get("judge_votes", [])) >= 2]
    if not repeated:
        return None
    disagreements = 0
    for votes in repeated:
        normalized = []
        for vote in votes:
            if "context_judgments" in vote:
                normalized.append(
                    [
                        (value["rank"], value["label"], value["relevance_score"])
                        for value in sorted(
                            vote["context_judgments"], key=lambda item: item["rank"]
                        )
                    ]
                )
            elif "judgments" in vote:
                normalized.append(
                    [
                        {
                            key: value
                            for key, value in item.items()
                            if key != "reasons"
                        }
                        for item in sorted(
                            vote["judgments"], key=lambda item: item["quality_tier"]
                        )
                    ]
                )
            else:
                normalized.append(
                    {
                        key: value
                        for key, value in vote.items()
                        if key != "judge_reasons"
                    }
                )
        if any(value != normalized[0] for value in normalized[1:]):
            disagreements += 1
    return disagreements / len(repeated)


def summarize_rag_samples(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed = _completed(rows)
    metrics = [row["metrics"] for row in completed]
    controlled = [row["controlled_reference"] for row in rows]
    empty_count = sum(not row.get("retrieved_contexts") for row in rows)
    return {
        "evaluation_set": "synthetic controlled evaluation set",
        "sample_count": len(rows),
        "successful_count": len(completed),
        "failure_count": len(rows) - len(completed),
        "ragas_inspired_context_precision_without_reference": _mean(
            [value["context_precision_without_reference"] for value in metrics]
        ),
        "mean_context_relevance": _mean(
            [value["mean_context_relevance"] for value in metrics]
        ),
        "relevant_at_k_rate": _mean([value["relevant_at_k_rate"] for value in metrics]),
        "irrelevant_at_k_rate": _mean(
            [value["irrelevant_at_k_rate"] for value in metrics]
        ),
        "empty_retrieval_rate": empty_count / len(rows) if rows else None,
        "retrieval_latency": latency_summary(
            [float(row["latency_ms"]) for row in rows]
        ),
        "controlled_retrieval": {
            "classification": "synthetic controlled retrieval test",
            "hit_rate_at_8": _mean(
                [1.0 if value["hit_at_8"] else 0.0 for value in controlled]
            ),
            "recall_at_8": _mean([value["recall_at_8"] for value in controlled]),
            "mrr_at_8": _mean([value["mrr_at_8"] for value in controlled]),
        },
        "context_recall": None,
        "context_recall_reason": (
            "No human-reviewed reference contexts or reference answers are available "
            "in this pilot."
        ),
        "judge_repeated_sample_count": sum(
            len(row.get("judge_votes", [])) >= 2 for row in rows
        ),
        "judge_disagreement_rate": _judge_disagreement_rate(rows),
        "evidence_classification": {
            "latency_and_empty_rate": "A",
            "reference_free_relevance": "B/C",
            "controlled_hit_recall_mrr": "A/C",
        },
    }


def summarize_question_samples(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed = _completed(rows)
    values = [row["metrics"] for row in completed]
    return {
        "evaluation_set": "synthetic controlled evaluation set",
        "sample_count": len(rows),
        "successful_count": len(completed),
        "failure_count": len(rows) - len(completed),
        "role_relevance_pass_rate": _mean([value["role_relevance"] for value in values]),
        "cv_alignment_pass_rate": _mean([value["cv_alignment"] for value in values]),
        "technical_validity_pass_rate": _mean(
            [value["technical_validity"] for value in values]
        ),
        "hallucinated_candidate_claim_rate": _mean(
            [value["hallucinated_candidate_claim"] for value in values]
        ),
        "mean_rag_grounding": _mean([value["rag_grounding"] for value in values]),
        "mean_difficulty_alignment": _mean(
            [value["difficulty_alignment"] for value in values]
        ),
        "mean_clarity": _mean([value["clarity"] for value in values]),
        "generation_latency": latency_summary(
            [float(row["generation_latency_ms"]) for row in completed]
        ),
        "judge_repeated_sample_count": sum(
            len(row.get("judge_votes", [])) >= 2 for row in rows
        ),
        "judge_disagreement_rate": _judge_disagreement_rate(rows),
        "evidence_classification": "B/C",
    }


def summarize_answer_samples(rows: list[dict[str, Any]]) -> dict[str, Any]:
    completed = _completed(rows)
    metrics = [row["judge_metrics"] for row in completed if row.get("judge_metrics")]
    group_metrics: dict[str, dict[str, Any]] = {}
    group_ladder_validity: dict[str, bool] = {}
    for row in completed:
        if row.get("group_metrics"):
            group_metrics[row["group_id"]] = row["group_metrics"]
        group_id = row.get("group_id")
        if group_id:
            group_ladder_validity[group_id] = group_ladder_validity.get(
                group_id, True
            ) and bool(row.get("quality_ladder_validated", False))
    repeat_runs = [
        row["repeatability"]["scores"]
        for row in completed
        if row.get("repeatability")
    ]
    raw_monotonicity = _mean(
        [
            1.0 if value["strict_monotonic"] else 0.0
            for value in group_metrics.values()
        ]
    )
    validated_group_metrics = [
        value
        for group_id, value in group_metrics.items()
        if group_ladder_validity.get(group_id, False)
    ]
    validated_group_count = len(validated_group_metrics)
    total_metric_groups = len(group_metrics)
    validation_status = (
        "valid"
        if total_metric_groups > 0 and validated_group_count == total_metric_groups
        else "partial"
        if validated_group_count > 0
        else "invalid"
    )
    return {
        "evaluation_set": "synthetic controlled evaluation set",
        "sample_count": len(rows),
        "successful_count": len(completed),
        "failure_count": len(rows) - len(completed),
        "group_count": len({row.get("group_id") for row in rows}),
        "controlled_monotonicity_rate": _mean(
            [
                1.0 if value["strict_monotonic"] else 0.0
                for value in validated_group_metrics
            ]
        ),
        "raw_observed_monotonicity_rate": raw_monotonicity,
        "controlled_answer_set_validation": {
            "status": validation_status,
            "validated_group_count": validated_group_count,
            "total_group_count": total_metric_groups,
            "reason": (
                "The deterministic answer templates describe expected points at a "
                "meta level instead of supplying verified progressively stronger "
                "technical answers. Raw ordering is retained for audit but is not a "
                "defensible evaluator monotonicity metric."
                if validation_status != "valid"
                else "All controlled answer quality ladders were independently validated."
            ),
        },
        "mean_rubric_adherence": _mean(
            [value["rubric_adherence"] for value in metrics]
        ),
        "evidence_grounding_pass_rate": _mean(
            [value["evidence_grounding"] for value in metrics]
        ),
        "unsupported_feedback_rate": _mean(
            [value["unsupported_feedback"] for value in metrics]
        ),
        "mean_feedback_actionability": _mean(
            [value["feedback_actionability"] for value in metrics]
        ),
        "mean_score_feedback_consistency": _mean(
            [value["score_feedback_consistency"] for value in metrics]
        ),
        "repeatability": repeatability_summary(repeat_runs),
        "judge_repeated_group_count": sum(
            len(row.get("judge_votes", [])) >= 2
            for row in rows
            if row.get("quality_tier") == "good"
        ),
        "judge_disagreement_rate": _judge_disagreement_rate(
            [row for row in rows if row.get("quality_tier") == "good"]
        ),
        "human_mae": None,
        "human_correlation": None,
        "human_metrics_reason": "No verified human-labelled benchmark is available.",
        "evidence_classification": {
            "controlled_monotonicity": (
                "A/C" if validation_status == "valid" else "NOT EVALUATED"
            ),
            "repeatability": "A/C",
            "feedback_rubrics": "B/C",
        },
    }
