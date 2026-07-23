from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from infrastructure.repositories.base import CandidateRecord, InterviewRepository, InterviewSessionRecord
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    FinalReport,
    InterviewReport,
    InterviewSessionState,
    InterviewSessionSummary,
    InterviewStatus,
    InterviewTurn,
)


class FirestoreRepository(InterviewRepository):
    """Firestore adapter using paths scoped under users/{user_id}."""

    def __init__(
        self,
        client: Any,
        *,
        users_collection: str = "users",
        candidates_collection: str = "candidates",
        interviews_collection: str = "interviews",
    ) -> None:
        self.client = client
        self.users_collection = users_collection
        self.candidates_collection = candidates_collection
        self.interviews_collection = interviews_collection

    def save_candidate(
        self,
        user_id: str,
        candidate_profile: CandidateProfile,
        *,
        candidate_id: str | None = None,
        raw_resume_text: str | None = None,
    ) -> CandidateRecord:
        owner_id = self._require_user_id(user_id)
        self._ensure_user_document(owner_id)
        reference = self._candidate_collection(owner_id).document(candidate_id)
        now = self._now()
        payload = {
            "candidate_id": reference.id,
            "name": candidate_profile.name,
            "profile": candidate_profile.model_dump(mode="json"),
            "raw_resume_text": raw_resume_text,
            "updated_at": now,
        }
        snapshot = reference.get()
        if not snapshot.exists:
            payload["created_at"] = now
        reference.set(payload, merge=True)
        return self.get_candidate(reference.id, user_id=owner_id)

    def create_candidate(
        self, name: str | None = None, *, user_id: str | None = None
    ) -> CandidateRecord:
        owner_id = self._require_user_id(user_id)
        return self.save_candidate(
            owner_id,
            CandidateProfile(name=name or "Candidate"),
        )

    def get_candidate(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> CandidateRecord | None:
        owner_id = self._require_user_id(user_id)
        snapshot = self._candidate_collection(owner_id).document(candidate_id).get()
        if not snapshot.exists:
            return None
        data = snapshot.to_dict() or {}
        profile_data = data.get("profile")
        profile = CandidateProfile.model_validate(profile_data) if profile_data else None
        return CandidateRecord(
            candidate_id=snapshot.id,
            user_id=owner_id,
            name=data.get("name"),
            profile=profile,
            raw_resume_text=data.get("raw_resume_text"),
        )

    def save_candidate_profile(
        self,
        candidate_id: str,
        profile: CandidateProfile,
        *,
        user_id: str | None = None,
    ) -> CandidateProfile | None:
        owner_id = self._require_user_id(user_id)
        reference = self._candidate_collection(owner_id).document(candidate_id)
        if not reference.get().exists:
            return None
        reference.set(
            {
                "name": profile.name,
                "profile": profile.model_dump(mode="json"),
                "updated_at": self._now(),
            },
            merge=True,
        )
        return profile

    def get_candidate_profile(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> CandidateProfile | None:
        candidate = self.get_candidate(candidate_id, user_id=user_id)
        return candidate.profile if candidate is not None else None

    def save_candidate_resume_text(
        self,
        candidate_id: str,
        resume_text: str,
        *,
        user_id: str | None = None,
    ) -> str | None:
        owner_id = self._require_user_id(user_id)
        reference = self._candidate_collection(owner_id).document(candidate_id)
        if not reference.get().exists:
            return None
        reference.set(
            {"raw_resume_text": resume_text, "updated_at": self._now()},
            merge=True,
        )
        return resume_text

    def get_candidate_resume_text(
        self, candidate_id: str, *, user_id: str | None = None
    ) -> str | None:
        candidate = self.get_candidate(candidate_id, user_id=user_id)
        return candidate.raw_resume_text if candidate is not None else None

    def save_interview_session(
        self,
        user_id: str,
        session_id: str,
        state: InterviewSessionState,
    ) -> InterviewSessionRecord:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(session_id)
        snapshot = reference.get()
        existing = snapshot.to_dict() if snapshot.exists else {}
        candidate_id = existing.get("candidate_id") or state.candidate_profile.candidate_id or ""
        status = (
            InterviewStatus.IN_PROGRESS.value
            if state.current_turn is not None
            else InterviewStatus.COMPLETED.value
        )
        now = self._now()
        payload = {
            "session_id": session_id,
            "candidate_id": candidate_id,
            "status": status,
            "state": "INTERVIEWING" if state.current_turn is not None else "ENDED",
            "state_payload": state.model_dump(mode="json"),
            "mode": state.interview_config.mode.value,
            "language": state.interview_config.language,
            "level": state.interview_config.experience_level,
            "updated_at": now,
        }
        if not snapshot.exists:
            self._ensure_user_document(owner_id)
            payload["started_at"] = now
        if status == InterviewStatus.COMPLETED.value:
            payload["completed_at"] = existing.get("completed_at") or now
        reference.set(payload, merge=True)
        return self.get_session(session_id, user_id=owner_id)

    def create_session(
        self,
        candidate_id: str,
        role: str | None = None,
        level: str | None = None,
        language: str = "vi",
        user_id: str | None = None,
    ) -> InterviewSessionRecord:
        owner_id = self._require_user_id(user_id)
        if self.get_candidate(candidate_id, user_id=owner_id) is None:
            raise ValueError(f"Candidate {candidate_id} does not exist for this user")
        self._ensure_user_document(owner_id)
        reference = self._interview_collection(owner_id).document()
        now = self._now()
        reference.set(
            {
                "session_id": reference.id,
                "candidate_id": candidate_id,
                "status": InterviewStatus.CREATED.value,
                "state": "GREETING",
                "role": role,
                "level": level,
                "language": language,
                "state_payload": {},
                "turns": [],
                "evaluations": [],
                "started_at": now,
                "updated_at": now,
            }
        )
        return self.get_session(reference.id, user_id=owner_id)

    def get_interview_session(
        self, session_id: str, user_id: str
    ) -> InterviewSessionRecord | None:
        return self.get_session(session_id, user_id=user_id)

    def get_session(
        self, session_id: str, *, user_id: str | None = None
    ) -> InterviewSessionRecord | None:
        owner_id = self._require_user_id(user_id)
        snapshot = self._interview_collection(owner_id).document(session_id).get()
        if not snapshot.exists:
            return None
        return self._session_from_data(snapshot.id, owner_id, snapshot.to_dict() or {})

    def update_session_state(
        self,
        session_id: str,
        state: str,
        state_payload: dict[str, Any] | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ) -> InterviewSessionRecord | None:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(session_id)
        snapshot = reference.get()
        if not snapshot.exists:
            return None
        normalized_status = self._normalize_status(
            status
            or (
                InterviewStatus.COMPLETED.value
                if state in {"ENDED", InterviewStatus.COMPLETED.value}
                else InterviewStatus.IN_PROGRESS.value
            ),
            has_report=bool((snapshot.to_dict() or {}).get("report")),
        )
        payload: dict[str, Any] = {
            "state": state,
            "status": normalized_status,
            "updated_at": self._now(),
        }
        if state_payload is not None:
            payload["state_payload"] = state_payload
            config_payload = state_payload.get("interview_config")
            if isinstance(config_payload, dict) and config_payload.get("mode") in {
                "text",
                "voice",
            }:
                payload["mode"] = config_payload["mode"]
        if normalized_status in {
            InterviewStatus.COMPLETED.value,
            InterviewStatus.REPORT_GENERATED.value,
        }:
            payload["completed_at"] = (snapshot.to_dict() or {}).get(
                "completed_at"
            ) or self._now()
        reference.set(payload, merge=True)
        return self.get_session(session_id, user_id=owner_id)

    def update_session_status(
        self,
        session_id: str,
        status: str,
        report_id: str | None = None,
        user_id: str | None = None,
    ) -> InterviewSessionRecord | None:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(session_id)
        snapshot = reference.get()
        if not snapshot.exists:
            return None
        normalized_status = self._normalize_status(status)
        payload: dict[str, Any] = {
            "status": normalized_status,
            "updated_at": self._now(),
        }
        if report_id is not None:
            payload["report_id"] = report_id
        if normalized_status in {
            InterviewStatus.COMPLETED.value,
            InterviewStatus.REPORT_GENERATED.value,
        }:
            payload["completed_at"] = (snapshot.to_dict() or {}).get(
                "completed_at"
            ) or self._now()
        reference.set(payload, merge=True)
        return self.get_session(session_id, user_id=owner_id)

    def list_interview_sessions(
        self,
        candidate_id: str | None,
        limit: int,
        offset: int,
        user_id: str | None = None,
    ) -> list[InterviewSessionSummary]:
        owner_id = self._require_user_id(user_id)
        summaries: list[InterviewSessionSummary] = []
        for snapshot in self._interview_collection(owner_id).stream():
            data = snapshot.to_dict() or {}
            if candidate_id is not None and data.get("candidate_id") != candidate_id:
                continue
            summaries.append(self._summary_from_data(snapshot.id, data))
        summaries.sort(key=lambda item: item.started_at, reverse=True)
        return summaries[offset : offset + limit]

    def count_interview_sessions(
        self, candidate_id: str | None = None, *, user_id: str | None = None
    ) -> int:
        owner_id = self._require_user_id(user_id)
        return sum(
            1
            for snapshot in self._interview_collection(owner_id).stream()
            if candidate_id is None
            or (snapshot.to_dict() or {}).get("candidate_id") == candidate_id
        )

    def save_turn(
        self, session_id: str, turn: InterviewTurn, *, user_id: str | None = None
    ) -> InterviewTurn:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(session_id)
        snapshot = reference.get()
        if not snapshot.exists:
            raise ValueError(f"Session {session_id} does not exist for this user")
        data = snapshot.to_dict() or {}
        turns = list(data.get("turns") or [])
        turns.append(turn.model_dump(mode="json"))
        reference.set({"turns": turns, "updated_at": self._now()}, merge=True)
        return turn

    def get_turns(
        self, session_id: str, *, user_id: str | None = None
    ) -> list[InterviewTurn]:
        owner_id = self._require_user_id(user_id)
        snapshot = self._interview_collection(owner_id).document(session_id).get()
        if not snapshot.exists:
            return []
        turns = (snapshot.to_dict() or {}).get("turns") or []
        return [InterviewTurn.model_validate(turn) for turn in turns]

    def save_evaluation(
        self,
        session_id: str,
        evaluation: AnswerEvaluation,
        question_id: int | None = None,
        answer_id: int | None = None,
        user_id: str | None = None,
    ) -> AnswerEvaluation:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(session_id)
        snapshot = reference.get()
        if not snapshot.exists:
            raise ValueError(f"Session {session_id} does not exist for this user")
        data = snapshot.to_dict() or {}
        evaluations = list(data.get("evaluations") or [])
        evaluations.append(evaluation.model_dump(mode="json"))
        reference.set(
            {"evaluations": evaluations, "updated_at": self._now()}, merge=True
        )
        return evaluation

    def save_interview_report(
        self, report: InterviewReport, *, user_id: str | None = None
    ) -> InterviewReport:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(report.session_id)
        snapshot = reference.get()
        if not snapshot.exists:
            raise ValueError(f"Session {report.session_id} does not exist for this user")
        existing_data = (snapshot.to_dict() or {}).get("report")
        if existing_data:
            return InterviewReport.model_validate(existing_data)
        reference.set(
            {
                "report": report.model_dump(mode="json"),
                "report_id": report.id,
                "status": InterviewStatus.REPORT_GENERATED.value,
                "completed_at": (snapshot.to_dict() or {}).get("completed_at")
                or self._now(),
                "updated_at": self._now(),
            },
            merge=True,
        )
        return report

    def get_interview_report(
        self, session_id: str, *, user_id: str | None = None
    ) -> InterviewReport | None:
        owner_id = self._require_user_id(user_id)
        snapshot = self._interview_collection(owner_id).document(session_id).get()
        if not snapshot.exists:
            return None
        report_data = (snapshot.to_dict() or {}).get("report")
        return InterviewReport.model_validate(report_data) if report_data else None

    def save_report(
        self,
        session_id: str,
        report: FinalReport,
        *,
        user_id: str | None = None,
    ) -> FinalReport:
        owner_id = self._require_user_id(user_id)
        reference = self._interview_collection(owner_id).document(session_id)
        if not reference.get().exists:
            raise ValueError(f"Session {session_id} does not exist for this user")
        reference.set(
            {"legacy_report": report.model_dump(mode="json"), "updated_at": self._now()},
            merge=True,
        )
        return report

    def get_report(
        self, session_id: str, *, user_id: str | None = None
    ) -> FinalReport | None:
        owner_id = self._require_user_id(user_id)
        snapshot = self._interview_collection(owner_id).document(session_id).get()
        if not snapshot.exists:
            return None
        report_data = (snapshot.to_dict() or {}).get("legacy_report")
        return FinalReport.model_validate(report_data) if report_data else None

    def check_ready(self) -> bool:
        next(iter(self.client.collection(self.users_collection).limit(1).stream()), None)
        return True

    def _ensure_user_document(self, user_id: str) -> None:
        self._user_document(user_id).set(
            {"user_id": user_id, "updated_at": self._now()}, merge=True
        )

    def _user_document(self, user_id: str) -> Any:
        return self.client.collection(self.users_collection).document(user_id)

    def _candidate_collection(self, user_id: str) -> Any:
        return self._user_document(user_id).collection(self.candidates_collection)

    def _interview_collection(self, user_id: str) -> Any:
        return self._user_document(user_id).collection(self.interviews_collection)

    def _session_from_data(
        self, session_id: str, user_id: str, data: dict[str, Any]
    ) -> InterviewSessionRecord:
        return InterviewSessionRecord(
            session_id=session_id,
            candidate_id=str(data.get("candidate_id") or ""),
            user_id=user_id,
            status=self._normalize_status(
                data.get("status"), has_report=bool(data.get("report"))
            ),
            state=data.get("state") or "GREETING",
            role=data.get("role"),
            level=data.get("level"),
            language=data.get("language") or "vi",
            state_payload=self._dict_value(data.get("state_payload")),
            started_at=self._datetime_value(data.get("started_at")),
            completed_at=self._datetime_value(data.get("completed_at"), required=False),
            report_id=data.get("report_id"),
        )

    def _summary_from_data(
        self, session_id: str, data: dict[str, Any]
    ) -> InterviewSessionSummary:
        state_payload = self._dict_value(data.get("state_payload"))
        question_count = 0
        answered_count = 0
        language = self._normalize_language(data.get("language"))
        experience_level = self._normalize_level(data.get("level"))
        if state_payload:
            try:
                state = InterviewSessionState.model_validate(state_payload)
                question_count = state.interview_config.question_count
                answered_count = len(state.completed_turns)
                language = state.interview_config.language
                experience_level = state.interview_config.experience_level
            except ValueError:
                pass
        report_data = data.get("report")
        overall_score = None
        if report_data:
            try:
                overall_score = InterviewReport.model_validate(report_data).overall_score
            except ValueError:
                pass
        return InterviewSessionSummary(
            session_id=session_id,
            candidate_id=str(data.get("candidate_id") or ""),
            status=self._normalize_status(
                data.get("status"), has_report=bool(report_data)
            ),
            language=language,
            experience_level=experience_level,
            question_count=question_count,
            answered_question_count=answered_count,
            overall_score=overall_score,
            started_at=self._datetime_value(data.get("started_at")),
            completed_at=self._datetime_value(data.get("completed_at"), required=False),
        )

    @staticmethod
    def _require_user_id(user_id: str | None) -> str:
        if not user_id or not user_id.strip():
            raise ValueError("user_id is required for Firestore repository operations")
        return user_id

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
    def _dict_value(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return {}
            return parsed if isinstance(parsed, dict) else {}
        return {}

    @staticmethod
    def _datetime_value(value: Any, *, required: bool = True) -> datetime | None:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                pass
        return datetime.now(timezone.utc) if required else None

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
