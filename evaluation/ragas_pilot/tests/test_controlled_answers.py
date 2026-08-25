from __future__ import annotations

from evaluation.ragas_pilot.answers import build_controlled_answers


def test_controlled_answers_have_ordinal_intent_without_human_scores() -> None:
    answers = build_controlled_answers(
        expected_points=["authentication flow", "token validation", "failure handling"],
        language="en",
    )

    assert [answer["quality_tier"] for answer in answers] == [
        "weak",
        "partial",
        "good",
        "strong",
    ]
    assert all(answer["source_type"] == "synthetic_controlled" for answer in answers)
    assert all("human_score" not in answer for answer in answers)
    assert all(answer["quality_ladder_validated"] is False for answer in answers)
    assert len({answer["answer"] for answer in answers}) == 4
