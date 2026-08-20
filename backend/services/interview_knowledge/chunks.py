from __future__ import annotations

import hashlib
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


@dataclass(frozen=True)
class KnowledgeChunk:
    document_id: str
    topic_id: str
    domain_key: str
    domain_label: str
    path: tuple[str, ...]
    title: str
    anchors: tuple[str, ...]
    content: str
    content_sha256: str


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_catalog_chunks(catalog_path: Path) -> list[KnowledgeChunk]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    chunks: list[KnowledgeChunk] = []
    for domain_key in sorted(catalog.get("domains", {})):
        domain_label = DOMAIN_LABELS.get(
            domain_key, domain_key.replace("_", " ")
        )
        entries = catalog["domains"][domain_key]
        for entry in entries:
            title = str(entry.get("title", "")).strip()
            if not title:
                continue
            path = tuple(str(value).strip() for value in entry.get("path", []))
            anchors = tuple(
                str(value).strip()
                for value in entry.get("anchors", [])
                if str(value).strip()
            )
            topic_id = "::".join((domain_key, *path, title))
            topic_path = " > ".join((*path, title))
            content = f"Role: {domain_label}\nTopic: {topic_path}"
            if anchors:
                content += "\nInterview anchors: " + "; ".join(anchors)
            chunks.append(
                KnowledgeChunk(
                    document_id=_sha256(topic_id)[:32],
                    topic_id=topic_id,
                    domain_key=domain_key,
                    domain_label=domain_label,
                    path=path,
                    title=title,
                    anchors=anchors,
                    content=content,
                    content_sha256=_sha256(content),
                )
            )
    return chunks
