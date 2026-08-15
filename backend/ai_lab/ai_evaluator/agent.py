from __future__ import annotations

from core.settings import get_settings
from infrastructure.llm.base import BaseLLMService

from ai_lab.ai_evaluator.prompt import SYSTEM_INSTRUCTION, build_prompt
from ai_lab.ai_evaluator.schemas import AnswerEvaluation, EvaluatorInput, InterviewMode


class EvaluatorLabAgent:
    TEMPERATURE = 0.1

    def __init__(self, llm_service: BaseLLMService, *, text_task_type: str | None = None):
        self.llm_service = llm_service
        self.text_task_type = text_task_type or get_settings().evaluator_task_type

    def task_type_for(self, input_data: EvaluatorInput) -> str:
        return "simple" if input_data.interview_config.mode == InterviewMode.VOICE else self.text_task_type

    async def run(self, input_data: EvaluatorInput, *, prompt: str | None = None, model: str | None = None, temperature: float | None = None) -> AnswerEvaluation:
        is_voice = input_data.interview_config.mode == InterviewMode.VOICE
        return await self.llm_service.generate_json(
            prompt or build_prompt(input_data),
            AnswerEvaluation,
            system_instruction=SYSTEM_INSTRUCTION,
            task_type=self.task_type_for(input_data),
            model=model,
            temperature=self.TEMPERATURE if temperature is None else temperature,
            thinking_budget=0 if is_voice else None,
            operation="ai_lab_answer_evaluation",
        )
