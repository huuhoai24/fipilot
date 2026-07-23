from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.question_generator.prompts import (
    QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
    build_question_generator_prompt,
)
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


class QuestionGeneratorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def generate_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
    ) -> InterviewQuestion:
        return await self.llm_service.generate_json(
            build_question_generator_prompt(candidate_profile, interview_round, interview_config),
            InterviewQuestion,
            system_instruction=QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
            task_type="complex",
            temperature=0.2,
        )
