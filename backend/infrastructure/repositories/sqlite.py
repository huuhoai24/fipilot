from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import inspect, or_, text
from sqlalchemy.orm import Session

import crud
import models
from infrastructure.repositories.base import CandidateRecord, InterviewRepository, InterviewSessionRecord
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    FinalReport,
    InterviewReport,
    InterviewMode,
    InterviewSessionState,
    InterviewSessionSummary,
    InterviewStatus,
    InterviewTurn,
    PersistedCandidateProfile,
)


class SQLiteInterviewRepository(InterviewRepository):
    def __init__(
        self,
        db: Session,
        *,
        auth_enabled: bool = False,
        dev_user_id: str = "local-development-user",
    ) -> None:
        self.db = db
        self.auth_enabled = auth_enabled
        self.dev_user_id = dev_user_id
        self._ensure_schema_columns()

    def create_candidate(
        self, name: str | None = None, *, user_id: str | None = None
    ) -> CandidateRecord:
        owner_id = self._resolve_user_id(user_id)
        candidate = crud.create_user(self.db, name or "Candidate", user_id=owner_id)
        return self._candidate_from_model(candidate)

    def get_candidate(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> CandidateRecord | None:
        candidate = self._get_candidate_model(candidate_id, user_id)
        return self._candidate_from_model(candidate) if candidate is not None else None

    def save_candidate_profile(
        self,
        candidate_id: str,
        profile: CandidateProfile,
        *,
        user_id: str | None = None,
    ) -> CandidateProfile | None:
        candidate = self._get_candidate_model(candidate_id, user_id)
        if candidate is None:
            return None
        if profile.name:
            candidate.name = profile.name
        candidate.profile_json = profile.model_dump_json()
        self.db.commit()
        self.db.refresh(candidate)
        return profile

    def get_candidate_profile(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> PersistedCandidateProfile | None:
        candidate = self._get_candidate_model(candidate_id, user_id)
        if candidate is None or not candidate.profile_json:
            return None
        profile = CandidateProfile.model_validate_json(candidate.profile_json)
        return PersistedCandidateProfile(
            **profile.model_dump(exclude={"candidate_id"}),
            candidate_id=str(candidate.id),
            profile_version=candidate.profile_version,
        )

    def save_candidate_resume_text(
        self,
        candidate_id: str,
        resume_text: str,
        *,
        user_id: str | None = None,
    ) -> str | None:
        candidate = self._get_candidate_model(candidate_id, user_id)
        if candidate is None:
            return None
        candidate.raw_resume_text = resume_text
        self.db.commit()
        self.db.refresh(candidate)
        return resume_text

    def get_candidate_resume_text(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> str | None:
        candidate = self._get_candidate_model(candidate_id, user_id)
        return candidate.raw_resume_text if candidate is not None else None

    def create_session(
        self,
        candidate_id: str,
        role: str | None = None,
        level: str | None = None,
        language: str = "vi",
        user_id: str | None = None,
    ) -> InterviewSessionRecord:
        owner_id = self._resolve_user_id(user_id)
        candidate = self._get_candidate_model(candidate_id, owner_id)
        if candidate is None:
            raise ValueError(f"Candidate {candidate_id} does not exist for this user")

        session = crud.create_session(
            self.db,
            self._int_id(candidate_id),
            user_id=owner_id,
        )
        session.role = role
        session.level = level
        session.language = language
        session.status = InterviewStatus.CREATED.value
        session.candidate_name = candidate.name
        self.db.commit()
        self.db.refresh(session)
        return self._session_from_model(session)

    def get_session(
        self, session_id: str, *, user_id: str | None = None
    ) -> InterviewSessionRecord | None:
        session = self._get_session_model(session_id, user_id)
        return self._session_from_model(session) if session is not None else None

    def update_session_state(
        self,
        session_id: str,
        state: str,
        state_payload: dict[str, Any] | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ) -> InterviewSessionRecord | None:
        session = self._get_session_model(session_id, user_id)
        if session is None:
            return None
        session.state = state
        if status is not None:
            session.status = self._normalize_status(status)
        elif state in {"INTERVIEWING", InterviewStatus.IN_PROGRESS.value}:
            session.status = InterviewStatus.IN_PROGRESS.value
        elif state in {"ENDED", InterviewStatus.COMPLETED.value}:
            session.status = InterviewStatus.COMPLETED.value
        if session.status in {
            InterviewStatus.COMPLETED.value,
            InterviewStatus.REPORT_GENERATED.value,
        } and session.completed_at is None:
            session.completed_at = datetime.now(timezone.utc)
        if state_payload is not None:
            session.question_plan_json = json.dumps(state_payload)
        self.db.commit()
        self.db.refresh(session)
        return self._session_from_model(session)

    def update_session_status(
        self,
        session_id: str,
        status: str,
        report_id: str | None = None,
        user_id: str | None = None,
    ) -> InterviewSessionRecord | None:
        session = self._get_session_model(session_id, user_id)
        if session is None:
            return None
        session.status = self._normalize_status(status)
        if report_id is not None:
            session.report_id = report_id
        if session.status in {
            InterviewStatus.COMPLETED.value,
            InterviewStatus.REPORT_GENERATED.value,
        } and session.completed_at is None:
            session.completed_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(session)
        return self._session_from_model(session)

    def list_interview_sessions(
        self,
        candidate_id: str | None,
        limit: int,
        offset: int,
        user_id: str | None = None,
    ) -> list[InterviewSessionSummary]:
        owner_id = self._resolve_user_id(user_id)
        query = self.db.query(models.Session).filter(
            self._ownership_clause(models.Session.user_id, owner_id)
        )
        if candidate_id is not None:
            query = query.filter(models.Session.candidate_id == self._int_id(candidate_id))
        sessions = (
            query.order_by(models.Session.created_at.desc(), models.Session.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [self._session_summary_from_model(session) for session in sessions]

    def count_interview_sessions(
        self, candidate_id: str | None = None, *, user_id: str | None = None
    ) -> int:
        owner_id = self._resolve_user_id(user_id)
        query = self.db.query(models.Session).filter(
            self._ownership_clause(models.Session.user_id, owner_id)
        )
        if candidate_id is not None:
            query = query.filter(models.Session.candidate_id == self._int_id(candidate_id))
        return query.count()

    def save_turn(
        self, session_id: str, turn: InterviewTurn, *, user_id: str | None = None
    ) -> InterviewTurn:
        if self._get_session_model(session_id, user_id) is None:
            raise ValueError(f"Session {session_id} does not exist for this user")
        crud.create_message(
            self.db,
            session_id=self._int_id(session_id),
            role="turn",
            content=turn.model_dump_json(),
        )
        return turn

    def get_turns(
        self, session_id: str, *, user_id: str | None = None
    ) -> list[InterviewTurn]:
        owner_id = self._resolve_user_id(user_id)
        messages = (
            self.db.query(models.Message)
            .join(models.Session, models.Message.session_id == models.Session.id)
            .filter(
                models.Message.session_id == self._int_id(session_id),
                models.Message.role == "turn",
                self._ownership_clause(models.Session.user_id, owner_id),
            )
            .order_by(models.Message.created_at, models.Message.id)
            .all()
        )
        turns: list[InterviewTurn] = []
        for message in messages:
            try:
                turns.append(InterviewTurn.model_validate_json(message.content))
            except ValueError:
                continue
        return turns

    def save_evaluation(
        self,
        session_id: str,
        evaluation: AnswerEvaluation,
        question_id: int | None = None,
        answer_id: int | None = None,
        user_id: str | None = None,
    ) -> AnswerEvaluation:
        if self._get_session_model(session_id, user_id) is None:
            raise ValueError(f"Session {session_id} does not exist for this user")
        turn_message = self._get_turn_message(session_id, evaluation.turn_id, user_id)
        fallback_message_id = turn_message.id if turn_message is not None else None
        score = int(round(evaluation.scores.overall_score))
        crud.create_evaluation(
            self.db,
            session_id=self._int_id(session_id),
            question_id=question_id or fallback_message_id or 0,
            answer_id=answer_id or fallback_message_id or 0,
            correctness=self._correctness_from_score(score),
            score=score,
            explanation=evaluation.feedback,
            rubric_json=evaluation.model_dump_json(),
        )
        return evaluation

    def save_report(
        self,
        session_id: str,
        report: FinalReport,
        *,
        user_id: str | None = None,
    ) -> FinalReport:
        session = self._get_session_model(session_id, user_id)
        if session is None:
            raise ValueError(f"Session {session_id} does not exist for this user")
        session.report_data = report.model_dump_json()
        self.db.commit()
        self.db.refresh(session)
        return report

    def get_report(
        self, session_id: str, *, user_id: str | None = None
    ) -> FinalReport | None:
        session = self._get_session_model(session_id, user_id)
        if session is None or not session.report_data:
            return None
        try:
            return FinalReport.model_validate_json(session.report_data)
        except ValueError:
            return None

    def save_interview_report(
        self, report: InterviewReport, *, user_id: str | None = None
    ) -> InterviewReport:
        session = self._get_session_model(report.session_id, user_id)
        if session is None:
            raise ValueError(f"Session {report.session_id} does not exist for this user")
        session.report_data = report.model_dump_json()
        session.report_id = report.id
        self.db.commit()
        self.db.refresh(session)
        return report

    def get_interview_report(
        self, session_id: str, *, user_id: str | None = None
    ) -> InterviewReport | None:
        session = self._get_session_model(session_id, user_id)
        if session is None or not session.report_data:
            return None
        try:
            return InterviewReport.model_validate_json(session.report_data)
        except ValueError:
            return None

    def _get_candidate_model(
        self, candidate_id: str, user_id: str | None
    ) -> models.User | None:
        owner_id = self._resolve_user_id(user_id)
        return (
            self.db.query(models.User)
            .filter(
                models.User.id == self._int_id(candidate_id),
                self._ownership_clause(models.User.user_id, owner_id),
            )
            .first()
        )

    def _get_session_model(
        self, session_id: str, user_id: str | None
    ) -> models.Session | None:
        owner_id = self._resolve_user_id(user_id)
        return (
            self.db.query(models.Session)
            .filter(
                models.Session.id == self._int_id(session_id),
                self._ownership_clause(models.Session.user_id, owner_id),
            )
            .first()
        )

    def _candidate_from_model(self, candidate: models.User) -> CandidateRecord:
        profile = (
            CandidateProfile.model_validate_json(candidate.profile_json)
            if candidate.profile_json
            else None
        )
        return CandidateRecord(
            candidate_id=str(candidate.id),
            user_id=candidate.user_id,
            name=candidate.name,
            profile=profile,
            raw_resume_text=candidate.raw_resume_text,
        )

    def _ensure_schema_columns(self) -> None:
        bind = self.db.get_bind()
        if bind is None or bind.dialect.name != "sqlite":
            return

        inspector = inspect(bind)
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        for column_name, column_type in {
            "user_id": "VARCHAR",
            "profile_json": "TEXT",
            "profile_version": "INTEGER NOT NULL DEFAULT 1",
            "raw_resume_text": "TEXT",
        }.items():
            if column_name not in user_columns:
                self.db.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))

        session_columns = {column["name"] for column in inspector.get_columns("sessions")}
        if "candidate_id" not in session_columns and "user_id" in session_columns:
            self.db.execute(text("ALTER TABLE sessions RENAME COLUMN user_id TO candidate_id"))
            self.db.commit()
            inspector = inspect(bind)
            session_columns = {
                column["name"] for column in inspector.get_columns("sessions")
            }

        for column_name, column_type in {
            "candidate_id": "INTEGER",
            "user_id": "VARCHAR",
            "completed_at": "DATETIME",
            "report_id": "VARCHAR",
            "report_data": "TEXT",
        }.items():
            if column_name not in session_columns:
                self.db.execute(
                    text(f"ALTER TABLE sessions ADD COLUMN {column_name} {column_type}")
                )

        for index in inspect(bind).get_indexes("sessions"):
            if (
                index["name"] == "ix_sessions_user_id"
                and index.get("column_names") != ["user_id"]
            ):
                self.db.execute(text("DROP INDEX ix_sessions_user_id"))
        self.db.execute(text("CREATE INDEX IF NOT EXISTS ix_users_user_id ON users (user_id)"))
        self.db.execute(
            text("CREATE INDEX IF NOT EXISTS ix_sessions_user_id ON sessions (user_id)")
        )
        self.db.commit()

    def _session_from_model(self, session: models.Session) -> InterviewSessionRecord:
        return InterviewSessionRecord(
            session_id=str(session.id),
            candidate_id=str(session.candidate_id),
            user_id=session.user_id,
            status=self._normalize_status(session.status, has_report=bool(session.report_data)),
            state=session.state,
            role=session.role,
            level=session.level,
            language=session.language,
            state_payload=self._loads_json_object(session.question_plan_json),
            started_at=session.created_at,
            completed_at=session.completed_at,
            report_id=session.report_id,
        )

    def _session_summary_from_model(self, session: models.Session) -> InterviewSessionSummary:
        payload = self._loads_json_object(session.question_plan_json)
        question_count = session.question_count or 0
        answered_count = 0
        mode = InterviewMode.TEXT
        language = self._normalize_language(session.language)
        experience_level = self._normalize_level(session.level)
        if payload:
            try:
                state = InterviewSessionState.model_validate(payload)
                question_count = state.interview_config.question_count
                answered_count = len(state.completed_turns)
                mode = state.interview_config.mode
                language = state.interview_config.language
                experience_level = state.interview_config.experience_level
            except ValueError:
                pass

        overall_score: float | None = None
        if session.report_data:
            try:
                overall_score = InterviewReport.model_validate_json(
                    session.report_data
                ).overall_score
            except ValueError:
                try:
                    overall_score = FinalReport.model_validate_json(
                        session.report_data
                    ).overall_score
                except ValueError:
                    pass

        return InterviewSessionSummary(
            session_id=str(session.id),
            candidate_id=str(session.candidate_id),
            status=self._normalize_status(session.status, has_report=bool(session.report_data)),
            mode=mode,
            language=language,
            experience_level=experience_level,
            question_count=question_count,
            answered_question_count=answered_count,
            overall_score=overall_score,
            started_at=session.created_at or datetime.now(timezone.utc),
            completed_at=session.completed_at,
        )

    def _get_turn_message(
        self, session_id: str, turn_id: str, user_id: str | None
    ) -> models.Message | None:
        owner_id = self._resolve_user_id(user_id)
        messages = (
            self.db.query(models.Message)
            .join(models.Session, models.Message.session_id == models.Session.id)
            .filter(
                models.Message.session_id == self._int_id(session_id),
                models.Message.role == "turn",
                self._ownership_clause(models.Session.user_id, owner_id),
            )
            .order_by(models.Message.created_at.desc(), models.Message.id.desc())
            .all()
        )
        for message in messages:
            try:
                turn = InterviewTurn.model_validate_json(message.content)
            except ValueError:
                continue
            if turn.turn_id == turn_id:
                return message
        return None

    def _resolve_user_id(self, user_id: str | None) -> str:
        if user_id:
            return user_id
        if not self.auth_enabled:
            return self.dev_user_id
        raise ValueError("user_id is required when authentication is enabled")

    def _ownership_clause(self, column: Any, user_id: str) -> Any:
        owned = column == user_id
        if not self.auth_enabled and user_id == self.dev_user_id:
            return or_(owned, column.is_(None))
        return owned

    @staticmethod
    def _correctness_from_score(score: int) -> str:
        if score >= 8:
            return "Correct"
        if score >= 4:
            return "Partial"
        return "Wrong"

    @staticmethod
    def _loads_json_object(value: str | None) -> dict[str, Any]:
        if not value:
            return {}
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}

    @staticmethod
    def _normalize_status(value: str | None, *, has_report: bool = False) -> str:
        if has_report:
            return InterviewStatus.REPORT_GENERATED.value
        normalized = (value or "").strip().lower()
        if normalized in {"ended", "completed"}:
            return InterviewStatus.COMPLETED.value
        if normalized in {"interviewing", "evaluating", "in_progress"}:
            return InterviewStatus.IN_PROGRESS.value
        if normalized == "report_generated":
            return InterviewStatus.REPORT_GENERATED.value
        return InterviewStatus.CREATED.value

    @staticmethod
    def _normalize_language(value: str | None) -> str:
        return "en" if (value or "").lower() == "en" else "vi"

    @staticmethod
    def _normalize_level(value: str | None) -> str:
        normalized = (value or "junior").strip().lower()
        aliases = {"fresher": "intern", "mid": "middle", "mid-level": "middle"}
        normalized = aliases.get(normalized, normalized)
        return normalized if normalized in {"intern", "junior", "middle", "senior"} else "junior"

    @staticmethod
    def _int_id(value: str | int) -> int:
        return int(value)
