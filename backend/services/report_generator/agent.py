from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from infrastructure.llm.base import BaseLLMService
from services.report_generator.prompts import REPORT_SYSTEM_INSTRUCTION, build_report_prompt
from services.report_generator.schemas import InterviewReport
from shared.schemas import CandidateProfile, InterviewSessionState


class ReportGeneratorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def generate_report(
        self,
        candidate_profile: CandidateProfile,
        interview_state: InterviewSessionState,
    ) -> InterviewReport:
        report = await self.llm_service.generate_json(
            build_report_prompt(candidate_profile, interview_state),
            InterviewReport,
            system_instruction=REPORT_SYSTEM_INSTRUCTION,
            task_type="complex",
            temperature=0.1,
        )
        return report.model_copy(
            update={
                "id": str(uuid4()),
                "session_id": "",
                "generated_at": datetime.now(timezone.utc),
            }
        )
