from __future__ import annotations

import os
import shutil
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from core.dependencies import (
    get_current_user,
    get_document_service,
    get_interview_repository,
    get_resume_agent,
)
from infrastructure.documents import DocumentService
from infrastructure.repositories import SQLiteInterviewRepository
from services.profile_scanner.agent import ResumeAgent
from services.profile_scanner.exceptions import NonResumeDocumentError
from shared.schemas import CurrentUser


router = APIRouter(prefix="/api/v2/resume", tags=["v2-resume"])

MAX_RESUME_BYTES = 10 * 1024 * 1024
ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx"}


@router.post("/upload")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    repository: SQLiteInterviewRepository = Depends(get_interview_repository),
    document_service: DocumentService = Depends(get_document_service),
    resume_agent: ResumeAgent = Depends(get_resume_agent),
    current_user: CurrentUser = Depends(get_current_user),
):
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

        try:
            resume_text = document_service.extract_text(tmp_path, filename)
        except ValueError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error

        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(status_code=422, detail="Could not extract enough resume text.")

        try:
            profile = await resume_agent.extract_profile(resume_text)
        except NonResumeDocumentError as error:
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
        candidate = repository.create_candidate(
            profile.name or "Candidate", user_id=current_user.uid
        )
        repository.save_candidate_resume_text(
            candidate.candidate_id, resume_text, user_id=current_user.uid
        )
        persisted_profile = repository.save_candidate_profile(
            candidate.candidate_id, profile, user_id=current_user.uid
        )

        return {
            "candidate_id": candidate.candidate_id,
            "profile": persisted_profile,
            "confidence_score": persisted_profile.confidence_score,
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
