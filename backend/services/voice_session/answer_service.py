from __future__ import annotations

from infrastructure.repositories.base import InterviewRepository
from orchestrator.interview_orchestrator import InterviewOrchestrator, QuestionProvider
from services.interview_answer_service import (
    InterviewAnswerSubmissionError,
    InterviewAnswerSubmissionService,
)
from shared.schemas import (
    InterviewMode,
    InterviewSessionState,
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
        self._submission_service = InterviewAnswerSubmissionService(
            repository=repository,
            orchestrator=orchestrator,
        )

    async def submit_answer(
        self,
        session_id: str,
        user_id: str,
        turn_id: str,
        answer: str,
        *,
        question_provider: QuestionProvider | None = None,
        voice_analytics: VoiceAnalytics | None = None,
    ) -> InterviewSessionState:
        try:
            result = await self._submission_service.submit_answer(
                session_id,
                user_id,
                turn_id,
                answer,
                expected_mode=InterviewMode.VOICE,
                question_provider=question_provider,
                voice_analytics=voice_analytics,
            )
        except InterviewAnswerSubmissionError as error:
            raise VoiceAnswerSubmissionError(str(error), code=error.code) from error
        return result.state
