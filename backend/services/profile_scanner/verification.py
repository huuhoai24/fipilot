from __future__ import annotations

import re
import unicodedata
from enum import Enum

from pydantic import BaseModel, Field

from services.profile_scanner.context import split_resume_sections
from shared.schemas import CandidateExperience, CandidateProfile


class VerificationStatus(str, Enum):
    SUPPORTED = "supported"
    NORMALIZED_MATCH = "normalized_match"
    UNSUPPORTED = "unsupported"
    UNCERTAIN = "uncertain"


class ProvenanceRecord(BaseModel):
    field_path: str
    value: str
    status: VerificationStatus
    source_section: str | None = None
    evidence_text: str | None = None


class VerifiedProfileResult(BaseModel):
    profile: CandidateProfile
    provenance: list[ProvenanceRecord] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


_EXPERIENCE_LINE = re.compile(
    r"^(?P<title>[^|\n]{2,100}?)\s+at\s+(?P<company>[^|\n]{2,120}?)\s*\|\s*(?P<start>.+?)\s+(?:-|–|—|to)\s+(?P<end>[^|\n]+)$",
    re.IGNORECASE,
)


def _normalize(value: str | None) -> str:
    decomposed = unicodedata.normalize("NFKD", (value or "").casefold())
    plain = "".join(character for character in decomposed if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", " ", plain).strip()


def _parse_experiences(resume_text: str) -> list[tuple[CandidateExperience, str]]:
    parsed: list[tuple[CandidateExperience, str]] = []
    for section in split_resume_sections(resume_text):
        if section.key != "experience":
            continue
        lines = [line.strip() for line in section.text.splitlines() if line.strip()]
        for index, line in enumerate(lines):
            match = _EXPERIENCE_LINE.match(line)
            if not match:
                continue
            description = lines[index + 1] if index + 1 < len(lines) and not _EXPERIENCE_LINE.match(lines[index + 1]) else ""
            parsed.append((CandidateExperience(company=match.group("company").strip(), title=match.group("title").strip(), start_date=match.group("start").strip(), end_date=match.group("end").strip(), description=description), line))
    return parsed


def _status_for(value: str, source: str) -> VerificationStatus:
    if value and value in source:
        return VerificationStatus.SUPPORTED
    if _normalize(value) and _normalize(value) in _normalize(source):
        return VerificationStatus.NORMALIZED_MATCH
    return VerificationStatus.UNCERTAIN


def _identity_titles(resume_text: str, candidate_name: str) -> set[str]:
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    name = _normalize(candidate_name)
    return {
        _normalize(lines[index + 1])
        for index, line in enumerate(lines[:-1])
        if _normalize(line) == name
    }


def verify_and_reconcile_profile(profile: CandidateProfile, resume_text: str) -> VerifiedProfileResult:
    reconciled = profile.model_copy(deep=True)
    parsed = _parse_experiences(resume_text)
    matched_predictions: set[int] = set()
    final_experiences: list[CandidateExperience] = []
    repair_fields: set[tuple[int, str]] = set()
    rejected_identity_claims: list[tuple[int, CandidateExperience]] = []
    identity_titles = _identity_titles(resume_text, reconciled.name)
    for parsed_experience, _ in parsed:
        best_index = next((index for index, predicted in enumerate(reconciled.experiences) if index not in matched_predictions and _normalize(predicted.title) == _normalize(parsed_experience.title) and (_normalize(predicted.company) in _normalize(parsed_experience.company) or _normalize(parsed_experience.company) in _normalize(predicted.company))), None)
        if best_index is None:
            final_experiences.append(parsed_experience)
            continue
        matched_predictions.add(best_index)
        predicted = reconciled.experiences[best_index].model_copy(deep=True)
        final_index = len(final_experiences)
        if predicted.company != parsed_experience.company:
            predicted.company = parsed_experience.company
            repair_fields.add((final_index, "company"))
        if predicted.title != parsed_experience.title:
            predicted.title = parsed_experience.title
            repair_fields.add((final_index, "title"))
        predicted.start_date = parsed_experience.start_date or predicted.start_date
        predicted.end_date = parsed_experience.end_date or predicted.end_date
        if not predicted.description:
            predicted.description = parsed_experience.description
        final_experiences.append(predicted)
    for index, predicted in enumerate(reconciled.experiences):
        if index in matched_predictions:
            continue
        if _normalize(predicted.company) == _normalize(reconciled.name):
            rejected_identity_claims.append((index, predicted))
            continue
        if (
            _normalize(predicted.title) in identity_titles
            and not predicted.start_date
            and not predicted.end_date
            and any(
                _normalize(parsed_experience.company) == _normalize(predicted.company)
                for parsed_experience, _ in parsed
            )
        ):
            rejected_identity_claims.append((index, predicted))
            continue
        final_experiences.append(predicted)
    reconciled.experiences = final_experiences[:6]
    provenance: list[ProvenanceRecord] = [
        ProvenanceRecord(
            field_path=f"experiences[{index}]",
            value=f"{experience.title} at {experience.company}",
            status=VerificationStatus.UNSUPPORTED,
            evidence_text="Identity-block content is not a separate dated Experience entry.",
        )
        for index, experience in rejected_identity_claims
    ]
    for field in ("name", "recent_role", "specialization"):
        value = getattr(reconciled, field) or ""
        provenance.append(
            ProvenanceRecord(field_path=field, value=value, status=_status_for(value, resume_text))
        )
    for index, skill in enumerate(reconciled.skills):
        provenance.append(
            ProvenanceRecord(field_path=f"skills[{index}]", value=skill, status=_status_for(skill, resume_text), source_section="skills")
        )
    for index, experience in enumerate(reconciled.experiences):
        for field in ("company", "title", "start_date", "end_date"):
            value = getattr(experience, field) or ""
            status = VerificationStatus.NORMALIZED_MATCH if (index, field) in repair_fields else _status_for(value, resume_text)
            provenance.append(ProvenanceRecord(field_path=f"experiences[{index}].{field}", value=value, status=status, source_section="experience" if status is not VerificationStatus.UNCERTAIN else None, evidence_text=next((line for _, line in parsed if value and _normalize(value) in _normalize(line)), None)))
    return VerifiedProfileResult(profile=reconciled, provenance=provenance)
