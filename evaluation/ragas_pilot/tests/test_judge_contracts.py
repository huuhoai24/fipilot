from __future__ import annotations

import pytest
from pydantic import ValidationError

from evaluation.ragas_pilot.judges import QuestionJudgeOutput


def test_grounded_question_judgment_requires_context_citation() -> None:
    with pytest.raises(ValidationError):
        QuestionJudgeOutput(
            role_relevance=1,
            cv_alignment=1,
            rag_grounding=2,
            difficulty_alignment=4,
            technical_validity=1,
            clarity=5,
            hallucinated_candidate_claim=0,
            grounding_context_ranks=[],
            judge_reasons={"rag_grounding": "Grounded but no citation supplied."},
        )
