from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.profile_scanner.prompts import (
    RESUME_EXTRACTION_SYSTEM_INSTRUCTION,
    build_resume_extraction_prompt,
)
from shared.schemas import CandidateProfile


class ResumeAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        return await self.llm_service.generate_json(
            build_resume_extraction_prompt(resume_text),
            CandidateProfile,
            system_instruction=RESUME_EXTRACTION_SYSTEM_INSTRUCTION,
            task_type="complex",
            temperature=0.1,
        )
