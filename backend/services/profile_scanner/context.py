from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


DEFAULT_MAX_CONTEXT_CHARACTERS = 16_000


@dataclass(frozen=True)
class ResumeSection:
    key: str
    heading: str
    text: str


@dataclass(frozen=True)
class ResumeContext:
    text: str
    total_characters: int
    characters_considered: int
    is_partial: bool
    warnings: tuple[str, ...]
    sections: tuple[ResumeSection, ...]


_ALIASES = {
    "experience": {"experience", "work experience", "professional experience", "employment history", "kinh nghiem", "kinh nghiem lam viec", "qua trinh cong tac"},
    "projects": {"projects", "project experience", "selected projects", "du an", "cac du an"},
    "skills": {"skills", "technical skills", "core skills", "ky nang", "ky nang chuyen mon"},
    "education": {"education", "academic background", "hoc van", "giao duc"},
    "summary": {"summary", "profile", "professional summary", "muc tieu nghe nghiep", "gioi thieu"},
    "certifications": {"certifications", "certificates", "chung chi"},
}
_WEIGHTS = {"experience": 8, "projects": 5, "skills": 4, "education": 2, "summary": 2, "certifications": 1, "identity": 2, "other": 1}


def _fold(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    plain = "".join(character for character in decomposed if not unicodedata.combining(character))
    return re.sub(r"[^a-z0-9]+", " ", plain).strip()


def heading_key(line: str) -> str | None:
    stripped = line.strip().strip(":|-–—")
    if not stripped or len(stripped) > 80:
        return None
    folded = _fold(stripped)
    for key, aliases in _ALIASES.items():
        if folded in aliases:
            return key
    return None


def split_resume_sections(text: str) -> tuple[ResumeSection, ...]:
    sections: list[ResumeSection] = []
    current_key, current_heading, lines = "identity", "IDENTITY", []
    for line in (text or "").splitlines():
        key = heading_key(line)
        if key is None:
            lines.append(line)
            continue
        section_text = "\n".join(lines).strip()
        if section_text:
            sections.append(ResumeSection(current_key, current_heading, section_text))
        current_key, current_heading, lines = key, line.strip(), []
    section_text = "\n".join(lines).strip()
    if section_text:
        sections.append(ResumeSection(current_key, current_heading, section_text))
    return tuple(sections) or (ResumeSection("other", "DOCUMENT", (text or "").strip()),)


def _head_and_tail(value: str, budget: int) -> str:
    if len(value) <= budget:
        return value
    marker = "\n[... section content omitted ...]\n"
    remaining = max(0, budget - len(marker))
    head = remaining // 2
    return value[:head].rstrip() + marker + value[-(remaining - head):].lstrip()


def _compact_repeated_sentences(value: str) -> str:
    parts = re.split(r"(?<=[.!?])\s+|\n+", value)
    normalized = [_fold(part) for part in parts]
    counts = {item: normalized.count(item) for item in set(normalized) if item}
    seen: set[str] = set()
    output: list[str] = []
    omitted = False
    for part, key in zip(parts, normalized, strict=True):
        if counts.get(key, 0) >= 4 and key in seen:
            omitted = True
            continue
        if key:
            seen.add(key)
        if part.strip():
            output.append(part.strip())
    if omitted:
        output.append("[repeated boilerplate omitted]")
    return "\n".join(output)


def build_resume_context(resume_text: str, *, max_characters: int = DEFAULT_MAX_CONTEXT_CHARACTERS) -> ResumeContext:
    text = (resume_text or "").strip()
    sections = split_resume_sections(text)
    if len(text) <= max_characters:
        return ResumeContext(text, len(text), len(text), False, (), sections)
    effective_texts = [_compact_repeated_sentences(section.text) for section in sections]
    headings_cost = sum(len(section.heading) + 2 for section in sections)
    available = max(0, max_characters - headings_cost)
    base = min(256, available // max(1, len(sections)))
    allocations = [min(len(value), base) for value in effective_texts]
    remaining = max(0, available - sum(allocations))
    while remaining:
        candidates = [index for index, value in enumerate(effective_texts) if allocations[index] < len(value)]
        if not candidates:
            break
        total_weight = sum(_WEIGHTS.get(sections[index].key, 1) for index in candidates)
        before = remaining
        for index in candidates:
            share = max(1, remaining * _WEIGHTS.get(sections[index].key, 1) // total_weight)
            increment = min(share, len(effective_texts[index]) - allocations[index], remaining)
            allocations[index] += increment
            remaining -= increment
            if remaining == 0:
                break
        if remaining == before:
            break
    rendered = [f"{section.heading}\n{_head_and_tail(effective_texts[index], allocations[index])}" for index, section in enumerate(sections)]
    context_text = "\n\n".join(rendered)[:max_characters]
    return ResumeContext(context_text, len(text), len(context_text), True, ("content_omitted",), sections)
