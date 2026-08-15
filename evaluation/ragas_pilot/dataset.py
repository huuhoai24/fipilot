from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


DOMAIN_LABELS = {
    "AI_Engineer": "AI Engineer",
    "Backend_Developer": "Backend Developer",
    "Business_Analyst": "Business Analyst",
    "Data_Engineer": "Data Engineer",
    "Data_Scientist": "Data Scientist",
    "DevOps_Engineer": "DevOps Engineer",
    "Full_Stack_Developer": "Full Stack Developer",
    "Software_Engineer": "Software Engineer",
    "Tester_QA_QC": "Tester / QA / QC",
    "Web_Developer": "Web Developer",
}
LEVELS = ("intern", "junior", "middle", "senior")
LANGUAGES = ("vi", "en")


@dataclass(frozen=True)
class ControlledCaseSpec:
    sample_id: str
    source_type: str
    domain_key: str
    candidate_role: str
    candidate_level: str
    language: str
    topic_title: str
    topic_path: tuple[str, ...]
    anchors: tuple[str, ...]
    expected_topic_id: str


def _topic_id(domain: str, title: str, path: tuple[str, ...]) -> str:
    return "::".join((domain, *path, title))


def build_controlled_case_specs(
    catalog_path: Path,
    *,
    limit: int = 30,
) -> list[ControlledCaseSpec]:
    if limit < 1:
        return []
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    domains: dict[str, list[dict[str, object]]] = catalog.get("domains", {})
    selected: list[ControlledCaseSpec] = []
    candidates_by_domain: dict[str, list[dict[str, object]]] = {}
    for domain_key in sorted(domains):
        candidates = [
            entry
            for entry in domains[domain_key]
            if entry.get("title") and entry.get("anchors")
        ]
        candidates.sort(
            key=lambda entry: (
                str(entry.get("title", "")).lower(),
                tuple(str(value) for value in entry.get("path", [])),
            )
        )
        candidates_by_domain[domain_key] = candidates

    round_index = 0
    while len(selected) < limit:
        added = False
        for domain_key in sorted(candidates_by_domain):
            candidates = candidates_by_domain[domain_key]
            if round_index >= len(candidates):
                continue
            entry = candidates[round_index]
            title = str(entry["title"])
            path = tuple(str(value) for value in entry.get("path", []))
            anchors = tuple(str(value) for value in entry.get("anchors", [])[:5])
            sequence = len(selected) + 1
            selected.append(
                ControlledCaseSpec(
                    sample_id=f"pilot-{sequence:03d}",
                    source_type="synthetic_controlled",
                    domain_key=domain_key,
                    candidate_role=DOMAIN_LABELS.get(
                        domain_key, domain_key.replace("_", " ")
                    ),
                    candidate_level=LEVELS[(sequence - 1) % len(LEVELS)],
                    language=LANGUAGES[(sequence - 1) % len(LANGUAGES)],
                    topic_title=title,
                    topic_path=path,
                    anchors=anchors,
                    expected_topic_id=_topic_id(domain_key, title, path),
                )
            )
            added = True
            if len(selected) == limit:
                break
        if not added:
            break
        round_index += 1
    return selected
