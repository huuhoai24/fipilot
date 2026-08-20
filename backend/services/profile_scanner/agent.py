from __future__ import annotations

from pydantic import BaseModel, Field

from infrastructure.llm.base import BaseLLMService
from services.profile_scanner.context import ResumeContext, build_resume_context
from services.profile_scanner.exceptions import NonResumeDocumentError
from services.profile_scanner.prompts import (
    RESUME_EXTRACTION_SYSTEM_INSTRUCTION,
    build_resume_extraction_prompt,
)
from services.profile_scanner.schemas import ResumeExtractionResult
from services.profile_scanner.verification import ProvenanceRecord, verify_and_reconcile_profile
from shared.schemas import CandidateProfile


class ResumeProcessingResult(BaseModel):
    profile: CandidateProfile
    context_total_characters: int
    context_characters_considered: int
    is_partial: bool
    warnings: list[str] = Field(default_factory=list)
    provenance: list[ProvenanceRecord] = Field(default_factory=list)


class ResumeAgent:
    MIN_RESUME_CLASSIFICATION_CONFIDENCE = 0.7

    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        return (await self.extract_profile_result(resume_text)).profile

    async def extract_raw(self, context: ResumeContext) -> ResumeExtractionResult:
        extraction = await self.llm_service.generate_json(
            build_resume_extraction_prompt(context.text),
            ResumeExtractionResult,
            system_instruction=RESUME_EXTRACTION_SYSTEM_INSTRUCTION,
            task_type="simple",
            temperature=0.1,
            thinking_budget=0,
            operation="resume_extraction",
        )
        if (
            extraction.document_type != "resume"
            or extraction.classification_confidence
            < self.MIN_RESUME_CLASSIFICATION_CONFIDENCE
        ):
            raise NonResumeDocumentError
        return extraction

    async def extract_profile_result(self, resume_text: str) -> ResumeProcessingResult:
        context = build_resume_context(resume_text)
        extraction = await self.extract_raw(context)
        verified = verify_and_reconcile_profile(extraction.to_candidate_profile(), resume_text)
        verified.profile.extraction_method = (
            "section_aware_partial" if context.is_partial else "section_aware_verified"
        )
        return ResumeProcessingResult(
            profile=verified.profile,
            context_total_characters=context.total_characters,
            context_characters_considered=context.characters_considered,
            is_partial=context.is_partial,
            warnings=[*context.warnings, *verified.warnings],
            provenance=verified.provenance,
        )
