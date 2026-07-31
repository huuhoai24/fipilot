"""Schemas used only at the Resume extraction boundary."""

from pydantic import BaseModel, Field

from shared.schemas.candidate import *  # noqa: F401,F403


class ExtractedSkillEvidence(BaseModel):
    skill: str = ""
    evidence: str = ""
    source_section: str | None = None


class ResumeExtractionResult(BaseModel):
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
