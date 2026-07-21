from __future__ import annotations

from pydantic import BaseModel, Field


class CandidateProject(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)
    role: str | None = None


class CandidateProfile(BaseModel):
    candidate_id: str | None = None
    name: str = "Candidate"
    years_experience: float | None = None
    recent_role: str | None = None
    skills: list[str] = Field(default_factory=list)
    projects: list[CandidateProject] = Field(default_factory=list)
    education: str | None = None
    seniority_signal: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_method: str | None = None


class ResumeUploadResult(BaseModel):
    candidate_id: str
    profile: CandidateProfile
    resume_text_preview: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

