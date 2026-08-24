from __future__ import annotations

from datetime import datetime, timezone
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


class InterviewTurn(BaseModel):
    turn_id: str
    round_id: str | None = None
    question: InterviewQuestion | str
    answer: str | None = None
    status: Literal["created", "answered", "evaluated"] = "created"
    evaluation: AnswerEvaluation | None = None
    question_type: Literal["opening", "conceptual", "practical", "project_deep_dive", "system_design", "debugging", "follow_up"] = "conceptual"
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    topic: str = ""
    expected_signal: list[str] = Field(default_factory=list)
    candidate_answer: str | None = None


class InterviewMemoryState(BaseModel):
    previous_topics: list[str] = Field(default_factory=list)
    covered_skills: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    follow_up_points: list[str] = Field(default_factory=list)


class VoiceAnalytics(BaseModel):
    speaking_duration_ms: float = Field(default=0.0, ge=0.0)
    response_latencies_ms: list[float] = Field(default_factory=list)
    interruption_count: int = Field(default=0, ge=0)


class InterviewSessionState(BaseModel):
    candidate_profile: CandidateProfile
    interview_config: InterviewConfig
    interview_plan: InterviewPlan
    phase: Literal["opening", "interviewing", "closing"] = "interviewing"
    opening_turn: InterviewTurn | None = None
    pending_turn: InterviewTurn | None = None
    current_turn: InterviewTurn | None = None
    completed_turns: list[InterviewTurn] = Field(default_factory=list)
    current_question_index: int = Field(default=0, ge=0)
    memory: InterviewMemoryState = Field(default_factory=InterviewMemoryState)
    voice_analytics: VoiceAnalytics = Field(default_factory=VoiceAnalytics)


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


class ReportInput(BaseModel):
    candidate_profile: CandidateProfile
    interview_state: InterviewSessionState
