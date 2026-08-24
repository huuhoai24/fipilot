from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class CandidateProject(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)
    role: str | None = None


class CandidateExperience(BaseModel):
    company: str = ""
    title: str = ""
    start_date: str | None = None
    end_date: str | None = None
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class CandidateEducation(BaseModel):
    institution: str = ""
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class SkillEvidence(BaseModel):
    skill: str = ""
    evidence: list[str] = Field(default_factory=list)
    source_section: str | None = None


class CandidateProfile(BaseModel):
    candidate_id: str | None = None
    name: str = "Candidate"
    years_experience: float | None = None
    recent_role: str | None = None
    skills: list[str] = Field(default_factory=list)
    skill_evidence: list[SkillEvidence] = Field(default_factory=list)
    projects: list[CandidateProject] = Field(default_factory=list)
    experiences: list[CandidateExperience] = Field(default_factory=list)
    education: str | list[CandidateEducation] | None = None
    specialization: str | None = None
    seniority_signal: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_method: str | None = None

    @model_validator(mode="before")
    @classmethod
    def keep_confidence_fields_compatible(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "confidence" not in data and "confidence_score" in data:
                data["confidence"] = data["confidence_score"]
            elif "confidence_score" not in data and "confidence" in data:
                data["confidence_score"] = data["confidence"]
        return data


class InterviewMode(str, Enum):
    TEXT = "text"
    VOICE = "voice"


class InterviewConfig(BaseModel):
    mode: InterviewMode = InterviewMode.TEXT
    language: Literal["vi", "en"] = "vi"
    experience_level: Literal["intern", "junior", "middle", "senior"]
    duration_minutes: int = Field(default=30, ge=5, le=180)
    interview_style: Literal["technical", "behavioral", "mixed"] = "technical"
    question_count: int = Field(default=10, ge=1)
    objective: str = "Evaluate technical knowledge and practical experience"
    interviewer_personality: Literal[
        "professional", "friendly", "challenging", "supportive"
    ] = "professional"


class InterviewRound(BaseModel):
    round_id: str
    topic: str
    objective: str = ""
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    reasoning: str = ""
    recommended_question_areas: list[str] = Field(default_factory=list)
    weight: float = Field(default=0.0, ge=0.0, le=1.0)
    target_skills: list[str] = Field(default_factory=list)
    question_budget: int = Field(default=1, ge=1)


class InterviewPlan(BaseModel):
    duration_minutes: int = Field(default=30, ge=5, le=180)
    rounds: list[InterviewRound] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def keep_rounds_compatible(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "rounds" not in data and "interview_rounds" in data:
                data["rounds"] = data["interview_rounds"]
        return data


class PlannerInput(BaseModel):
    candidate_profile: CandidateProfile
    interview_config: InterviewConfig
    knowledge_topics: list[str] = Field(default_factory=list)
