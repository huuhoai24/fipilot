from __future__ import annotations

from core.logging import get_logger
from core.performance import timed_stage
from infrastructure.llm.base import BaseLLMService
from services.question_generator.prompts import (
    QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
    build_question_generator_prompt,
)
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


logger = get_logger(__name__)


class QuestionGeneratorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def generate_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
    ) -> InterviewQuestion:
        with timed_stage(
            logger,
            "interview.question_prompt",
            stage="prompt_build",
        ):
            prompt = build_question_generator_prompt(
                candidate_profile,
                interview_round,
                interview_config,
            )
        with timed_stage(
            logger,
            "interview.question_generation",
            stage="question_model_call",
        ):
            return await self.llm_service.generate_json(
                prompt,
                InterviewQuestion,
                system_instruction=QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
                task_type="simple",
                temperature=0.6,
                thinking_budget=0,
                operation="question_generation",
            )
