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
from infrastructure.documents import DocumentService
from infrastructure.repositories import SQLiteInterviewRepository
from services.profile_scanner.agent import ResumeAgent
from services.profile_scanner.cache import ProcessedResumeCache
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
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resumes are supported.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        if os.path.getsize(tmp_path) > MAX_RESUME_BYTES:
            raise HTTPException(status_code=413, detail="Resume file is too large.")

        with timed_stage(logger, "cv.content_hash", stage="sha256"):
            with open(tmp_path, "rb") as resume_stream:
                content_hash = hashlib.file_digest(resume_stream, "sha256").hexdigest()

        try:
            with timed_stage(
                logger,
                "cv.file_parse",
                stage="document_extraction",
            ):
                resume_text = document_service.extract_text(tmp_path, filename)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=422, detail="Could not extract enough resume text.")

        cache_started_at = time.perf_counter()
        profile = processed_resume_cache.get(current_user.uid, content_hash)
        cache_hit = profile is not None
        log_duration(
            logger,
            "cv.processed_cache",
            cache_started_at,
            status="hit" if cache_hit else "miss",
            stage="profile_extraction_reuse",
            cache_hit=cache_hit,
        )

        if profile is None:
            try:
                with timed_stage(
                    logger,
                    "cv.profile_extraction",
                    stage="profile_model_call",
                ):
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
            )

        total_status = "cached" if cache_hit else "complete"
        return {
            "candidate_id": candidate.candidate_id,
            "profile": persisted_profile,
            "confidence_score": persisted_profile.confidence_score,
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
