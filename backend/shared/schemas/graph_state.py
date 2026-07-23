"""Compatibility graph state schemas.

The refactor intentionally does not add LangGraph; these contracts are kept so
older imports continue to resolve while orchestrator.state is the active state
boundary.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from shared.schemas.candidate import CandidateProfile
from shared.schemas.evaluation import AnswerEvaluation
from shared.schemas.interview import InterviewSessionState
from shared.schemas.job import JobRequirements
from shared.schemas.report import FinalReport


class RAGChunk(BaseModel):
    chunk_id: str
    source: str = ""
    domain: str = ""
    topic: str = ""
    content: str
    score: float = Field(default=0.0, ge=0.0)


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
    candidate_profile: CandidateProfile | None = None
    job_requirements: JobRequirements | None = None
    session_state: InterviewSessionState | None = None
    retrieved_context: list[RAGChunk] = Field(default_factory=list)
    memory: MemoryState = Field(default_factory=MemoryState)
    last_evaluation: AnswerEvaluation | None = None
    final_report: FinalReport | None = None
    errors: list[GraphError] = Field(default_factory=list)
