from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class CandidateProject(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)
    role: str | None = None


class CandidateExperience(BaseModel):
    company: str = ""
    title: str = ""
    start_date: str | None = None
    end_date: str | None = None
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class CandidateEducation(BaseModel):
    institution: str = ""
    degree: str | None = None
    field_of_study: str | None = None
    start_date: str | None = None
    end_date: str | None = None


class SkillEvidence(BaseModel):
    skill: str = ""
    evidence: list[str] = Field(default_factory=list)
    source_section: str | None = None


class CandidateProfile(BaseModel):
    candidate_id: str | None = None
    name: str = "Candidate"
    years_experience: float | None = None
    recent_role: str | None = None
    skills: list[str] = Field(default_factory=list)
    skill_evidence: list[SkillEvidence] = Field(default_factory=list)
    projects: list[CandidateProject] = Field(default_factory=list)
    experiences: list[CandidateExperience] = Field(default_factory=list)
    education: str | list[CandidateEducation] | None = None
    specialization: str | None = None
    seniority_signal: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    extraction_method: str | None = None

    @model_validator(mode="before")
    @classmethod
    def keep_confidence_fields_compatible(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "confidence" not in data and "confidence_score" in data:
                data["confidence"] = data["confidence_score"]
            elif "confidence_score" not in data and "confidence" in data:
                data["confidence_score"] = data["confidence"]
        return data


class ResumeUploadResult(BaseModel):
    candidate_id: str
    profile: CandidateProfile
    resume_text_preview: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class PersistedCandidateProfile(CandidateProfile):
    candidate_id: str
    profile_version: int = Field(ge=1)


class ProfileIssue(BaseModel):
    code: str
    origin: Literal["profile_validity", "interview_readiness"]
    field_path: str | None = None


class InterviewReadiness(BaseModel):
    is_ready: bool
    issues: list[ProfileIssue] = Field(default_factory=list)


class CandidateProfileReadResponse(BaseModel):
    profile: PersistedCandidateProfile
    readiness: InterviewReadiness
