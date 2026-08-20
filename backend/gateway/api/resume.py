from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
import time

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from core.dependencies import (
    get_current_user,
    get_document_service,
    get_interview_repository,
    get_processed_resume_cache,
    get_resume_agent,
)
from core.logging import get_logger
from core.performance import log_duration, timed_stage
from infrastructure.documents import (
    DocumentExtractionResult,
    DocumentExtractionStatus,
    DocumentProcessingError,
    DocumentService,
)
from infrastructure.repositories import SQLiteInterviewRepository
from services.profile_scanner.agent import ResumeAgent
from services.profile_scanner.context import build_resume_context
from services.profile_scanner.cache import (
    RESUME_EXTRACTION_VERSION,
    ProcessedResumeCache,
)
from services.profile_scanner.exceptions import NonResumeDocumentError
from shared.schemas import CurrentUser


router = APIRouter(prefix="/api/v2/resume", tags=["v2-resume"])
logger = get_logger(__name__)

MAX_RESUME_BYTES = 10 * 1024 * 1024
ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx"}


@router.post("/upload")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    document_service: DocumentService = Depends(get_document_service),
    resume_agent: ResumeAgent = Depends(get_resume_agent),
    processed_resume_cache: ProcessedResumeCache = Depends(get_processed_resume_cache),
    current_user: CurrentUser = Depends(get_current_user),
):
    total_started_at = time.perf_counter()
    total_status = "failed"
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_RESUME_EXTENSIONS:
        return JSONResponse(
            status_code=415,
            content={
                "error": {
                    "code": "unsupported_file_type",
                    "message": "Only PDF and DOCX resumes are supported.",
                    "retryable": False,
                    "issues": [],
                },
                "request_id": request.state.request_id,
            },
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        if os.path.getsize(tmp_path) > MAX_RESUME_BYTES:
            raise HTTPException(status_code=413, detail="Resume file is too large.")

        with timed_stage(logger, "cv.content_hash", stage="sha256"):
            with open(tmp_path, "rb") as resume_stream:
                content_hash = hashlib.file_digest(resume_stream, "sha256").hexdigest()

        document_result: DocumentExtractionResult
        try:
            with timed_stage(
                logger,
                "cv.file_parse",
                stage="document_extraction",
            ):
                if hasattr(document_service, "extract_document"):
                    document_result = document_service.extract_document(
                        tmp_path,
                        filename,
                        content_type=file.content_type,
                    )
                    resume_text = document_result.text
                else:  # compatibility for narrow dependency-injected test doubles
                    resume_text = document_service.extract_text(tmp_path, filename)
                    document_result = DocumentExtractionResult(
                        text=resume_text,
                        source_type=ext,
                        character_count=len(resume_text),
                        extraction_method="injected",
                        status=DocumentExtractionStatus.COMPLETE,
                    )
        except DocumentProcessingError as error:
            total_status = "rejected"
            return JSONResponse(
                status_code=error.status_code,
                content={
                    "error": {
                        "code": error.code,
                        "message": error.safe_message,
                        "retryable": False,
                        "issues": [],
                        "warnings": error.warnings,
                    },
                    "request_id": request.state.request_id,
                },
            )

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=422, detail="Could not extract enough resume text.")

        cache_started_at = time.perf_counter()
        profile = processed_resume_cache.get(
            current_user.uid,
            content_hash,
            RESUME_EXTRACTION_VERSION,
        )
        cache_hit = profile is not None
        log_duration(
            logger,
            "cv.processed_cache",
            cache_started_at,
            status="hit" if cache_hit else "miss",
            stage="profile_extraction_reuse",
            cache_hit=cache_hit,
        )

        persistent_artifact_key = processed_resume_cache.key_for(
            current_user.uid,
            content_hash,
            RESUME_EXTRACTION_VERSION,
        )
        persistent_hit = False
        if profile is None:
            persistent_started_at = time.perf_counter()
            profile = repository.get_resume_extraction_artifact(
                persistent_artifact_key,
                user_id=current_user.uid,
            )
            persistent_hit = profile is not None
            log_duration(
                logger,
                "cv.persistent_extraction",
                persistent_started_at,
                status="hit" if persistent_hit else "miss",
                stage="versioned_profile_artifact",
                cache_hit=persistent_hit,
            )
        cache_hit = profile is not None

        processing_result = None
        if profile is None:
            try:
                with timed_stage(
                    logger,
                    "cv.profile_extraction",
                    stage="profile_model_call",
                ):
                    if hasattr(resume_agent, "extract_profile_result"):
                        processing_result = await resume_agent.extract_profile_result(resume_text)
                        profile = processing_result.profile
                    else:  # compatibility for narrow dependency-injected test doubles
                        profile = await resume_agent.extract_profile(resume_text)
            except NonResumeDocumentError as error:
                total_status = "rejected"
                return JSONResponse(
                    status_code=422,
                    content={
                        "error": {
                            "code": error.code,
                            "message": error.safe_message,
                            "retryable": False,
                            "issues": [],
                        },
                        "request_id": request.state.request_id,
                    },
                )
        with timed_stage(logger, "cv.persistence", stage="candidate_profile_save"):
            candidate = repository.create_candidate(
                profile.name or "Candidate", user_id=current_user.uid
            )
            repository.save_candidate_resume_text(
                candidate.candidate_id, resume_text, user_id=current_user.uid
            )
            persisted_profile = repository.save_candidate_profile(
                candidate.candidate_id, profile, user_id=current_user.uid
            )
            processed_resume_cache.store(
                current_user.uid,
                content_hash,
                profile,
                RESUME_EXTRACTION_VERSION,
            )
            repository.save_resume_extraction_artifact(
                persistent_artifact_key,
                profile,
                user_id=current_user.uid,
            )

        total_status = "cached" if cache_hit else "complete"
        context_summary = build_resume_context(resume_text)
        warnings = [*document_result.warnings, *context_summary.warnings]
        if processing_result is not None:
            warnings.extend(processing_result.warnings)
        is_partial = document_result.is_partial or context_summary.is_partial or bool(
            processing_result and processing_result.is_partial
        )
        return {
            "candidate_id": candidate.candidate_id,
            "profile": persisted_profile,
            "confidence_score": persisted_profile.confidence_score,
            "extraction": {
                "status": "partial" if is_partial else "complete",
                "source_type": document_result.source_type,
                "page_count": document_result.page_count,
                "character_count": document_result.character_count,
                "extraction_method": document_result.extraction_method,
                "is_partial": is_partial,
                "warnings": list(dict.fromkeys(warnings)),
                "context_characters_considered": (
                    processing_result.context_characters_considered
                    if processing_result is not None
                    else context_summary.characters_considered
                ),
                "context_total_characters": (
                    processing_result.context_total_characters
                    if processing_result is not None
                    else context_summary.total_characters
                ),
            },
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        log_duration(
            logger,
            "cv.total",
            total_started_at,
            status=total_status,
        )
