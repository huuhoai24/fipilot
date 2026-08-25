from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

from evaluation.ragas_pilot.dataset import ControlledCaseSpec


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from services.interview_knowledge.local import LocalKnowledgeRetriever  # noqa: E402
from shared.schemas import CandidateProfile, InterviewConfig  # noqa: E402


YEARS_BY_LEVEL = {"intern": 0.5, "junior": 1.5, "middle": 4.0, "senior": 8.0}


def build_synthetic_profile(spec: ControlledCaseSpec) -> CandidateProfile:
    anchor = spec.anchors[0] if spec.anchors else spec.topic_title
    return CandidateProfile(
        name=f"Synthetic Candidate {spec.sample_id}",
        recent_role=spec.candidate_role,
        specialization=spec.candidate_role,
        years_experience=YEARS_BY_LEVEL[spec.candidate_level],
        skills=[spec.topic_title, *spec.anchors[:2]],
        skill_evidence=[
            {
                "skill": spec.topic_title,
                "evidence": [
                    f"Synthetic controlled project evidence covering {anchor}."
                ],
                "source_section": "synthetic_controlled",
            }
        ],
        projects=[
            {
                "name": f"Controlled {spec.topic_title} project",
                "description": (
                    f"Synthetic controlled implementation focused on {anchor}."
                ),
                "technologies": [spec.topic_title],
                "role": spec.candidate_role,
            }
        ],
        confidence=1.0,
        extraction_method="synthetic_controlled",
    )


def build_interview_config(spec: ControlledCaseSpec) -> InterviewConfig:
    return InterviewConfig(
        experience_level=spec.candidate_level,
        language=spec.language,
        interview_style="technical",
        question_count=3,
        objective=f"Evaluate implementation decisions for {spec.topic_title}",
    )


def _topic_context_index(catalog_path: Path, domain_key: str) -> dict[str, str]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    entries = catalog.get("domains", {}).get(domain_key, [])
    for entry in entries:
        title = str(entry.get("title", ""))
        path_values = [str(value) for value in entry.get("path", [])]
        path = " > ".join([*path_values, title])
        anchors = "; ".join(str(value) for value in entry.get("anchors", [])[:5])
        text = f"Candidate-aligned topic: {path}"
        if anchors:
            text += f" | anchors: {anchors}"
        topic_id = "::".join((domain_key, *path_values, title))
        result[text] = topic_id
    return result


def _context_id(text: str) -> str:
    return "ctx-" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def evaluate_retrieval_spec(
    spec: ControlledCaseSpec,
    catalog_path: Path,
) -> dict[str, Any]:
    profile = build_synthetic_profile(spec)
    config = build_interview_config(spec)
    retriever = LocalKnowledgeRetriever(catalog_path=catalog_path, topic_limit=8)
    started = time.perf_counter()
    raw_contexts = retriever.retrieve_topics(profile, config)
    latency_ms = (time.perf_counter() - started) * 1000
    topic_index = _topic_context_index(catalog_path, spec.domain_key)

    contexts: list[dict[str, Any]] = []
    topic_rank = 0
    expected_topic_rank: int | None = None
    for rank, text in enumerate(raw_contexts, start=1):
        if text.startswith("Domain: "):
            context_type = "domain"
            topic_id = None
            current_topic_rank = None
        elif text.startswith("Level guidance: "):
            context_type = "level_guidance"
            topic_id = None
            current_topic_rank = None
        else:
            context_type = "topic"
            topic_rank += 1
            current_topic_rank = topic_rank
            topic_id = topic_index.get(text)
            if topic_id == spec.expected_topic_id:
                expected_topic_rank = topic_rank
        contexts.append(
            {
                "rank": rank,
                "topic_rank": current_topic_rank,
                "context_id": _context_id(text),
                "topic_id": topic_id,
                "context_type": context_type,
                "text": text,
                "similarity": None,
            }
        )

    query = (
        f"Role: {spec.candidate_role}; level: {spec.candidate_level}; "
        f"skills: {', '.join(profile.skills)}; objective: {config.objective}"
    )
    return {
        "sample_id": "rag-" + spec.sample_id.removeprefix("pilot-"),
        "source_type": spec.source_type,
        "candidate_role": spec.candidate_role,
        "candidate_level": spec.candidate_level,
        "candidate_skills": profile.skills,
        "candidate_profile": profile.model_dump(mode="json"),
        "interview_config": config.model_dump(mode="json"),
        "query": query,
        "query_construction": (
            "human-readable projection of the CandidateProfile strings and "
            "InterviewConfig; production retrieval consumes those objects directly"
        ),
        "retrieval_implementation": "LocalKnowledgeRetriever",
        "knowledge_source": "backend/services/interview_knowledge/catalog.json",
        "embedding_model": None,
        "vector_database": None,
        "topic_top_k": 8,
        "similarity_metric": "weighted_lexical_token_overlap",
        "production_score_exposed": False,
        "retrieved_contexts": contexts,
        "latency_ms": latency_ms,
        "controlled_reference": {
            "classification": "synthetic controlled retrieval test",
            "expected_topic_id": spec.expected_topic_id,
            "expected_topic_source": "actual catalog metadata",
            "expected_topic_rank": expected_topic_rank,
            "hit_at_8": expected_topic_rank is not None and expected_topic_rank <= 8,
            "recall_at_8": 1.0
            if expected_topic_rank is not None and expected_topic_rank <= 8
            else 0.0,
            "mrr_at_8": 1.0 / expected_topic_rank
            if expected_topic_rank is not None and expected_topic_rank <= 8
            else 0.0,
        },
        "reference_based_context_recall": {
            "value": None,
            "reason": (
                "No human-reviewed reference contexts or reference answers are "
                "available in this pilot."
            ),
        },
    }
