"""Shared Pydantic schemas for the V2 architecture."""

from app.schemas.candidate import CandidateProfile, CandidateProject, ResumeUploadResult
from app.schemas.evaluation import AnswerEvaluation, DifficultyDecision, EvaluationScore
from app.schemas.graph_state import GraphError, InterviewGraphState, MemoryState, RAGChunk
from app.schemas.interview import (
    AnswerSubmission,
    InterviewHistoryTurn,
    InterviewPlan,
    InterviewRound,
    InterviewSessionStartRequest,
    InterviewSessionStartResponse,
    InterviewStatus,
    InterviewTurn,
)
from app.schemas.job import JobAnalysisResult, JobRequirements
from app.schemas.report import FinalReport, TopicScore

__all__ = [
    "AnswerEvaluation",
    "AnswerSubmission",
    "CandidateProfile",
    "CandidateProject",
    "DifficultyDecision",
    "EvaluationScore",
    "FinalReport",
    "GraphError",
    "InterviewGraphState",
    "InterviewHistoryTurn",
    "InterviewPlan",
    "InterviewRound",
    "InterviewSessionStartRequest",
    "InterviewSessionStartResponse",
    "InterviewStatus",
    "InterviewTurn",
    "JobAnalysisResult",
    "JobRequirements",
    "MemoryState",
    "RAGChunk",
    "ResumeUploadResult",
    "TopicScore",
]

