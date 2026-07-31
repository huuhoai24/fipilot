from __future__ import annotations

from infrastructure.llm.base import BaseLLMService
from services.profile_scanner.prompts import (
    RESUME_EXTRACTION_SYSTEM_INSTRUCTION,
    build_resume_extraction_prompt,
)
from services.profile_scanner.schemas import ResumeExtractionResult
from shared.schemas import CandidateProfile


class ResumeAgent:
    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        extraction = await self.llm_service.generate_json(
            build_resume_extraction_prompt(resume_text),
            ResumeExtractionResult,
            system_instruction=RESUME_EXTRACTION_SYSTEM_INSTRUCTION,
            task_type="simple",
            temperature=0.1,
            thinking_budget=0,
        )
        return extraction.to_candidate_profile()
