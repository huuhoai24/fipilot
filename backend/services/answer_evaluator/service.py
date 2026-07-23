from __future__ import annotations

from services.answer_evaluator.agent import EvaluatorAgent
from shared.schemas import AnswerEvaluation, CandidateProfile, InterviewConfig, InterviewQuestion


class AnswerEvaluatorService:
    def __init__(self, agent: EvaluatorAgent):
        self.agent = agent

    async def evaluate_answer(
        self,
        candidate_profile: CandidateProfile,
        interview_question: InterviewQuestion,
        answer: str,
        interview_config: InterviewConfig,
    ) -> AnswerEvaluation:
        return await self.agent.evaluate_answer(candidate_profile, interview_question, answer, interview_config)

