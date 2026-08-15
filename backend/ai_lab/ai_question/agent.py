from __future__ import annotations

from infrastructure.llm.base import BaseLLMService

from ai_lab.ai_question.prompt import SYSTEM_INSTRUCTION, build_prompt
from ai_lab.ai_question.schemas import InterviewQuestion, QuestionInput


class QuestionLabAgent:
    TASK_TYPE = "simple"
    TEMPERATURE = 0.2

    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def run(self, input_data: QuestionInput, *, prompt: str | None = None, model: str | None = None, temperature: float | None = None) -> InterviewQuestion:
        return await self.llm_service.generate_json(
            prompt or build_prompt(input_data),
            InterviewQuestion,
            system_instruction=SYSTEM_INSTRUCTION,
            task_type=self.TASK_TYPE,
            model=model,
            temperature=self.TEMPERATURE if temperature is None else temperature,
            thinking_budget=0,
            operation="ai_lab_question_generation",
        )
