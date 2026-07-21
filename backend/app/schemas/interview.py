from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.evaluation import AnswerEvaluation, DifficultyDecision


InterviewStatus = Literal["draft", "planning", "interviewing", "evaluating", "completed", "failed"]
Difficulty = Literal["easy", "medium", "hard"]
QuestionType = Literal["conceptual", "practical", "project_deep_dive", "system_design", "debugging", "follow_up"]


class InterviewRound(BaseModel):
    round_id: str
    topic: str
    objective: str = ""
    difficulty: Difficulty = "medium"
    weight: float = Field(default=0.0, ge=0.0, le=1.0)
    target_skills: list[str] = Field(default_factory=list)
    question_budget: int = Field(default=1, ge=1)


class InterviewPlan(BaseModel):
    duration_minutes: int = Field(default=30, ge=5, le=180)
    rounds: list[InterviewRound] = Field(default_factory=list)
    coverage_goals: list[str] = Field(default_factory=list)
    risk_areas: list[str] = Field(default_factory=list)


class InterviewTurn(BaseModel):
    turn_id: str
    round_id: str | None = None
    question: str
    question_type: QuestionType = "conceptual"
    difficulty: Difficulty = "medium"
    topic: str
    expected_signal: list[str] = Field(default_factory=list)
    candidate_answer: str | None = None


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

