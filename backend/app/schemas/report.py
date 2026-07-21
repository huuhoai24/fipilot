from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class TopicScore(BaseModel):
    topic: str
    score: float = Field(default=0.0, ge=0.0, le=10.0)
    evidence: list[str] = Field(default_factory=list)


class FinalReport(BaseModel):
    session_id: str
    candidate_id: str | None = None
    overall_score: float = Field(default=0.0, ge=0.0, le=10.0)
    recommendation: Literal["strong_hire", "hire", "consider", "reject"] = "consider"
    summary: str = ""
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    topic_scores: list[TopicScore] = Field(default_factory=list)
    learning_plan: list[str] = Field(default_factory=list)

