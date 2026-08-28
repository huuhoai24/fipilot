"""POST /api/v2/resume/upload — Upload and extract a candidate resume.

Pipeline (matches 04_pipeline_poc.ipynb):
    1. Validate: extension (pdf/docx) + size (≤ 10 MB)
    2. Extract text:
         PDF  → pymupdf4llm.to_markdown()  (primary)
                pypdf + OCR               (fallback)
         DOCX → python-docx
    3. Compute SHA-256 hash of raw file bytes
    4. Cache lookup (in-memory ProcessedResumeCache, then PostgreSQL row)
    5. [miss] LLM Agent → CandidateProfile
    6. Persist row in `resumes` table + repopulate cache
    7. Return candidate_id, profile, extraction metadata
"""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
import time

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse

from core.dependencies import (
    CurrentUser,
    get_current_user,
    get_document_service,
    get_processed_resume_cache,
    get_resume_agent,
    get_resume_repository,
)
from infrastructure.documents import (
    DocumentExtractionResult,
    DocumentExtractionStatus,
    DocumentProcessingError,
    DocumentService,
)
from infrastructure.repositories import PostgresResumeRepository
from services.profile_scanner.agent import ResumeAgent
from services.profile_scanner.cache import (
    RESUME_EXTRACTION_VERSION,
    ProcessedResumeCache,
)
from services.profile_scanner.exceptions import NonResumeDocumentError

router = APIRouter(prefix="/api/v2/resume", tags=["resume"])

MAX_RESUME_BYTES = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {"pdf", "docx"}


@router.post("/upload", summary="Upload a resume PDF or DOCX and extract the candidate profile")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    document_service: DocumentService = Depends(get_document_service),
    resume_agent: ResumeAgent = Depends(get_resume_agent),
    resume_cache: ProcessedResumeCache = Depends(get_processed_resume_cache),
    repository: PostgresResumeRepository = Depends(get_resume_repository),
    current_user: CurrentUser = Depends(get_current_user),
):
    """Upload a PDF or DOCX resume, run the extraction pipeline, and return
    the structured ``CandidateProfile`` together with extraction metadata.

    **Response** (HTTP 200):
    ```json
    {
        "candidate_id": "<uuid>",
        "profile": { "name": "...", "skills": [...], ... },
        "extraction": {
            "status": "complete | partial",
            "source": "cached | extracted",
            "source_type": "pdf | docx",
            "extraction_method": "pymupdf4llm | native_pdf | ocr | mixed | docx",
            "character_count": 4471,
            "file_hash": "sha256..."
        }
    }
    ```
    """
    started_at = time.perf_counter()
    filename = file.filename or "resume"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    # ------------------------------------------------------------------
    # 1. Validate extension
    # ------------------------------------------------------------------
    if ext not in ALLOWED_EXTENSIONS:
        return _error(
            request,
            status_code=415,
            code="unsupported_file_type",
            message="Only PDF and DOCX resumes are supported.",
        )

    # ------------------------------------------------------------------
    # 2. Spool to a temp file (enables seekable reads for hash + extraction)
    # ------------------------------------------------------------------
    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # ------------------------------------------------------------------
        # 3. Validate size
        # ------------------------------------------------------------------
        file_size = os.path.getsize(tmp_path)
        if file_size > MAX_RESUME_BYTES:
            return _error(
                request,
                status_code=413,
                code="file_too_large",
                message=f"Resume must be ≤ 10 MB (received {file_size // 1024} KB).",
            )

        # ------------------------------------------------------------------
        # 4. SHA-256 hash
        # ------------------------------------------------------------------
        with open(tmp_path, "rb") as fh:
            content_hash = hashlib.file_digest(fh, "sha256").hexdigest()

        # ------------------------------------------------------------------
        # 5. Text extraction (pymupdf4llm primary for PDF, docx for DOCX)
        # ------------------------------------------------------------------
        document_result: DocumentExtractionResult
        try:
            document_result = document_service.extract_document(
                tmp_path,
                filename,
                content_type=file.content_type,
            )
        except DocumentProcessingError as exc:
            return _error(
                request,
                status_code=exc.status_code,
                code=exc.code,
                message=exc.safe_message,
                extra={"warnings": exc.warnings},
            )

        resume_text = document_result.text

        if not resume_text or len(resume_text.strip()) < 50:
            return _error(
                request,
                status_code=422,
                code="no_extractable_text",
                message="Could not extract enough text from the uploaded file.",
            )

        # ------------------------------------------------------------------
        # 6. Cache lookup — in-memory first, then PostgreSQL
        # ------------------------------------------------------------------
        profile = resume_cache.get(current_user.uid, content_hash, RESUME_EXTRACTION_VERSION)
        cache_source = "memory_cache"

        if profile is None:
            db_hit = repository.find_by_content_hash(
                user_id=current_user.uid,
                content_hash=content_hash,
            )
            if db_hit is not None:
                profile = db_hit
                cache_source = "db_cache"
                # Re-populate in-memory cache
                resume_cache.store(current_user.uid, content_hash, profile, RESUME_EXTRACTION_VERSION)

        # ------------------------------------------------------------------
        # 7. LLM extraction (only on full cache miss)
        # ------------------------------------------------------------------
        is_llm_extracted = False
        if profile is None:
            cache_source = "extracted"
            try:
                processing_result = await resume_agent.extract_profile_result(resume_text)
                profile = processing_result.profile
            except NonResumeDocumentError as exc:
                return _error(
                    request,
                    status_code=422,
                    code=exc.code,
                    message=exc.safe_message,
                )
            is_llm_extracted = True

        # ------------------------------------------------------------------
        # 8. Persist (only on fresh LLM extraction, avoid duplicate rows)
        # ------------------------------------------------------------------
        if is_llm_extracted:
            persisted = repository.save_resume(
                user_id=current_user.uid,
                filename=filename,
                profile=profile,
                content_hash=content_hash,
                resume_text=resume_text,
            )
            resume_cache.store(
                current_user.uid,
                content_hash,
                profile,
                RESUME_EXTRACTION_VERSION,
            )
        else:
            # profile came from cache — persisted already holds candidate_id
            persisted = profile  # type: ignore[assignment]

        # ------------------------------------------------------------------
        # 9. Build response
        # ------------------------------------------------------------------
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)
        return {
            "candidate_id": getattr(persisted, "candidate_id", None),
            "profile": persisted.model_dump(exclude={"candidate_id"}),
            "extraction": {
                "status": (
                    "partial"
                    if document_result.is_partial
                    else "complete"
                ),
                "source": cache_source,
                "source_type": document_result.source_type,
                "extraction_method": document_result.extraction_method,
                "character_count": document_result.character_count,
                "file_hash": content_hash,
                "elapsed_ms": elapsed_ms,
            },
        }

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _error(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    extra: dict | None = None,
) -> JSONResponse:
    body: dict = {
        "error": {
            "code": code,
            "message": message,
            **(extra or {}),
        }
    }
    # Include request_id if middleware set one
    if hasattr(request.state, "request_id"):
        body["request_id"] = request.state.request_id
    return JSONResponse(status_code=status_code, content=body)
