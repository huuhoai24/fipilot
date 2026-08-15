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
    interviewer_personality: Literal["professional", "friendly", "challenging", "supportive"] = "professional"


class InterviewQuestion(BaseModel):
    question: str
    language: Literal["vi", "en"]
    topic: str
    difficulty: Literal["easy", "medium", "hard"]
    reasoning: str = ""
    expected_answer_points: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)


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


class EvaluatorInput(BaseModel):
    candidate_profile: CandidateProfile
    interview_question: InterviewQuestion
    answer: str
    interview_config: InterviewConfig
