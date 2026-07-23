from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from core.dependencies import get_current_user, get_interview_repository, get_report_service
from core.exceptions import AIInterviewError, NotFoundError
from infrastructure.repositories.base import InterviewRepository
from services.report_generator.schemas import InterviewReport
from services.report_generator.service import ReportService
from shared.schemas import CurrentUser, InterviewSessionSummary


router = APIRouter(tags=["v2-report"])


class InterviewReportResponse(BaseModel):
    session_id: str
    report: InterviewReport


class InterviewHistoryResponse(BaseModel):
    items: list[InterviewSessionSummary]
    total: int
    limit: int
    offset: int


@router.post(
    "/api/v2/interview/{session_id}/report",
    response_model=InterviewReportResponse,
)
async def generate_interview_report(
    session_id: str,
    service: ReportService = Depends(get_report_service),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewReportResponse:
    try:
        report = await service.generate_for_session(session_id, current_user.uid)
    except AIInterviewError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
    return InterviewReportResponse(session_id=session_id, report=report)


@router.get(
    "/api/v2/interview/{session_id}/report",
    response_model=InterviewReportResponse,
)
async def get_interview_report(
    session_id: str,
    service: ReportService = Depends(get_report_service),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewReportResponse:
    try:
        report = await service.get_for_session(session_id, current_user.uid)
    except AIInterviewError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
    if report is None:
        error = NotFoundError("Interview report not found.")
        raise HTTPException(status_code=error.status_code, detail=str(error))
    return InterviewReportResponse(session_id=session_id, report=report)


@router.get("/api/v2/interviews", response_model=InterviewHistoryResponse)
async def list_interview_sessions(
    candidate_id: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    repository: InterviewRepository = Depends(get_interview_repository),
    current_user: CurrentUser = Depends(get_current_user),
) -> InterviewHistoryResponse:
    try:
        items = repository.list_interview_sessions(
            candidate_id, limit, offset, user_id=current_user.uid
        )
        total = repository.count_interview_sessions(
            candidate_id, user_id=current_user.uid
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail="Invalid candidate_id.") from error
    return InterviewHistoryResponse(items=items, total=total, limit=limit, offset=offset)
