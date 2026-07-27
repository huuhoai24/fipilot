from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.answer_evaluator.prompts import EVALUATOR_SYSTEM_INSTRUCTION, build_evaluator_prompt
from shared.schemas import AnswerEvaluation, CandidateProfile, InterviewConfig, InterviewQuestion


class EvaluatorAgent:
    """Scores one answer.

    In voice mode this sits on the critical path between the candidate finishing
    and the next question being spoken, and it dominates that gap: measured
    ~25 s on gemini-2.5-pro versus ~13.5 s on gemini-2.5-flash for the same
    answer. The default stays on the stronger model because the score is the
    product's output; set EVALUATOR_TASK_TYPE=simple to trade some scoring
    quality for roughly half the wait.
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
        return await self.llm_service.generate_json(
            build_evaluator_prompt(candidate_profile, interview_question, answer, interview_config),
            AnswerEvaluation,
            system_instruction=EVALUATOR_SYSTEM_INSTRUCTION,
            task_type=self.task_type,
            temperature=0.1,
        )
