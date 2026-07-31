from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.answer_evaluator.prompts import EVALUATOR_SYSTEM_INSTRUCTION, build_evaluator_prompt
from shared.schemas import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewConfig,
    InterviewMode,
    InterviewQuestion,
)


class EvaluatorAgent:
    """Scores one answer.

    Voice evaluation uses the low-latency route because it sits on the spoken
    conversation's critical path. Text evaluation keeps the configured route.
    """

    def __init__(self, llm_service: BaseLLMService, *, task_type: str = "complex"):
        self.llm_service = llm_service
        self.task_type = task_type

    async def evaluate_answer(
        self,
        candidate_profile: CandidateProfile,
        interview_question: InterviewQuestion,
        answer: str,
        interview_config: InterviewConfig,
    ) -> AnswerEvaluation:
        is_voice = interview_config.mode == InterviewMode.VOICE
        return await self.llm_service.generate_json(
            build_evaluator_prompt(candidate_profile, interview_question, answer, interview_config),
            AnswerEvaluation,
            system_instruction=EVALUATOR_SYSTEM_INSTRUCTION,
            task_type="simple" if is_voice else self.task_type,
            temperature=0.1,
            thinking_budget=0 if is_voice else None,
        )
