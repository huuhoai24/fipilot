from __future__ import annotations

from infrastructure.llm.base import BaseLLMService

from ai_lab.ai_cv.prompt import SYSTEM_INSTRUCTION, build_prompt
from ai_lab.ai_cv.schemas import CVInput, CandidateProfile, ResumeExtractionResult
from ai_lab.ai_cv.exceptions import NonResumeDocumentError, MarginalResumeDocumentError


class CVLabAgent:
    MIN_RESUME_CLASSIFICATION_CONFIDENCE = 0.7
    TASK_TYPE = "simple"
    TEMPERATURE = 0.1

    def __init__(self, llm_service: BaseLLMService):
        self.llm_service = llm_service

    async def run(
        self,
        input_data: CVInput,
        *,
        prompt: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
    ) -> CandidateProfile:
        extraction = await self.llm_service.generate_json(
            prompt or build_prompt(input_data.resume_text),
            ResumeExtractionResult,
            system_instruction=SYSTEM_INSTRUCTION,
            task_type=self.TASK_TYPE,
            model=model,
            temperature=self.TEMPERATURE if temperature is None else temperature,
            thinking_budget=0,
            operation="ai_lab_resume_extraction",
        )
        if extraction.document_type == "marginal_resume":
            raise MarginalResumeDocumentError(
                closest_domains=extraction.closest_domains,
                match_percentage=extraction.match_percentage,
            )
        elif (
            extraction.document_type != "resume"
            or extraction.classification_confidence
            < self.MIN_RESUME_CLASSIFICATION_CONFIDENCE
        ):
            raise NonResumeDocumentError()
        return extraction.to_candidate_profile()
