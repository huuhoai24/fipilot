from __future__ import annotations

from core.exceptions import ConflictError, NotFoundError
from infrastructure.repositories.base import InterviewRepository
from services.report_generator.agent import ReportGeneratorAgent
from services.report_generator.schemas import InterviewReport
from shared.schemas import InterviewSessionState, InterviewStatus


class ReportService:
    def __init__(self, agent: ReportGeneratorAgent, repository: InterviewRepository):
        self.agent = agent
        self.repository = repository

    async def generate_for_session(
        self, session_id: str, user_id: str | None = None
    ) -> InterviewReport:
        session = self.repository.get_session(session_id, user_id=user_id)
        if session is None:
            raise NotFoundError("Interview session not found.")

        if session.status not in {
            InterviewStatus.COMPLETED.value,
            InterviewStatus.REPORT_GENERATED.value,
        }:
            raise ConflictError("Interview must be completed before generating a report.")

        existing = self.repository.get_interview_report(session_id, user_id=user_id)
        if existing is not None:
            return existing

        if not session.state_payload:
            raise NotFoundError("Interview session state not found.")
        state = InterviewSessionState.model_validate(session.state_payload)
        if state.current_turn is not None:
            raise ConflictError("Interview must be completed before generating a report.")

        profile = self.repository.get_candidate_profile(
            session.candidate_id, user_id=user_id
        )
        if profile is None:
            raise NotFoundError("Candidate profile not found.")

        generated = await self.agent.generate_report(profile, state)
        report = generated.model_copy(update={"session_id": session_id})
        self.repository.save_interview_report(report, user_id=user_id)
        self.repository.update_session_status(
            session_id,
            InterviewStatus.REPORT_GENERATED.value,
            report_id=report.id,
            user_id=user_id,
        )
        return report

    async def get_for_session(
        self, session_id: str, user_id: str | None = None
    ) -> InterviewReport | None:
        if self.repository.get_session(session_id, user_id=user_id) is None:
            raise NotFoundError("Interview session not found.")
        return self.repository.get_interview_report(session_id, user_id=user_id)


# Compatibility name retained for imports introduced in the architecture refactor.
ReportGeneratorService = ReportService
