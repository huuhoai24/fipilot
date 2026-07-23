from __future__ import annotations

from pydantic import ValidationError

from infrastructure.repositories.base import InterviewRepository
from orchestrator.interview_orchestrator import InterviewOrchestrator, QuestionProvider
from shared.schemas import (
    InterviewMode,
    InterviewSessionState,
    InterviewStatus,
    VoiceAnalytics,
)


class VoiceAnswerSubmissionError(Exception):
    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


class VoiceAnswerSubmissionService:
    """Submits a reviewed transcript through the existing interview workflow."""

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
        answer: str,
        *,
        question_provider: QuestionProvider | None = None,
        voice_analytics: VoiceAnalytics | None = None,
    ) -> InterviewSessionState:
        normalized_answer = answer.strip()
        if not normalized_answer:
            raise VoiceAnswerSubmissionError(
                "Answer must not be empty.",
                code="empty_answer",
            )

        session = self.repository.get_session(session_id, user_id=user_id)
        if session is None:
            raise VoiceAnswerSubmissionError(
                "Interview session not found.",
                code="session_not_found",
            )

        try:
            state = InterviewSessionState.model_validate(session.state_payload)
        except ValidationError as error:
            raise VoiceAnswerSubmissionError(
                "Interview session is unavailable.",
                code="invalid_session_state",
            ) from error

        if state.interview_config.mode != InterviewMode.VOICE:
            raise VoiceAnswerSubmissionError(
                "Interview session is not configured for voice.",
                code="voice_mode_required",
            )
        if state.current_turn is None:
            raise VoiceAnswerSubmissionError(
                "There is no active interview question.",
                code="no_active_turn",
            )
        if voice_analytics is not None:
            state = state.model_copy(
                update={"voice_analytics": voice_analytics.model_copy(deep=True)}
            )

        updated_state = await self.orchestrator.submit_answer(
            state,
            normalized_answer,
            question_provider=question_provider,
        )
        saved_session = self.repository.update_session_state(
            session_id,
            "INTERVIEWING" if updated_state.current_turn is not None else "ENDED",
            updated_state.model_dump(mode="json"),
            status=(
                InterviewStatus.IN_PROGRESS.value
                if updated_state.current_turn is not None
                else InterviewStatus.COMPLETED.value
            ),
            user_id=user_id,
        )
        if saved_session is None:
            raise VoiceAnswerSubmissionError(
                "Interview session not found.",
                code="session_not_found",
            )

        if updated_state.current_turn is not None:
            self.repository.save_turn(
                session_id,
                updated_state.current_turn,
                user_id=user_id,
            )
        return updated_state
