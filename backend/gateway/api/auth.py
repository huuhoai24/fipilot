from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.dependencies import get_current_user
from shared.schemas import CurrentUser


router = APIRouter(prefix="/api/v2/auth", tags=["v2-auth"])


class CurrentUserResponse(BaseModel):
    uid: str
    email: str | None = None
    name: str | None = None
    picture: str | None = None
    email_verified: bool = False


@router.get("/me", response_model=CurrentUserResponse)
async def get_authenticated_user(
    current_user: CurrentUser = Depends(get_current_user),
) -> CurrentUserResponse:
    return CurrentUserResponse(**current_user.model_dump(exclude={"claims"}))
