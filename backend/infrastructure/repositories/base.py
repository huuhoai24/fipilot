from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    FinalReport,
    InterviewReport,
    InterviewSessionSummary,
    InterviewTurn,
    PersistedCandidateProfile,
)


class CandidateRecord(BaseModel):
    candidate_id: str
    user_id: str | None = None
    name: str | None = None
    profile: CandidateProfile | None = None
    raw_resume_text: str | None = None


class InterviewSessionRecord(BaseModel):
    session_id: str
    candidate_id: str
    user_id: str | None = None
    status: str = "created"
    state: str = "GREETING"
    role: str | None = None
    level: str | None = None
    language: str = "vi"
    state_payload: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    report_id: str | None = None


class CandidateRepository(ABC):
    @abstractmethod
    def create_candidate(
        self, name: str | None = None, *, user_id: str | None = None
    ) -> CandidateRecord:
        raise NotImplementedError

    @abstractmethod
    def get_candidate(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> CandidateRecord | None:
        raise NotImplementedError

    @abstractmethod
    def save_candidate_profile(
        self, candidate_id: str, profile: CandidateProfile, *, user_id: str | None = None
    ) -> CandidateProfile | None:
        raise NotImplementedError

    @abstractmethod
    def get_candidate_profile(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> PersistedCandidateProfile | None:
        raise NotImplementedError

    @abstractmethod
    def save_candidate_resume_text(
        self, candidate_id: str, resume_text: str, *, user_id: str | None = None
    ) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def get_candidate_resume_text(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> str | None:
        raise NotImplementedError

    def update_candidate_profile(
        self, candidate_id: str, profile: CandidateProfile, *, user_id: str | None = None
    ) -> CandidateProfile | None:
        return self.save_candidate_profile(candidate_id, profile, user_id=user_id)


class InterviewSessionRepository(ABC):
    @abstractmethod
    def create_session(
        self,
        candidate_id: str,
        role: str | None = None,
        level: str | None = None,
        language: str = "vi",
        user_id: str | None = None,
    ) -> InterviewSessionRecord:
        raise NotImplementedError

    @abstractmethod
    def get_session(
        self, session_id: str, *, user_id: str | None = None
    ) -> InterviewSessionRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update_session_state(
        self,
        session_id: str,
        state: str,
        state_payload: dict[str, Any] | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ) -> InterviewSessionRecord | None:
        raise NotImplementedError

    @abstractmethod
    def update_session_status(
        self,
        session_id: str,
        status: str,
        report_id: str | None = None,
        user_id: str | None = None,
    ) -> InterviewSessionRecord | None:
        raise NotImplementedError

    @abstractmethod
    def list_interview_sessions(
        self,
        candidate_id: str | None,
        limit: int,
        offset: int,
        user_id: str | None = None,
    ) -> list[InterviewSessionSummary]:
        raise NotImplementedError

    @abstractmethod
    def count_interview_sessions(
        self, candidate_id: str | None = None, *, user_id: str | None = None
    ) -> int:
        raise NotImplementedError


class InterviewTurnRepository(ABC):
    @abstractmethod
    def save_turn(
        self, session_id: str, turn: InterviewTurn, *, user_id: str | None = None
    ) -> InterviewTurn:
        raise NotImplementedError

    @abstractmethod
    def get_turns(
        self, session_id: str, *, user_id: str | None = None
    ) -> list[InterviewTurn]:
        raise NotImplementedError


class EvaluationRepository(ABC):
    @abstractmethod
    def save_evaluation(
        self,
        session_id: str,
        evaluation: AnswerEvaluation,
        question_id: int | None = None,
        answer_id: int | None = None,
        user_id: str | None = None,
    ) -> AnswerEvaluation:
        raise NotImplementedError


class ReportRepository(ABC):
    @abstractmethod
    def save_interview_report(
        self, report: InterviewReport, *, user_id: str | None = None
    ) -> InterviewReport:
        raise NotImplementedError

    @abstractmethod
    def get_interview_report(
        self, session_id: str, *, user_id: str | None = None
    ) -> InterviewReport | None:
        raise NotImplementedError

    @abstractmethod
    def save_report(
        self, session_id: str, report: FinalReport, *, user_id: str | None = None
    ) -> FinalReport:
        raise NotImplementedError

    @abstractmethod
    def get_report(
        self, session_id: str, *, user_id: str | None = None
    ) -> FinalReport | None:
        raise NotImplementedError


class InterviewRepository(
    CandidateRepository,
    InterviewSessionRepository,
    InterviewTurnRepository,
    EvaluationRepository,
    ReportRepository,
    ABC,
):
    pass
