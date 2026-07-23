"""Repository adapters."""

from infrastructure.repositories.base import (
    CandidateRecord,
    CandidateRepository,
    EvaluationRepository,
    InterviewRepository,
    InterviewSessionRecord,
    InterviewSessionRepository,
    InterviewTurnRepository,
    ReportRepository,
)
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from infrastructure.repositories.firestore import FirestoreRepository

__all__ = [
    "CandidateRecord",
    "CandidateRepository",
    "EvaluationRepository",
    "InterviewRepository",
    "InterviewSessionRecord",
    "InterviewSessionRepository",
    "InterviewTurnRepository",
    "FirestoreRepository",
    "ReportRepository",
    "SQLiteInterviewRepository",
]
