from __future__ import annotations

from services.question_generator.agent import QuestionGeneratorAgent
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion, InterviewRound


class QuestionGeneratorService:
    def __init__(self, agent: QuestionGeneratorAgent):
        self.agent = agent

    async def generate_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
    ) -> InterviewQuestion:
        return await self.agent.generate_question(candidate_profile, interview_round, interview_config)

