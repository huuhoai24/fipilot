from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends, Header, HTTPException

from infrastructure.documents.pdf_service import DocumentService
from infrastructure.llm.azure_openai import AzureOpenAIService
from infrastructure.llm.base import BaseLLMService
from infrastructure.repositories import PostgresResumeRepository
from services.profile_scanner.agent import ResumeAgent
from services.profile_scanner.cache import ProcessedResumeCache


@dataclass(frozen=True)
class CurrentUser:
    """Lightweight identity token passed through the request context."""
    uid: str


# ---------------------------------------------------------------------------
# Singletons
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_document_service() -> DocumentService:
    return DocumentService()


@lru_cache(maxsize=1)
def get_processed_resume_cache() -> ProcessedResumeCache:
    return ProcessedResumeCache(ttl_seconds=3600.0, max_entries=256)


@lru_cache(maxsize=1)
def get_llm_service() -> BaseLLMService:
    return AzureOpenAIService()


@lru_cache(maxsize=1)
def get_resume_repository() -> PostgresResumeRepository:
    return PostgresResumeRepository()


# ---------------------------------------------------------------------------
# Per-request dependencies
# ---------------------------------------------------------------------------

def get_resume_agent(
    llm_service: BaseLLMService = Depends(get_llm_service),
) -> ResumeAgent:
    return ResumeAgent(llm_service)


def get_interview_planner_agent(
    llm_service: BaseLLMService = Depends(get_llm_service),
) -> "InterviewPlannerAgent":
    from services.interview_planner.agent import InterviewPlannerAgent
    return InterviewPlannerAgent(llm_service)


def get_question_generator_agent(
    llm_service: BaseLLMService = Depends(get_llm_service),
):
    from services.interview_planner.question_agent import QuestionGeneratorAgent
    return QuestionGeneratorAgent(llm_service)


def get_rag_retriever(
    llm_service: BaseLLMService = Depends(get_llm_service),
) -> "RagRetrieverMock":
    from infrastructure.interview_knowledge.rag_mock import RagRetrieverMock
    # In a real app this would be a singleton or loaded on startup
    return RagRetrieverMock(llm_service)



def get_current_user(
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> CurrentUser:
    """Resolve the current user from the request.

    When ``AUTH_ENABLED=false`` (local dev) the caller may pass any value in
    ``X-User-ID``.  In production this header should be removed at the gateway
    and replaced with a verified Firebase UID after token validation.
    """
    auth_enabled = os.getenv("AUTH_ENABLED", "true").strip().lower() not in {"false", "0", "no"}

    if auth_enabled:
        # Production: X-User-ID must be injected by the auth middleware upstream.
        if not x_user_id:
            raise HTTPException(status_code=401, detail="Missing authentication.")
        return CurrentUser(uid=x_user_id)

    # Dev mode: use provided header or a deterministic fallback.
    uid = x_user_id or os.getenv("AUTH_DEV_USER_ID", "dev-user")
    return CurrentUser(uid=uid)


def get_evaluator_agent(
    llm_service: BaseLLMService = Depends(get_llm_service),
):
    from services.interview_evaluation.evaluator_agent import EvaluatorAgent
    return EvaluatorAgent(llm_service)

def get_report_agent(
    llm_service: BaseLLMService = Depends(get_llm_service),
):
    from services.interview_evaluation.report_agent import ReportGeneratorAgent
    return ReportGeneratorAgent(llm_service)
