from __future__ import annotations

from pydantic import BaseModel, Field


class JobRequirements(BaseModel):
    job_id: str | None = None
    title: str | None = None
    domain: str | None = None
    level: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    raw_text: str | None = None


class JobAnalysisResult(BaseModel):
    job_id: str
    requirements: JobRequirements
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

