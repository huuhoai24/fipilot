from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from core.dependencies import get_current_user, get_interview_repository
from infrastructure.repositories import InterviewRepository
from services.candidate_profile import evaluate_interview_readiness
from shared.schemas import CandidateProfileReadResponse, CurrentUser


router = APIRouter(prefix="/api/v2/candidates", tags=["v2-candidate-profile"])


@router.get(
    "/{candidate_id}/profile",
    response_model=CandidateProfileReadResponse,
)
def get_candidate_profile(
    candidate_id: str,
    request: Request,
    response: Response,
    repository: InterviewRepository = Depends(get_interview_repository),
    current_user: CurrentUser = Depends(get_current_user),
) -> CandidateProfileReadResponse | JSONResponse:
    profile = repository.get_candidate_profile(
        candidate_id,
        user_id=current_user.uid,
    )
    if profile is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "candidate_profile_not_found",
                    "message": "Candidate Profile not found.",
                    "retryable": False,
                    "issues": [],
                },
                "request_id": request.state.request_id,
            },
        )

    response.headers["ETag"] = f'"{profile.profile_version}"'
    return CandidateProfileReadResponse(
        profile=profile,
        readiness=evaluate_interview_readiness(profile),
    )
