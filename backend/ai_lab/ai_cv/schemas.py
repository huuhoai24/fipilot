from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class CVInput(BaseModel):
    resume_text: str = Field(min_length=1)


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


class ExtractedSkillEvidence(BaseModel):
    skill: str = ""
    evidence: str = ""
    source_section: str | None = None


class ResumeExtractionResult(BaseModel):
    document_type: Literal[
        "resume",
        "portfolio",
        "job_description",
        "academic_report",
        "project_report",
        "research_paper",
        "certificate",
        "other",
    ]
    classification_confidence: float = Field(ge=0.0, le=1.0)
    name: str = "Candidate"
    years_experience: float | None = None
    recent_role: str | None = None
    skills: list[str] = Field(default_factory=list)
    skill_evidence: list[ExtractedSkillEvidence] = Field(default_factory=list)
    projects: list[CandidateProject] = Field(default_factory=list)
    experiences: list[CandidateExperience] = Field(default_factory=list)
    education: list[CandidateEducation] = Field(default_factory=list)
    specialization: str | None = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)

    def to_candidate_profile(self) -> CandidateProfile:
        skill_by_key = {
            skill.strip().casefold(): skill for skill in self.skills if skill.strip()
        }
        selected_evidence = [
            item
            for item in self.skill_evidence
            if item.evidence.strip() and item.skill.strip().casefold() in skill_by_key
        ][:8]
        evidence_keys = [item.skill.strip().casefold() for item in selected_evidence]
        selected_keys = list(dict.fromkeys([*evidence_keys, *skill_by_key.keys()]))[:30]
        selected_skill_keys = set(selected_keys)

        return CandidateProfile(
            name=self.name,
            years_experience=self.years_experience,
            recent_role=self.recent_role,
            skills=[skill_by_key[key] for key in selected_keys],
            skill_evidence=[
                {
                    "skill": skill_by_key[item.skill.strip().casefold()],
                    "evidence": [item.evidence],
                    "source_section": item.source_section,
                }
                for item in selected_evidence
                if item.skill.strip().casefold() in selected_skill_keys
            ],
            projects=self.projects[:6],
            experiences=self.experiences[:6],
            education=self.education,
            specialization=self.specialization,
            confidence_score=self.confidence_score,
        )
