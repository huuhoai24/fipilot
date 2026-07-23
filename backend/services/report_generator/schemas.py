from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class HiringRecommendation(str, Enum):
    STRONG_HIRE = "strong_hire"
    HIRE = "hire"
    CONSIDER = "consider"
    NO_HIRE = "no_hire"


class SkillAssessment(BaseModel):
    skill: str
    score: float = Field(ge=0.0, le=10.0)
    evidence: list[str] = Field(default_factory=list)
    feedback: str


class LearningPlanItem(BaseModel):
    topic: str
    priority: str
    reason: str
    recommended_action: str


class InterviewReport(BaseModel):
    id: str = ""
    session_id: str = ""
    overall_score: float = Field(ge=0.0, le=10.0)
    technical_score: float = Field(ge=0.0, le=10.0)
    communication_score: float = Field(ge=0.0, le=10.0)
    correctness_score: float = Field(ge=0.0, le=10.0)
    summary: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    demonstrated_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    skill_assessments: list[SkillAssessment] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    learning_plan: list[LearningPlanItem] = Field(default_factory=list)
    hiring_recommendation: HiringRecommendation
    confidence_score: float = Field(ge=0.0, le=1.0)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


__all__ = [
    "HiringRecommendation",
    "InterviewReport",
    "LearningPlanItem",
    "SkillAssessment",
]
