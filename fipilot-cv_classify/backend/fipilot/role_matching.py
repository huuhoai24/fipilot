"""Deterministic, evidence-based matching between resume content and interview roles."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from fipilot.role_catalog import ROLE_CATALOG

ROLE_TAXONOMY = ROLE_CATALOG


def _normalize(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return re.sub(r"\s+", " ", text).strip()


def _contains(text: str, keyword: str) -> bool:
    return re.search(rf"(?<![\w]){re.escape(keyword)}(?![\w])", text) is not None


def _matched_keywords(text: str, keywords: tuple[str, ...]) -> set[str]:
    return {keyword for keyword in keywords if _contains(text, keyword)}


def _allocate_percentages(raw_scores: list[int]) -> list[int]:
    total = sum(raw_scores)
    exact = [score * 100 / total for score in raw_scores]
    result = [int(value) for value in exact]
    remaining = 100 - sum(result)
    order = sorted(range(len(exact)), key=lambda index: exact[index] - result[index], reverse=True)
    for index in order[:remaining]:
        result[index] += 1
    return result


def _role_signal_scores(
    *,
    skills: list[str],
    work_experience: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Keep title and demonstrated-task signals separate for grounded role inference."""

    clean_skills = [str(skill).strip() for skill in skills if str(skill).strip()]
    normalized_skills = {_normalize(skill): skill for skill in clean_skills}
    signals: dict[str, dict[str, Any]] = {}
    for role in ROLE_TAXONOMY:
        keywords = role["keywords"]
        matched_skills = [
            original
            for normalized, original in normalized_skills.items()
            if any(_contains(normalized, keyword) or _contains(keyword, normalized) for keyword in keywords)
        ]
        title_hits = 0
        task_hits = len(matched_skills)
        relevant_indexes: list[int] = []
        for index, entry in enumerate(work_experience):
            title = _normalize(entry.get("position"))
            task_text = _normalize(
                f"{entry.get('name', '')} {entry.get('jobDescription', '')}"
            )
            entry_title_hits = _matched_keywords(title, keywords)
            entry_task_hits = _matched_keywords(task_text, keywords)
            title_hits += len(entry_title_hits)
            task_hits += len(entry_task_hits)
            if entry_title_hits or entry_task_hits:
                relevant_indexes.append(index)
        signals[role["id"]] = {
            "role": role,
            "title_hits": title_hits,
            "task_hits": task_hits,
            "matched_skills": matched_skills,
            "relevant_indexes": relevant_indexes,
        }
    return signals


def _best_role(signals: dict[str, dict[str, Any]], signal_name: str) -> tuple[str | None, int]:
    candidates = [
        signal
        for signal in signals.values()
        if signal[signal_name] > 0
    ]
    if not candidates:
        return None, 0
    best = sorted(
        candidates,
        key=lambda signal: (-signal[signal_name], signal["role"]["title"]),
    )[0]
    return best["role"]["title"], best[signal_name]


def infer_candidate_role(
    *,
    skills: list[str],
    work_experience: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return candidate role provenance without treating an interview target as evidence."""

    signals = _role_signal_scores(skills=skills, work_experience=work_experience)
    title_role, title_strength = _best_role(signals, "title_hits")
    task_role, task_strength = _best_role(signals, "task_hits")
    conflict = bool(title_role and task_role and title_role != task_role)
    # A single broad task keyword (for example, React) is not enough to erase an
    # equally explicit title. Multiple demonstrated task signals resolve a conflict.
    task_dominates_title = not conflict or task_strength > title_strength
    effective_role = (
        task_role
        if task_role and (title_role is None or task_dominates_title)
        else title_role or "Unknown"
    )
    strength = task_strength if effective_role == task_role else title_strength
    confidence = "none" if strength == 0 else "high" if strength >= 2 else "medium"
    return {
        "title_role": title_role,
        "task_role": task_role,
        "effective_role": effective_role,
        "confidence": confidence,
        "conflict": conflict,
    }


def match_resume_roles(
    *,
    skills: list[str],
    work_experience: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return role evidence shares; scores describe resume evidence, not hiring odds."""

    matches: list[dict[str, Any]] = []
    for signal in _role_signal_scores(
        skills=skills,
        work_experience=work_experience,
    ).values():
        # Demonstrated tasks are stronger evidence than a conflicting job title.
        score = signal["title_hits"] * 2 + signal["task_hits"] * 4
        if score > 0:
            matches.append(
                {
                    "id": signal["role"]["id"],
                    "title": signal["role"]["title"],
                    "rawScore": score,
                    "matchedSkills": signal["matched_skills"],
                    "relevantExperienceIndexes": signal["relevant_indexes"],
                }
            )

    if not matches:
        return []

    matches.sort(key=lambda match: (-match["rawScore"], match["title"]))
    percentages = _allocate_percentages([match["rawScore"] for match in matches])
    for match, percentage in zip(matches, percentages, strict=True):
        match["score"] = percentage
        match["summary"] = (
            f"{len(match['matchedSkills'])} matched skills and "
            f"{len(match['relevantExperienceIndexes'])} relevant experience items"
        )
        del match["rawScore"]
    return matches
