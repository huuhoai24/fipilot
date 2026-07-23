from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.interview_planner.prompts import (
    INTERVIEW_PLANNER_SYSTEM_INSTRUCTION,
    build_interview_planner_prompt,
)
from shared.schemas import CandidateProfile, InterviewConfig, InterviewPlan


class InterviewPlannerAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def create_plan(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig | None = None,
    ) -> InterviewPlan:
        config = interview_config or InterviewConfig(experience_level="junior")
        return await self.llm_service.generate_json(
            build_interview_planner_prompt(candidate_profile, config),
            InterviewPlan,
            system_instruction=INTERVIEW_PLANNER_SYSTEM_INSTRUCTION,
            task_type="complex",
            temperature=0.1,
        )
