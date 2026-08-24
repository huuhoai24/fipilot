"""Build a small, traceable interview plan from role-focused resume evidence."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import PurePosixPath
import re
from typing import Any

from fipilot.role_matching import infer_candidate_role


KnowledgeRetriever = Callable[[str, str, int], list[dict[str, Any]]]

DIFFICULTY_BY_LEVEL = {
    "entry": "easy",
    "intern": "easy",
    "junior": "medium",
    "middle": "hard",
    "senior": "hard",
}


def _default_retrieve(query: str, role: str, top_k: int) -> list[dict[str, Any]]:
    from fipilot.knowledge_index import search_domain

    return search_domain(query, role, top_k=top_k)


def _topic_for(entry: dict[str, Any], knowledge: list[dict[str, Any]]) -> str:
    if knowledge:
        source = str(knowledge[0].get("source") or knowledge[0].get("path") or "")
        topic = PurePosixPath(source.replace("\\", "/")).stem.strip()
        if topic:
            return topic
    return str(entry.get("name") or entry.get("position") or "CV deep dive").strip()


def _candidate_level(work_experience: list[dict[str, Any]]) -> str:
    if not work_experience:
        return "Unknown"
    if all(str(entry.get("type", "")).casefold() != "work" for entry in work_experience):
        return "Entry"
    text = " ".join(
        str(entry.get(field, ""))
        for entry in work_experience
        for field in ("position", "name", "jobDescription")
    ).casefold()
    years = [int(value) for value in re.findall(r"\b(\d{1,2})\+?\s+years?\b", text)]
    if bool(re.search(r"\b(senior|lead|principal|staff|architect|manager)\b", text)) or any(
        value >= 5 for value in years
    ):
        return "Senior"
    if bool(re.search(r"\b(mid|middle)\b", text)) or any(value >= 3 for value in years):
        return "Middle"
    return "Entry"


def _education_evidence(education: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for item in education or []:
        if not isinstance(item, dict):
            continue
        institution = str(item.get("institution", "")).strip()
        degree = str(item.get("degree", "")).strip()
        field = str(item.get("field_of_study", "")).strip()
        details = ", ".join(value for value in (degree, field, institution) if value)
        if not details:
            continue
        entries.append(
            {
                "type": "Education",
                "name": institution or degree or field,
                "position": degree,
                "jobDescription": f"Education evidence: {details}.",
            }
        )
    return entries


def _skill_evidence(
    skills: list[str] | None,
    skill_evidence: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in skill_evidence or []:
        if not isinstance(item, dict):
            continue
        skill = str(item.get("skill", "")).strip()
        if not skill or skill.casefold() in seen:
            continue
        scope = str(item.get("scope", "unknown")).strip().casefold()
        if scope not in {"familiarity", "demonstrated", "strong", "unknown"}:
            scope = "unknown"
        source = str(item.get("source", "resume")).strip().casefold()
        if source not in {"resume", "work", "project"}:
            source = "resume"
        entries.append(
            {
                "type": "Skill",
                "name": skill,
                "position": "",
                "jobDescription": f"Skill evidence: {skill}; scope: {scope}; source: {source}.",
                "skill_scope": scope,
                "evidence_source": source,
            }
        )
        seen.add(skill.casefold())
    for skill in skills or []:
        if not isinstance(skill, str) or not skill.strip() or skill.casefold() in seen:
            continue
        clean_skill = skill.strip()
        entries.append(
            {
                "type": "Skill",
                "name": clean_skill,
                "position": "",
                "jobDescription": f"Skill evidence: {clean_skill}; scope: unknown; source: resume.",
                "skill_scope": "unknown",
                "evidence_source": "resume",
            }
        )
        seen.add(clean_skill.casefold())
    return entries


def _legacy_level(candidate_level: str, target_level: str) -> str:
    if candidate_level in {"Entry", "Unknown"}:
        return "Intern" if target_level.casefold() == "intern" else "Junior"
    return candidate_level


def _candidate_scope(entry: dict[str, Any]) -> str:
    entry_type = str(entry.get("type", "")).strip().casefold()
    if entry_type == "education":
        return "Education"
    if entry_type == "skill":
        return str(entry.get("skill_scope", "unknown")).strip().title()
    text = " ".join(
        str(entry.get(field, ""))
        for field in ("name", "position", "jobDescription")
    ).casefold()
    if "prototype" in text:
        return "Prototype"
    if "proof of concept" in text or re.search(r"\bpoc\b", text):
        return "POC"
    if any(marker in text for marker in ("academic", "university", "coursework", "course project", "student")):
        return "Academic"
    if any(marker in text for marker in ("personal project", "side project", "personal")):
        return "Personal"
    if entry_type == "project":
        return "Project"
    if entry_type == "work":
        return "Work"
    return "Unknown"


def create_interview_plan(
    *,
    work_experience: list[dict[str, Any]] | None = None,
    skills: list[str] | None = None,
    skill_evidence: list[dict[str, Any]] | None = None,
    education: list[dict[str, Any]] | None = None,
    role: str,
    level: str,
    job_description: str = "",
    retrieve: KnowledgeRetriever = _default_retrieve,
    max_rounds: int = 5,
) -> dict[str, Any]:
    """Create bounded rounds; every round points to one resume evidence item."""

    work_entries = [
        (index, entry)
        for index, entry in enumerate(work_experience or [])
        if isinstance(entry, dict)
        and any(
            str(entry.get(field, "")).strip()
            for field in ("name", "position", "jobDescription")
        )
    ]
    usable_experience = [entry for _, entry in work_entries]
    education_entries = _education_evidence(education)
    skill_entries = _skill_evidence(skills, skill_evidence)
    evidence = usable_experience + education_entries + skill_entries
    evidence_entries = list(enumerate(evidence))
    role_skills = [
        str(entry["name"])
        for entry in skill_entries
        if entry.get("skill_scope") in {"demonstrated", "strong"}
    ]
    role_inference = infer_candidate_role(skills=role_skills, work_experience=usable_experience)
    candidate_role = role_inference["effective_role"]
    candidate_level = _candidate_level(usable_experience)
    if candidate_level == "Unknown" and education_entries:
        candidate_level = "Entry"
    role_mismatch = candidate_role == "Unknown" or candidate_role.casefold() != role.casefold()
    level_conflict = candidate_level.casefold() != level.casefold()
    effective_level = _legacy_level(candidate_level, level)
    difficulty = DIFFICULTY_BY_LEVEL.get(effective_level.casefold(), "medium")
    rounds: list[dict[str, Any]] = []
    for evidence_index, entry in evidence_entries[:max_rounds]:
        description = str(entry.get("jobDescription", "")).strip()
        query = "\n".join(
            part
            for part in (
                f"Target role: {role}",
                f"Experience: {entry.get('name', '')}",
                f"Position: {entry.get('position', '')}",
                description,
                f"Target job description: {job_description}" if job_description.strip() else "",
            )
            if part.strip()
        )
        knowledge = (
            retrieve(query, role, 3)
            if description and entry.get("type") in {"Work", "Project"} and not role_mismatch
            else []
        )
        topic = _topic_for(entry, knowledge)
        entry_type = str(entry.get("type", "")).casefold()
        evidence_label = "experience"
        if entry_type == "education":
            evidence_label = "education background"
        elif entry_type == "skill":
            evidence_label = f"{_candidate_scope(entry).casefold()} skill knowledge"
        objective = f"Validate the candidate's {topic} {evidence_label} for {role}."
        reasoning = (
            f"Grounded in {_candidate_scope(entry)} evidence from "
            f"{entry.get('name', 'the resume')}."
        )
        if role_mismatch:
            objective = (
                f"Validate transferable {topic} evidence for the target {role} role "
                f"without assuming {role} experience."
            )
            reasoning = (
                f"Role mismatch: candidate evidence aligns with {candidate_role}, while the target role is {role}. "
                f"Grounded in {_candidate_scope(entry)} evidence from "
                f"{entry.get('name', 'the resume')}."
            )
        rounds.append(
            {
                "round_id": f"round-{len(rounds) + 1}",
                "evidence_index": evidence_index,
                "role": candidate_role,
                "level": effective_level,
                "candidate_role": candidate_role,
                "candidate_level": candidate_level,
                "target_role": role,
                "target_level": level,
                "level_conflict": level_conflict,
                "role_confidence": role_inference["confidence"],
                "role_conflict": role_inference["conflict"],
                "candidate_scope": _candidate_scope(entry),
                "evidence": entry,
                "topic": topic,
                "difficulty": difficulty,
                "objective": objective,
                "reasoning": reasoning,
                "knowledge": knowledge,
            }
        )

    return {
        "role": role,
        "level": level,
        "target_role": role,
        "target_level": level,
        "candidate_role": candidate_role,
        "candidate_level": candidate_level,
        "level_conflict": level_conflict,
        "role_inference": role_inference,
        "skills": list(skills or []),
        "skill_evidence": list(skill_evidence or []),
        "education": list(education or []),
        "rounds": rounds,
        "coverage_goals": [
            f"Validate role-relevant implementation decisions for {role}.",
            "Verify concrete resume claims with mechanisms, trade-offs, and failure cases.",
        ],
    }
