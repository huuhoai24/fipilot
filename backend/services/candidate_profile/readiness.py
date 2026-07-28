from __future__ import annotations

import math
from collections.abc import Iterable

from services.candidate_profile.normalization import (
    normalize_profile_text,
    normalized_comparison_key,
)
from shared.schemas import CandidateProfile, InterviewReadiness, ProfileIssue


def _has_meaningful_text(values: Iterable[str | None]) -> bool:
    return any(normalize_profile_text(value) for value in values)


def evaluate_interview_readiness(profile: CandidateProfile) -> InterviewReadiness:
    issues: list[ProfileIssue] = []
    name = normalize_profile_text(profile.name)
    if not name:
        issues.append(
            ProfileIssue(
                code="missing_name",
                origin="interview_readiness",
                field_path="name",
            )
        )
    elif name.casefold() == "candidate":
        issues.append(
            ProfileIssue(
                code="fallback_name",
                origin="interview_readiness",
                field_path="name",
            )
        )

    if (
        profile.years_experience is not None
        and (
            not math.isfinite(profile.years_experience)
            or profile.years_experience < 0
        )
    ):
        issues.append(
            ProfileIssue(
                code="invalid_years_experience",
                origin="profile_validity",
                field_path="years_experience",
            )
        )

    normalized_skills = [
        skill
        for skill in (normalize_profile_text(skill) for skill in profile.skills)
        if skill
    ]
    if not normalized_skills:
        issues.append(
            ProfileIssue(
                code="missing_skills",
                origin="interview_readiness",
                field_path="skills",
            )
        )

    skill_keys = {normalized_comparison_key(skill) for skill in normalized_skills}
    for index, item in enumerate(profile.skill_evidence):
        if not _has_meaningful_text([item.skill, *item.evidence]):
            issues.append(
                ProfileIssue(
                    code="empty_nested_entry",
                    origin="profile_validity",
                    field_path=f"skill_evidence.{index}",
                )
            )
        elif normalized_comparison_key(item.skill) not in skill_keys:
            issues.append(
                ProfileIssue(
                    code="evidence_skill_not_found",
                    origin="profile_validity",
                    field_path=f"skill_evidence.{index}.skill",
                )
            )

    has_skill_evidence = any(
        normalize_profile_text(text)
        for item in profile.skill_evidence
        for text in item.evidence
    )
    has_project_evidence = any(
        normalize_profile_text(project.name)
        or normalize_profile_text(project.description)
        for project in profile.projects
    )
    has_experience_evidence = any(
        normalize_profile_text(experience.title)
        or normalize_profile_text(experience.company)
        or normalize_profile_text(experience.description)
        for experience in profile.experiences
    )
    has_education_evidence = isinstance(profile.education, list) and any(
        normalize_profile_text(education.institution)
        and (
            normalize_profile_text(education.degree)
            or normalize_profile_text(education.field_of_study)
        )
        for education in profile.education
    )
    if not (
        has_skill_evidence
        or has_project_evidence
        or has_experience_evidence
        or has_education_evidence
    ):
        issues.append(
            ProfileIssue(
                code="missing_interviewable_evidence",
                origin="interview_readiness",
                field_path="skill_evidence",
            )
        )

    for index, project in enumerate(profile.projects):
        if not _has_meaningful_text(
            [
                project.name,
                project.description,
                project.role,
                *project.technologies,
            ]
        ):
            issues.append(
                ProfileIssue(
                    code="empty_nested_entry",
                    origin="profile_validity",
                    field_path=f"projects.{index}",
                )
            )

    for index, experience in enumerate(profile.experiences):
        if not _has_meaningful_text(
            [
                experience.company,
                experience.title,
                experience.start_date,
                experience.end_date,
                experience.description,
                *experience.technologies,
            ]
        ):
            issues.append(
                ProfileIssue(
                    code="empty_nested_entry",
                    origin="profile_validity",
                    field_path=f"experiences.{index}",
                )
            )

    if isinstance(profile.education, list):
        for index, education in enumerate(profile.education):
            if not _has_meaningful_text(
                [
                    education.institution,
                    education.degree,
                    education.field_of_study,
                    education.start_date,
                    education.end_date,
                ]
            ):
                issues.append(
                    ProfileIssue(
                        code="empty_nested_entry",
                        origin="profile_validity",
                        field_path=f"education.{index}",
                    )
                )

    return InterviewReadiness(is_ready=not issues, issues=issues)
