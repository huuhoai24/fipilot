from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    uid: str
    email: str | None = None
    name: str | None = None
    picture: str | None = None
    email_verified: bool = False
    claims: dict[str, Any] = Field(default_factory=dict)
