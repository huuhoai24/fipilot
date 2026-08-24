from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class GeneratedQuestion(BaseModel):
    question: str
    language: Literal["en", "vi"]
    topic: str
    difficulty: Literal["easy", "medium", "hard"]
    reasoning: str = ""
    expected_answer_points: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)


class QualityJudgment(BaseModel):
    technical_validity: Literal[0, 1]
    role_relevance: Literal[0, 1]
    cv_alignment: Literal[0, 1]
    difficulty_label: Literal["Intern", "Junior", "Middle", "Senior"]
    difficulty_score: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    specificity: int = Field(ge=0, le=2)
    rag_grounding: int | None = Field(default=None, ge=0, le=2)
    answerability: Literal[0, 1]
    non_redundancy: Literal[0, 1]
    knowledge_false_premise: Literal[0, 1]
    grounding_chunk_ids: list[str] = Field(default_factory=list)
    reasons: dict[str, str] = Field(default_factory=dict)

