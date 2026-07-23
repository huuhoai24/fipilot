from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.answer_evaluator.prompts import EVALUATOR_SYSTEM_INSTRUCTION, build_evaluator_prompt
from shared.schemas import AnswerEvaluation, CandidateProfile, InterviewConfig, InterviewQuestion


class EvaluatorAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def evaluate_answer(
        self,
        candidate_profile: CandidateProfile,
        interview_question: InterviewQuestion,
        answer: str,
        interview_config: InterviewConfig,
    ) -> AnswerEvaluation:
        return await self.llm_service.generate_json(
            build_evaluator_prompt(candidate_profile, interview_question, answer, interview_config),
            AnswerEvaluation,
            system_instruction=EVALUATOR_SYSTEM_INSTRUCTION,
            task_type="complex",
            temperature=0.1,
        )
