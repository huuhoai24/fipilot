from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

from shared.schemas.candidate import CandidateProfile
from shared.schemas.evaluation import AnswerEvaluation, DifficultyDecision


class InterviewStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REPORT_GENERATED = "report_generated"

    # Retained so older serialized V2 payloads continue to validate.
    DRAFT = "draft"
    PLANNING = "planning"
    INTERVIEWING = "interviewing"
    EVALUATING = "evaluating"
    FAILED = "failed"


class InterviewMode(str, Enum):
    TEXT = "text"
    VOICE = "voice"


Difficulty = Literal["easy", "medium", "hard"]
QuestionType = Literal["opening", "conceptual", "practical", "project_deep_dive", "system_design", "debugging", "follow_up"]
InterviewPhase = Literal["opening", "interviewing", "closing"]
InterviewLanguage = Literal["vi", "en"]
ExperienceLevel = Literal["intern", "junior", "middle", "senior"]
InterviewStyle = Literal["technical", "behavioral", "mixed"]
InterviewTurnStatus = Literal["created", "answered", "evaluated"]
InterviewerPersonality = Literal[
    "professional",
    "friendly",
    "challenging",
    "supportive",
]


class InterviewConfig(BaseModel):
    mode: InterviewMode = InterviewMode.TEXT
    language: InterviewLanguage = "vi"
    experience_level: ExperienceLevel
    duration_minutes: int = Field(default=30, ge=5, le=180)
    interview_style: InterviewStyle = "technical"
    question_count: int = Field(default=10, ge=1)
    objective: str = "Evaluate technical knowledge and practical experience"
    interviewer_personality: InterviewerPersonality = "professional"


class InterviewRound(BaseModel):
    round_id: str
    topic: str
    objective: str = ""
    difficulty: Difficulty = "medium"
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


class InterviewQuestion(BaseModel):
    question: str
    language: InterviewLanguage
    topic: str
    difficulty: Difficulty
    reasoning: str = ""
    expected_answer_points: list[str] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)


class InterviewTurn(BaseModel):
    turn_id: str
    round_id: str | None = None
    question: InterviewQuestion | str
    answer: str | None = None
    status: InterviewTurnStatus = "created"
    evaluation: AnswerEvaluation | None = None
    question_type: QuestionType = "conceptual"
    difficulty: Difficulty = "medium"
    topic: str = ""
    expected_signal: list[str] = Field(default_factory=list)
    candidate_answer: str | None = None

    def with_evaluation(self, evaluation: AnswerEvaluation) -> "InterviewTurn":
        return self.model_copy(update={"evaluation": evaluation, "status": "evaluated"})


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
    phase: InterviewPhase = "interviewing"
    opening_turn: InterviewTurn | None = None
    pending_turn: InterviewTurn | None = None
    current_turn: InterviewTurn | None = None
    completed_turns: list[InterviewTurn] = Field(default_factory=list)
    current_question_index: int = Field(default=0, ge=0)
    memory: InterviewMemoryState = Field(default_factory=InterviewMemoryState)
    voice_analytics: VoiceAnalytics = Field(default_factory=VoiceAnalytics)


class InterviewSessionSummary(BaseModel):
    session_id: str
    candidate_id: str
    status: InterviewStatus
    mode: InterviewMode = InterviewMode.TEXT
    language: InterviewLanguage
    experience_level: ExperienceLevel
    question_count: int = Field(default=0, ge=0)
    answered_question_count: int = Field(default=0, ge=0)
    overall_score: float | None = Field(default=None, ge=0.0, le=10.0)
    started_at: datetime
    completed_at: datetime | None = None


class InterviewHistoryTurn(BaseModel):
    turn_id: str
    question: str
    answer: str = ""
    topic: str = ""
    difficulty: Difficulty = "medium"
    evaluation: AnswerEvaluation | None = None
    decision: DifficultyDecision | None = None


class InterviewSessionStartRequest(BaseModel):
    candidate_id: str
    domain: str
    target_level: str
    duration_minutes: int = Field(default=30, ge=5, le=180)
    language: Literal["vi", "en"] = "vi"
    job_description: str | None = None


class InterviewSessionStartResponse(BaseModel):
    session_id: str
    status: InterviewStatus
    plan: InterviewPlan
    first_question: InterviewTurn


class AnswerSubmission(BaseModel):
    turn_id: str
    answer: str = Field(min_length=1, max_length=12000)
