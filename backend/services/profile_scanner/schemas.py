"""Schemas used only at the Resume extraction boundary."""

from typing import Literal

from pydantic import BaseModel, Field

from shared.schemas.candidate import *  # noqa: F401,F403


class ExtractedSkillEvidence(BaseModel):
    skill: str = ""
    evidence: str = ""
    source_section: str | None = None


class ExtractedRoleMatch(BaseModel):
    role_id: str = ""
    title: str = ""
    score: int = 0
    matched_skills: list[str] = Field(default_factory=list)
    relevant_experience_count: int = 0
    summary: str = ""


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
    role_matches: list[ExtractedRoleMatch] = Field(default_factory=list)

    def to_candidate_profile(self) -> CandidateProfile:
        skill_by_key = {
            skill.strip().casefold(): skill
            for skill in self.skills
            if skill.strip()
        }
        selected_evidence = [
            item
            for item in self.skill_evidence
            if item.evidence.strip()
            and item.skill.strip().casefold() in skill_by_key
        ][:8]
        evidence_keys = [
            item.skill.strip().casefold()
            for item in selected_evidence
        ]
        selected_keys = list(
            dict.fromkeys([*evidence_keys, *skill_by_key.keys()])
        )[:30]
        selected_skill_keys = set(selected_keys)

        converted_role_matches = [
            RoleMatch(
                role_id=rm.role_id,
                title=rm.title,
                score=rm.score,
                matched_skills=rm.matched_skills,
                relevant_experience_count=rm.relevant_experience_count,
                summary=rm.summary,
            )
            for rm in self.role_matches
        ]

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
            role_matches=converted_role_matches,
        )
