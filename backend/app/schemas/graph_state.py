from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.candidate import CandidateProfile
from app.schemas.evaluation import AnswerEvaluation
from app.schemas.interview import InterviewHistoryTurn, InterviewPlan, InterviewStatus, InterviewTurn
from app.schemas.job import JobRequirements
from app.schemas.report import FinalReport


class RAGChunk(BaseModel):
    chunk_id: str
    source: str = ""
    domain: str = ""
    topic: str = ""
    content: str
    score: float = Field(default=0.0, ge=0.0)


class SkillLevel(BaseModel):
    skill: str
    category: str = ""
    estimated_level: Literal["basic", "intermediate", "advanced"] = "basic"
    evidence: str = ""


class SkillMap(BaseModel):
    primary_domain: str = ""
    secondary_domains: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    skill_levels: list[SkillLevel] = Field(default_factory=list)


class MemoryState(BaseModel):
    summary: str = ""
    observed_strengths: list[str] = Field(default_factory=list)
    observed_weaknesses: list[str] = Field(default_factory=list)
    covered_topics: list[str] = Field(default_factory=list)
    uncovered_topics: list[str] = Field(default_factory=list)
    follow_up_targets: list[str] = Field(default_factory=list)


class GraphError(BaseModel):
    agent: str
    message: str
    recoverable: bool = True


class InterviewGraphState(BaseModel):
    session_id: str | None = None
    candidate_id: str | None = None
    job_id: str | None = None
    domain: str | None = None
    target_level: str | None = None
    language: Literal["vi", "en"] = "vi"
    status: InterviewStatus = "draft"

    resume_text: str = ""
    job_description_text: str | None = None
    candidate_profile: CandidateProfile | None = None
    job_requirements: JobRequirements | None = None
    skill_map: SkillMap = Field(default_factory=SkillMap)
    interview_plan: InterviewPlan | None = None
    retrieved_context: list[RAGChunk] = Field(default_factory=list)

    current_turn: InterviewTurn | None = None
    history: list[InterviewHistoryTurn] = Field(default_factory=list)
    memory: MemoryState = Field(default_factory=MemoryState)
    last_evaluation: AnswerEvaluation | None = None
    final_report: FinalReport | None = None
    errors: list[GraphError] = Field(default_factory=list)

