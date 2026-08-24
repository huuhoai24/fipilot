import json
import unicodedata
from pathlib import Path
from typing import Any

from fipilot.model.llm_client import LLMClient
from fipilot.pdf_text_extractor import extract_indexed_text_from_pdf
from fipilot.role_matching import match_resume_roles
from fipilot.utils.index_text import IndexedTextResolver

MAX_RESUME_CONTEXT_CHARS = 48_000
_SKILL_SCOPES = {"familiarity", "demonstrated", "strong", "unknown"}
_SKILL_SOURCES = {"resume", "work", "project"}
_EDUCATION_FIELDS = ("institution", "degree", "field_of_study", "start_date", "end_date")


def _take_indexed_lines(
    entries: list[tuple[int, str]],
    budget: int,
) -> dict[int, str]:
    selected: dict[int, str] = {}
    used = 0
    for index, value in entries:
        separator_size = 1 if selected else 0
        prefix = f"[{index}]: "
        available = budget - used - separator_size - len(prefix)
        if available <= 0:
            break
        selected[index] = value[:available]
        used += separator_size + len(prefix) + len(selected[index])
        if len(selected[index]) < len(value):
            break
    return selected


def _bounded_resume_context(
    resume_text: str,
    index_map: dict[int, str],
) -> tuple[str, dict[int, str]]:
    if len(resume_text) <= MAX_RESUME_CONTEXT_CHARS:
        return resume_text, index_map

    entries = list(index_map.items())
    head_budget = MAX_RESUME_CONTEXT_CHARS * 2 // 3
    tail_budget = MAX_RESUME_CONTEXT_CHARS - head_budget - 1
    selected = _take_indexed_lines(entries, head_budget)
    tail = _take_indexed_lines(
        [(index, value) for index, value in reversed(entries) if index not in selected],
        tail_budget,
    )
    selected.update(tail)
    bounded_map = dict(sorted(selected.items()))
    bounded_text = "\n".join(
        f"[{index}]: {value}" for index, value in bounded_map.items()
    )
    return bounded_text, bounded_map


class ResumeExtract:
    """Extract interview context from text-based PDF resumes.

    PyMuPDF supplies the document text and Azure OpenAI turns that text into the
    existing frontend contract. No image rendering or layout model is involved.
    """

    def __init__(self, llm_client: LLMClient | None = None):
        self.llm_client = llm_client

    def llm_analyzer(self, resume_text: str, resume_id: str) -> dict[str, Any]:
        client = self.llm_client or LLMClient()
        result = client.extract_info(
            text_content=resume_text,
            extract_types=["work_experience"],
            resume_id=resume_id,
        )
        if not isinstance(result, dict):
            raise ValueError("Resume analysis returned an invalid JSON object")
        if not isinstance(result.get("workExperience"), list):
            raise ValueError("Resume analysis did not return workExperience")
        if not isinstance(result.get("skills", []), list):
            raise ValueError("Resume analysis returned invalid skills")
        if not isinstance(result.get("skillEvidence", []), list):
            raise ValueError("Resume analysis returned invalid skillEvidence")
        if not isinstance(result.get("education", []), list):
            raise ValueError("Resume analysis returned invalid education")
        return result

    @staticmethod
    def _normalize_skill_evidence(
        raw_evidence: list[Any],
        skills: list[str],
    ) -> list[dict[str, str]]:
        evidence_by_skill: dict[str, dict[str, str]] = {}
        display_skill_by_key: dict[str, str] = {
            unicodedata.normalize("NFC", skill).casefold(): skill for skill in skills
        }
        for item in raw_evidence:
            if not isinstance(item, dict):
                continue
            skill = item.get("skill")
            if not isinstance(skill, str) or not skill.strip():
                continue
            clean_skill = skill.strip()
            key = unicodedata.normalize("NFC", clean_skill).casefold()
            display_skill_by_key.setdefault(key, clean_skill)
            scope = str(item.get("scope", "unknown")).strip().casefold()
            source = str(item.get("source", "resume")).strip().casefold()
            evidence_by_skill.setdefault(
                key,
                {
                    "skill": display_skill_by_key[key],
                    "scope": scope if scope in _SKILL_SCOPES else "unknown",
                    "source": source if source in _SKILL_SOURCES else "resume",
                },
            )

        for skill in skills:
            key = unicodedata.normalize("NFC", skill).casefold()
            evidence_by_skill.setdefault(
                key,
                {"skill": skill, "scope": "unknown", "source": "resume"},
            )
        return list(evidence_by_skill.values())

    @staticmethod
    def _normalize_education(raw_education: list[Any]) -> list[dict[str, str]]:
        education: list[dict[str, str]] = []
        for item in raw_education:
            if not isinstance(item, dict):
                continue
            normalized = {
                field: value.strip()
                for field in _EDUCATION_FIELDS
                if isinstance((value := item.get(field)), str) and value.strip()
            }
            if normalized.get("institution") or normalized.get("degree") or normalized.get("field_of_study"):
                education.append(normalized)
        return education

    def pipeline(self, pdf_path: str | Path) -> str:
        path = Path(pdf_path)
        resume_text, index_map = extract_indexed_text_from_pdf(path)
        resume_text, index_map = _bounded_resume_context(resume_text, index_map)
        result = self.llm_analyzer(resume_text, path.stem)
        normalized_entries = []
        for entry in result["workExperience"]:
            if not isinstance(entry, dict):
                raise ValueError("Resume analysis returned an invalid workExperience entry")

            entry_type = entry.get("type")
            name = entry.get("name")
            position = entry.get("position", "")
            index_range = entry.get("description_refer_index_range", [])
            if entry_type not in {"Work", "Project"}:
                raise ValueError("Resume analysis returned an invalid workExperience type")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Resume analysis returned a workExperience entry without a name")
            if not isinstance(position, str):
                raise ValueError("Resume analysis returned an invalid workExperience position")
            if index_range != [] and (
                not isinstance(index_range, list)
                or len(index_range) != 2
                or not all(isinstance(index, int) for index in index_range)
                or index_range[0] > index_range[1]
                or index_range[0] not in index_map
                or index_range[1] not in index_map
            ):
                raise ValueError("Resume analysis returned an invalid evidence index range")

            normalized_entry = {
                "type": entry_type,
                "name": name.strip(),
                "position": position.strip(),
                "description_refer_index_range": index_range,
            }
            normalized_entry = IndexedTextResolver.resolve(normalized_entry, index_map)
            normalized_entry.setdefault("jobDescription", "")
            normalized_entries.append(normalized_entry)

        skills = []
        seen_skills = set()
        for skill in result.get("skills", []):
            if not isinstance(skill, str) or not skill.strip():
                continue
            clean_skill = skill.strip()
            normalized_skill = unicodedata.normalize("NFC", clean_skill).casefold()
            if normalized_skill not in seen_skills:
                skills.append(clean_skill)
                seen_skills.add(normalized_skill)

        skill_evidence = self._normalize_skill_evidence(
            result.get("skillEvidence", []),
            skills,
        )
        education = self._normalize_education(result.get("education", []))

        if not normalized_entries and not skill_evidence and not education:
            raise ValueError("No work or project evidence was found in the resume")

        role_matches = match_resume_roles(
            skills=skills,
            work_experience=normalized_entries,
        )

        return json.dumps(
            {
                "skills": skills,
                "skillEvidence": skill_evidence,
                "education": education,
                "workExperience": normalized_entries,
                "roleMatches": role_matches,
            },
            indent=2,
            ensure_ascii=False,
        )
