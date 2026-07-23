from __future__ import annotations

from services.interview_planner.agent import InterviewPlannerAgent
from shared.schemas import CandidateProfile, InterviewConfig, InterviewPlan


class InterviewPlannerService:
    def __init__(self, agent: InterviewPlannerAgent):
        self.agent = agent

    async def create_plan(self, candidate_profile: CandidateProfile, interview_config: InterviewConfig) -> InterviewPlan:
        return await self.agent.create_plan(candidate_profile, interview_config)

