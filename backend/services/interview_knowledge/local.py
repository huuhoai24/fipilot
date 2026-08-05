from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from shared.schemas import CandidateProfile, InterviewConfig


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

DOMAIN_TERMS = {
    "AI_Engineer": (
        "ai engineer machine learning deep learning computer vision nlp llm rag pytorch "
        "tensorflow yolo model inference artificial intelligence"
    ),
    "Backend_Developer": "backend server api fastapi django flask spring node database microservice",
    "Business_Analyst": "business analyst requirement stakeholder process user story",
    "Data_Engineer": "data engineer etl elt spark airflow kafka warehouse pipeline",
    "Data_Scientist": "data scientist statistics analytics experiment pandas modeling",
    "DevOps_Engineer": "devops sre kubernetes docker terraform ci cd cloud observability",
    "Full_Stack_Developer": "full stack frontend backend react node api database",
    "Software_Engineer": "software engineer design pattern algorithm architecture programming",
    "Tester_QA_QC": "tester qa qc quality assurance test automation selenium playwright",
    "Web_Developer": "web developer frontend javascript typescript html css react vue angular",
}

STOP_WORDS = {
    "and",
    "the",
    "with",
    "from",
    "for",
    "using",
    "engineer",
    "developer",
    "project",
    "built",
    "worked",
    "experience",
}


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9+#.]+", value.lower())
        if len(token) >= 2 and token not in STOP_WORDS
    }


def _profile_text(profile: CandidateProfile) -> str:
    payload = profile.model_dump(mode="json")
    values: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, str):
            values.append(value)
        elif isinstance(value, dict):
            for nested in value.values():
                collect(nested)
        elif isinstance(value, list):
            for nested in value:
                collect(nested)

    collect(payload)
    return " ".join(values)


class LocalKnowledgeRetriever:
    def __init__(self, catalog_path: Path | None = None, topic_limit: int = 8):
        self.catalog_path = catalog_path or Path(__file__).with_name("catalog.json")
        self.topic_limit = topic_limit
        self._catalog = json.loads(self.catalog_path.read_text(encoding="utf-8"))

    def retrieve_topics(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig,
    ) -> list[str]:
        profile_text = _profile_text(candidate_profile)
        profile_tokens = _tokens(profile_text)
        domain_key = self._select_domain(profile_text, profile_tokens)
        domain_label = DOMAIN_LABELS.get(domain_key, domain_key.replace("_", " "))
        results = [f"Domain: {domain_label}"]

        level_name = interview_config.experience_level.title()
        level_guidance = (
            self._catalog.get("levels", {}).get(domain_key, {}).get(level_name, [])
        )
        if level_guidance:
            results.append("Level guidance: " + "; ".join(level_guidance[:10]))

        scored_topics = []
        for entry in self._catalog.get("domains", {}).get(domain_key, []):
            searchable = " ".join(
                [entry.get("title", ""), *entry.get("path", []), *entry.get("anchors", [])]
            )
            entry_tokens = _tokens(searchable)
            overlap = profile_tokens & entry_tokens
            score = sum(3 if len(token) >= 5 else 1 for token in overlap)
            title = entry.get("title", "")
            if title and title.lower() in profile_text.lower():
                score += 12
            if score > 0:
                scored_topics.append((score, title.lower(), entry))

        scored_topics.sort(key=lambda item: (-item[0], item[1]))
        for _, _, entry in scored_topics[: self.topic_limit]:
            path = " > ".join([*entry.get("path", []), entry.get("title", "")])
            anchors = "; ".join(entry.get("anchors", [])[:5])
            detail = f"Candidate-aligned topic: {path}"
            if anchors:
                detail += f" | anchors: {anchors}"
            results.append(detail)
        return results

    def _select_domain(self, profile_text: str, profile_tokens: set[str]) -> str:
        available_domains = self._catalog.get("domains", {})
        scored_domains: list[tuple[int, str]] = []
        lowered = profile_text.lower()
        for domain_key in available_domains:
            label = DOMAIN_LABELS.get(domain_key, domain_key.replace("_", " ")).lower()
            score = 20 if label in lowered else 0
            score += len(profile_tokens & _tokens(DOMAIN_TERMS.get(domain_key, label))) * 3
            scored_domains.append((score, domain_key))
        scored_domains.sort(key=lambda item: (-item[0], item[1]))
        if not scored_domains:
            raise ValueError("The interview knowledge catalog contains no domains")
        return scored_domains[0][1]
