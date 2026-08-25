from __future__ import annotations

from evaluation.ragas_pilot.summaries import summarize_answer_samples


def test_answer_summary_reports_controlled_metrics_without_human_claims() -> None:
    rows = []
    for tier, score in zip(
        ["weak", "partial", "good", "strong"],
        [1.0, 4.0, 7.0, 9.0],
        strict=True,
    ):
        rows.append(
            {
                "status": "completed",
                "group_id": "answer-group-001",
                "quality_tier": tier,
                "quality_ladder_validated": True,
                "evaluation": {"overall_score": score},
                "judge_metrics": {
                    "rubric_adherence": 4,
                    "evidence_grounding": 1,
                    "unsupported_feedback": 0,
                    "feedback_actionability": 4,
                    "score_feedback_consistency": 5,
                },
                "group_metrics": {"strict_monotonic": True},
                "repeatability": (
                    {"scores": [7.0, 7.5, 7.0]} if tier == "good" else None
                ),
            }
        )

    summary = summarize_answer_samples(rows)

    assert summary["controlled_monotonicity_rate"] == 1.0
    assert summary["evidence_grounding_pass_rate"] == 1.0
    assert summary["unsupported_feedback_rate"] == 0.0
    assert summary["repeatability"]["range_le_one_rate"] == 1.0
    assert summary["human_mae"] is None
    assert summary["human_correlation"] is None


def test_answer_summary_suppresses_monotonicity_for_unvalidated_ladder() -> None:
    rows = [
        {
            "status": "completed",
            "group_id": "answer-group-001",
            "quality_tier": tier,
            "group_metrics": {"strict_monotonic": False},
            "judge_metrics": {},
        }
        for tier in ["weak", "partial", "good", "strong"]
    ]

    summary = summarize_answer_samples(rows)

    assert summary["controlled_monotonicity_rate"] is None
    assert summary["raw_observed_monotonicity_rate"] == 0.0
    assert summary["controlled_answer_set_validation"]["status"] == "invalid"
    assert (
        summary["evidence_classification"]["controlled_monotonicity"]
        == "NOT EVALUATED"
    )
