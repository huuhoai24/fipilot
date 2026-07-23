from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class EvaluationScore(BaseModel):
    technical_score: float = Field(default=0.0, ge=0.0, le=10.0)
    depth_score: float = Field(default=0.0, ge=0.0, le=10.0)
    communication_score: float = Field(default=0.0, ge=0.0, le=10.0)
    engineering_mindset_score: float = Field(default=0.0, ge=0.0, le=10.0)
    overall_score: float = Field(default=0.0, ge=0.0, le=10.0)


class AnswerEvaluation(BaseModel):
    turn_id: str
    scores: EvaluationScore = Field(default_factory=EvaluationScore)
    overall_score: float = Field(default=0.0, ge=0.0, le=10.0)
    technical_score: float = Field(default=0.0, ge=0.0, le=10.0)
    communication_score: float = Field(default=0.0, ge=0.0, le=10.0)
    correctness_score: float = Field(default=0.0, ge=0.0, le=10.0)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_topics: list[str] = Field(default_factory=list)
    missing_concepts: list[str] = Field(default_factory=list)
    feedback: str = ""
    follow_up_needed: bool = False
    follow_up_reason: str | None = None


class DifficultyDecision(BaseModel):
    next_action: Literal[
        "follow_up",
        "next_topic",
        "increase_difficulty",
        "decrease_difficulty",
        "end",
    ] = "next_topic"
    reason: str = ""
    next_topic: str | None = None
    next_difficulty: Literal["easy", "medium", "hard"] | None = None
