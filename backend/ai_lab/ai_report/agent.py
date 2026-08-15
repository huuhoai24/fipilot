from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from infrastructure.llm.base import BaseLLMService

from ai_lab.ai_report.prompt import SYSTEM_INSTRUCTION, build_prompt
from ai_lab.ai_report.schemas import InterviewReport, ReportInput


class ReportLabAgent:
    TASK_TYPE = "complex"
    TEMPERATURE = 0.1

    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def run(self, input_data: ReportInput, *, prompt: str | None = None, model: str | None = None, temperature: float | None = None) -> InterviewReport:
        report = await self.llm_service.generate_json(
            prompt or build_prompt(input_data),
            InterviewReport,
            system_instruction=SYSTEM_INSTRUCTION,
            task_type=self.TASK_TYPE,
            model=model,
            temperature=self.TEMPERATURE if temperature is None else temperature,
            operation="ai_lab_report_generation",
        )
        return report.model_copy(update={"id": str(uuid4()), "session_id": "", "generated_at": datetime.now(timezone.utc)})
