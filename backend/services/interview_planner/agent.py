from __future__ import annotations

from core.logging import get_logger
from core.performance import timed_stage
from infrastructure.llm.base import BaseLLMService
from services.interview_knowledge import KnowledgeRetriever
from services.interview_planner.prompts import (
    INTERVIEW_PLANNER_SYSTEM_INSTRUCTION,
    build_interview_planner_prompt,
)
from shared.schemas import CandidateProfile, InterviewConfig, InterviewPlan


logger = get_logger(__name__)


class InterviewPlannerAgent:
    def __init__(
        self,
        llm_service: BaseLLMService,
        knowledge_retriever: KnowledgeRetriever | None = None,
    ):
        self.llm_service = llm_service
        self.knowledge_retriever = knowledge_retriever

    async def create_plan(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig | None = None,
    ) -> InterviewPlan:
        config = interview_config or InterviewConfig(experience_level="junior")
        with timed_stage(
            logger,
            "interview.retrieve_context",
            stage="local_knowledge_retrieval",
        ):
            knowledge_topics = (
                self.knowledge_retriever.retrieve_topics(candidate_profile, config)
                if self.knowledge_retriever
                else []
            )
        with timed_stage(logger, "interview.plan_prompt", stage="prompt_build"):
            prompt = build_interview_planner_prompt(
                candidate_profile,
                config,
                knowledge_topics,
            )
        with timed_stage(
            logger,
            "interview.plan_generation",
            stage="planner_model_call",
        ):
            return await self.llm_service.generate_json(
                prompt,
                InterviewPlan,
                system_instruction=INTERVIEW_PLANNER_SYSTEM_INSTRUCTION,
                task_type="simple",
                temperature=0.1,
                thinking_budget=0,
            )
