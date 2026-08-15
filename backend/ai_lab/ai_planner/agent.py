from __future__ import annotations

from infrastructure.llm.base import BaseLLMService

from ai_lab.ai_planner.prompt import SYSTEM_INSTRUCTION, build_prompt
from ai_lab.ai_planner.schemas import InterviewPlan, PlannerInput


class PlannerLabAgent:
    TASK_TYPE = "simple"
    TEMPERATURE = 0.1

    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def run(
        self,
        input_data: PlannerInput,
        *,
        prompt: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> InterviewPlan:
        return await self.llm_service.generate_json(
            prompt or build_prompt(input_data),
            InterviewPlan,
            system_instruction=SYSTEM_INSTRUCTION,
            task_type=self.TASK_TYPE,
            model=model,
            temperature=self.TEMPERATURE if temperature is None else temperature,
            thinking_budget=0,
            operation="ai_lab_interview_planning",
        )
