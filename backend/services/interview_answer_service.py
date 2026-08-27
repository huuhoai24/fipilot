from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime

from pydantic import ValidationError

from infrastructure.repositories.base import InterviewRepository
from orchestrator.conversation_flow import answer_opening, enter_closing_if_finished
from orchestrator.interview_orchestrator import InterviewOrchestrator, QuestionProvider
from shared.schemas import (
    InterviewMode,
    InterviewSessionState,
    InterviewStatus,
    VoiceAnalytics,
)


class InterviewAnswerSubmissionError(Exception):
    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class InterviewAnswerSubmissionResult:
    state: InterviewSessionState
    started_at: datetime | None
    replayed: bool = False


class InterviewAnswerSubmissionService:
    """Owns the idempotent claim, evaluation, and state transition for an answer."""

    def __init__(
        self,
        *,
        repository: InterviewRepository,
        orchestrator: InterviewOrchestrator,
    ) -> None:
        self.repository = repository
        self.orchestrator = orchestrator

    async def submit_answer(
        self,
        session_id: str,
        user_id: str,
        turn_id: str,
        answer: str,
        *,
        expected_mode: InterviewMode | None = None,
        question_provider: QuestionProvider | None = None,
        voice_analytics: VoiceAnalytics | None = None,
    ) -> InterviewAnswerSubmissionResult:
        normalized_answer = answer.strip()
        if not normalized_answer:
            raise InterviewAnswerSubmissionError(
                "Answer must not be empty.", code="empty_answer"
            )
        normalized_turn_id = turn_id.strip()
        session = self.repository.get_session(session_id, user_id=user_id)
        if session is None:
            raise InterviewAnswerSubmissionError(
                "Interview session not found.", code="session_not_found"
            )
        try:
            state = InterviewSessionState.model_validate(session.state_payload)
        except ValidationError as error:
            raise InterviewAnswerSubmissionError(
                "Interview session is unavailable.", code="invalid_session_state"
            ) from error
        if expected_mode is None:
            expected_mode = state.interview_config.mode
        if state.interview_config.mode != expected_mode:
            raise InterviewAnswerSubmissionError(
                f"Interview session is not configured for {expected_mode.value}.",
                code=f"{expected_mode.value}_mode_required",
            )
        if not normalized_turn_id:
            raise InterviewAnswerSubmissionError(
                "Turn ID must not be empty.", code="invalid_interview_turn"
            )

        answer_hash = hashlib.sha256(normalized_answer.encode("utf-8")).hexdigest()
        existing = self.repository.get_answer_submission(
            session_id, normalized_turn_id, user_id=user_id
        )
        if existing is not None:
            if existing.answer_hash != answer_hash:
                raise InterviewAnswerSubmissionError(
                    "This turn already has a different submitted answer.",
                    code="answer_already_submitted",
                )
            if existing.status == "completed":
                latest = self.repository.get_session(session_id, user_id=user_id)
                latest_state = InterviewSessionState.model_validate(
                    latest.state_payload if latest is not None else session.state_payload
                )
                return InterviewAnswerSubmissionResult(
                    state=latest_state,
                    started_at=(latest or session).started_at,
                    replayed=True,
                )
            raise InterviewAnswerSubmissionError(
                "This answer submission is already being processed.",
                code="answer_submission_in_progress",
            )

        if state.current_turn is None:
            raise InterviewAnswerSubmissionError(
                "There is no active interview question.", code="no_active_turn"
            )
        if state.current_turn.turn_id != normalized_turn_id:
            completed_ids = {turn.turn_id for turn in state.completed_turns}
            code = (
                "stale_interview_turn"
                if normalized_turn_id in completed_ids
                else "invalid_interview_turn"
            )
            raise InterviewAnswerSubmissionError(
                "The submitted turn is not the active interview turn.", code=code
            )

        claim = self.repository.claim_answer_submission(
            session_id,
            normalized_turn_id,
            answer_hash,
            user_id=user_id,
        )
        if claim.outcome != "claimed":
            if claim.outcome == "replay":
                latest = self.repository.get_session(session_id, user_id=user_id)
                latest_state = InterviewSessionState.model_validate(
                    latest.state_payload if latest is not None else session.state_payload
                )
                return InterviewAnswerSubmissionResult(
                    state=latest_state,
                    started_at=(latest or session).started_at,
                    replayed=True,
                )
            code = (
                "answer_already_submitted"
                if claim.outcome == "conflict"
                else "answer_submission_in_progress"
            )
            raise InterviewAnswerSubmissionError(
                "This turn already has an answer submission.", code=code
            )

        try:
            if voice_analytics is not None:
                state = state.model_copy(
                    update={"voice_analytics": voice_analytics.model_copy(deep=True)}
                )
            updated_state = answer_opening(state, normalized_answer)
            if updated_state is None:
                if question_provider is None:
                    updated_state = await self.orchestrator.submit_answer(
                        state, normalized_answer
                    )
                else:
                    updated_state = await self.orchestrator.submit_answer(
                        state,
                        normalized_answer,
                        question_provider=question_provider,
                    )
                if expected_mode == InterviewMode.TEXT:
                    updated_state = enter_closing_if_finished(updated_state)
            saved = self.repository.complete_answer_submission(
                session_id,
                normalized_turn_id,
                answer_hash,
                "INTERVIEWING" if updated_state.current_turn is not None else "ENDED",
                updated_state.model_dump(mode="json"),
                (
                    InterviewStatus.IN_PROGRESS.value
                    if updated_state.current_turn is not None
                    else InterviewStatus.COMPLETED.value
                ),
                user_id=user_id,
            )
            if saved is None:
                raise InterviewAnswerSubmissionError(
                    "Interview session not found.", code="session_not_found"
                )
        except BaseException:
            self.repository.abandon_answer_submission(
                session_id,
                normalized_turn_id,
                answer_hash,
                user_id=user_id,
            )
            raise

        if updated_state.current_turn is not None:
            self.repository.save_turn(
                session_id, updated_state.current_turn, user_id=user_id
            )
        return InterviewAnswerSubmissionResult(
            state=updated_state,
            started_at=session.started_at,
        )
