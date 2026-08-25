from __future__ import annotations

import asyncio
import hashlib
import json
import math
import re
import statistics
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from evaluation.cv_question_rag.cache import JsonCache
from evaluation.cv_question_rag.cost import estimate_cost
from evaluation.cv_question_rag.metrics import duplicate_statistics, grounding_overlap
from evaluation.cv_question_rag.production_prompt import production_base_prompt
from evaluation.cv_question_rag.prompts import (
    JUDGE_SYSTEM_INSTRUCTION,
    RUBRIC_VERSION,
    build_evaluation_question_prompt,
)
from evaluation.cv_question_rag.schemas import GeneratedQuestion, QualityJudgment


QUESTION_MODEL = "gemini-2.5-flash"
JUDGE_MODEL = "gemini-2.5-pro"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
        ),
        encoding="utf-8",
    )


def _hash(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _normalized_text(value: str) -> str:
    return " ".join(
        re.findall(r"[\w+#.]+", unicodedata.normalize("NFKC", value).casefold())
    )


def _unsupported_experience_assumption(question: str) -> bool:
    normalized = _normalized_text(question)
    patterns = (
        r"\bin your projects?\b",
        r"\bin your experience\b",
        r"\byou (?:have )?(?:used|built|implemented|deployed|applied)\b",
        r"\bwhen you (?:used|built|implemented|deployed|applied)\b",
        r"\btrong (?:các )?dự án của bạn\b",
        r"\bkinh nghiệm của bạn\b",
        r"\bbạn đã\b",
        r"\bbạn từng\b",
    )
    return any(re.search(pattern, normalized) for pattern in patterns)


def _balanced_limit(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["domain"]].append(row)
    for values in grouped.values():
        values.sort(key=lambda row: row["resume_id"])
    selected: list[dict[str, Any]] = []
    while len(selected) < min(limit, len(rows)):
        progressed = False
        for domain in sorted(grouped):
            if grouped[domain] and len(selected) < limit:
                selected.append(grouped[domain].pop(0))
                progressed = True
        if not progressed:
            break
    return selected


def _scenario(case: dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(
        scenario_id=f"Q-{case['resume_id']}",
        candidate_profile=case["candidate_profile"],
        role=case["domain"].replace("_", " "),
        domain=case["domain"],
        level=case["level"],
        language=case["language"],
        interview_objective="Evaluate Resume-derived technical decisions and trade-offs",
        target_topic=case["target_topic"],
        question_type="experience_based",
        previous_questions=[],
        question_position=1,
    )


def _judge_prompt(
    case: dict[str, Any], question: dict[str, Any], contexts: list[dict[str, Any]]
) -> str:
    evidence = {
        "resume_id": case["resume_id"],
        "derived_candidate_profile": case["candidate_profile"],
        "expected_domain": case["domain"],
        "expected_level": case["level"],
        "expected_language": case["language"],
        "target_topic": case["target_topic"],
        "question": question,
        "retrieved_contexts": contexts,
    }
    return f"""Locked rubric: {RUBRIC_VERSION}

Evaluate this one current-production lexical-RAG question.
- technical_validity, role_relevance, cv_alignment, answerability, non_redundancy: 0 or 1.
- difficulty_label: Intern, Junior, Middle, or Senior; difficulty_score: 1 to 5.
- clarity: 1 to 5; specificity: 0 to 2; rag_grounding: 0 to 2.
- knowledge_false_premise: 1 only for a technically false premise.
- grounding_chunk_ids may cite only chunk_id values supplied in retrieved_contexts.
- Resume-derived catalog skills are evidence of skill mention, not proof of proficiency.

Evidence:
{json.dumps(evidence, ensure_ascii=False)}
"""


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"sample_count": 0}
    judgments = [row["judgment"] for row in rows]
    return {
        "sample_count": len(rows),
        "technical_validity_rate": statistics.fmean(
            value["technical_validity"] for value in judgments
        ),
        "role_relevance_rate": statistics.fmean(
            value["role_relevance"] for value in judgments
        ),
        "cv_alignment_rate": statistics.fmean(value["cv_alignment"] for value in judgments),
        "answerability_rate": statistics.fmean(value["answerability"] for value in judgments),
        "false_premise_rate": statistics.fmean(
            value["knowledge_false_premise"] for value in judgments
        ),
        "mean_difficulty_score": statistics.fmean(
            value["difficulty_score"] for value in judgments
        ),
        "mean_clarity": statistics.fmean(value["clarity"] for value in judgments),
        "mean_specificity": statistics.fmean(value["specificity"] for value in judgments),
        "mean_rag_grounding": statistics.fmean(value["rag_grounding"] for value in judgments),
    }


def _grouped(rows: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row[field])].append(row)
    return {key: _aggregate(values) for key, values in sorted(groups.items())}


def plan_question_run(
    *,
    repo_root: Path,
    dataset_path: Path,
    retrieval_path: Path,
    max_cases: int = 150,
) -> dict[str, Any]:
    """Estimate provider calls and cost before any external request is made."""
    dataset = _balanced_limit(_read_jsonl(dataset_path), max_cases)
    retrieval_by_id = {row["resume_id"]: row for row in _read_jsonl(retrieval_path)}
    question_input_tokens = 0
    for case in dataset:
        retrieval = retrieval_by_id.get(case["resume_id"])
        if retrieval is None:
            raise ValueError(f"Missing retrieval row for {case['resume_id']}")
        base_prompt, _ = production_base_prompt(repo_root, _scenario(case))
        prompt = build_evaluation_question_prompt(
            base_prompt, retrieval.get("retrieved_contexts", [])
        )
        question_input_tokens += max(1, len(prompt) // 4)
    estimate = estimate_cost(
        base_scenarios=len(dataset),
        question_calls=len(dataset),
        judge_calls=len(dataset),
        repeatability_calls=0,
        embedding_calls=0,
        cached_calls=0,
        flash_input_tokens=question_input_tokens,
        flash_output_tokens=len(dataset) * 300,
        pro_input_tokens=len(dataset) * 3_000,
        pro_output_tokens=len(dataset) * 700,
        embedding_input_tokens=0,
    )
    estimate.update(
        {
            "status": "QUESTION BUDGET GATE PASS",
            "question_condition": "CURRENT_PRODUCTION_LEXICAL",
            "privacy": "Only redacted Candidate Profiles and public knowledge contexts are sent.",
        }
    )
    return estimate


def create_azure_provider(repo_root: Path):
    from dotenv import load_dotenv
    import os

    load_dotenv(repo_root / "fipilot-cv_classify/backend/.env", override=False)
    load_dotenv(repo_root / "backend/.env", override=False)
    from evaluation.cv_question_rag.provider import AzureOpenAIJsonClient

    base_url = os.environ.get("AZURE_OPENAI_BASE_URL", "https://hoai-openai-test-2026-55ac1.openai.azure.com/openai/v1/")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    return AzureOpenAIJsonClient(
        base_url=base_url,
        api_key=api_key,
        max_attempts=15,
        concurrency=1,
    )


def create_vertex_provider(repo_root: Path):
    from dotenv import load_dotenv

    backend = repo_root / "backend"
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))
    load_dotenv(backend / ".env.local", override=False)
    from core.settings import get_settings
    from evaluation.cv_question_rag.provider import VertexJsonClient

    get_settings.cache_clear()
    settings = get_settings()
    return VertexJsonClient(
        project=settings.google_cloud_project or "",
        location=settings.google_cloud_location,
        max_attempts=3,
        concurrency=6,
    )


async def _run_questions(
    *,
    repo_root: Path,
    dataset: list[dict[str, Any]],
    retrieval_by_id: dict[str, dict[str, Any]],
    output_dir: Path,
    provider: Any,
    question_model: str,
    judge_model: str,
) -> dict[str, Any]:
    existing_question_path = output_dir / "questions.jsonl"
    existing_judgment_path = output_dir / "judgments.jsonl"
    existing_questions = {
        row["resume_id"]: row
        for row in (_read_jsonl(existing_question_path) if existing_question_path.exists() else [])
    }
    existing_judgments = {
        row["resume_id"]: row
        for row in (_read_jsonl(existing_judgment_path) if existing_judgment_path.exists() else [])
    }
    question_cache = JsonCache(output_dir / "cache/questions")
    judgment_cache = JsonCache(output_dir / "cache/judgments")

    async def one(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], int]:
        retrieval = retrieval_by_id.get(case["resume_id"])
        if retrieval is None:
            raise ValueError(f"Missing retrieval row for {case['resume_id']}")
        contexts = retrieval.get("retrieved_contexts", [])
        scenario = _scenario(case)
        base_prompt, system_instruction = production_base_prompt(repo_root, scenario)
        question_prompt = build_evaluation_question_prompt(base_prompt, contexts)
        profile_hash = _hash(case["candidate_profile"])
        prompt_hash = _hash(question_prompt)
        previous_question = existing_questions.get(case["resume_id"])
        question_reused = bool(
            previous_question
            and previous_question.get("candidate_profile_hash") == profile_hash
            and previous_question.get("question_prompt_hash") == prompt_hash
            and previous_question.get("model") == question_model
        )
        if question_reused:
            question_row = previous_question
            question = GeneratedQuestion.model_validate(question_row["question"]).model_dump(mode="json")
            question_id = question_row["question_id"]
        else:
            question_cache_key = _hash(
                {
                    "prompt_hash": prompt_hash,
                    "model": question_model,
                    "temperature": 0.2,
                    "schema": "GeneratedQuestion.v1",
                }
            )
            cached_question = question_cache.get(question_cache_key)
            question_cache_hit = cached_question is not None
            if cached_question is None:
                question_result = await provider.generate_json(
                    question_prompt,
                    GeneratedQuestion,
                    model=question_model,
                    temperature=0.2,
                    system_instruction=system_instruction,
                    thinking_budget=0,
                    timeout_seconds=60.0,
                )
                cached_question = {
                    "parsed": question_result.parsed,
                    "raw_provider_output": question_result.raw_provider_output,
                    "usage": question_result.usage,
                    "latency_ms": question_result.latency_ms,
                }
                question_cache.put(question_cache_key, cached_question)
            question = GeneratedQuestion.model_validate(cached_question["parsed"]).model_dump(mode="json")
            question_id = "QUESTION-" + _hash(
                {"resume_id": case["resume_id"], "question": question}
            )[:12].upper()
            question_row = {
                "question_id": question_id,
                "resume_id": case["resume_id"],
                "category": case["category"],
                "domain": case["domain"],
                "level": case["level"],
                "language": case["language"],
                "condition": "CURRENT_PRODUCTION_LEXICAL",
                "target_topic_id": case["target_topic_id"],
                "target_topic": case["target_topic"],
                "candidate_profile_hash": profile_hash,
                "retrieved_contexts": contexts,
                "question": question,
                "question_prompt_hash": prompt_hash,
                "model": question_model,
                "temperature": 0.2,
                "latency_ms": cached_question["latency_ms"],
                "usage": cached_question["usage"],
                "raw_provider_output": cached_question["raw_provider_output"],
                "cache_key": question_cache_key,
                "cache_hit": question_cache_hit,
            }
        question_text = question["question"]
        question_row = {
            **question_row,
            "unsupported_experience_assumption": _unsupported_experience_assumption(
                question_text
            ),
            "deterministic_grounding_overlap": grounding_overlap(
                question_text, contexts
            ),
        }
        judge_prompt = _judge_prompt(case, question, contexts)
        judge_prompt_hash = _hash(judge_prompt)
        previous_judgment = existing_judgments.get(case["resume_id"])
        judgment_reused = bool(
            previous_judgment
            and previous_judgment.get("question_id") == question_id
            and previous_judgment.get("judge_prompt_hash") == judge_prompt_hash
            and previous_judgment.get("model") == judge_model
        )
        if judgment_reused:
            judgment_row = previous_judgment
            judgment = QualityJudgment.model_validate(judgment_row["judgment"]).model_dump(mode="json")
        else:
            judge_cache_key = _hash(
                {
                    "prompt_hash": judge_prompt_hash,
                    "model": judge_model,
                    "temperature": 0.0,
                    "rubric": RUBRIC_VERSION,
                }
            )
            cached_judgment = judgment_cache.get(judge_cache_key)
            judgment_cache_hit = cached_judgment is not None
            if cached_judgment is None:
                judge_result = await provider.generate_json(
                    judge_prompt,
                    QualityJudgment,
                    model=judge_model,
                    temperature=0.0,
                    system_instruction=JUDGE_SYSTEM_INSTRUCTION,
                    thinking_budget=128,
                    timeout_seconds=60.0,
                )
                cached_judgment = {
                    "parsed": judge_result.parsed,
                    "raw_provider_output": judge_result.raw_provider_output,
                    "usage": judge_result.usage,
                    "latency_ms": judge_result.latency_ms,
                }
                judgment_cache.put(judge_cache_key, cached_judgment)
            judgment = QualityJudgment.model_validate(cached_judgment["parsed"]).model_dump(mode="json")
            judgment_row = {
                "question_id": question_id,
                "resume_id": case["resume_id"],
                "category": case["category"],
                "domain": case["domain"],
                "level": case["level"],
                "language": case["language"],
                "rubric_version": RUBRIC_VERSION,
                "judgment": judgment,
                "judge_prompt_hash": judge_prompt_hash,
                "model": judge_model,
                "temperature": 0.0,
                "latency_ms": cached_judgment["latency_ms"],
                "usage": cached_judgment["usage"],
                "raw_provider_output": cached_judgment["raw_provider_output"],
                "cache_key": judge_cache_key,
                "cache_hit": judgment_cache_hit,
            }
        allowed_ids = {str(item.get("chunk_id")) for item in contexts if item.get("chunk_id")}
        judgment["grounding_chunk_ids"] = [
            cid for cid in judgment.get("grounding_chunk_ids", []) if str(cid) in allowed_ids
        ]
        question_row["retrieval_utilized"] = bool(
            judgment["rag_grounding"] >= 1
            and question_row["deterministic_grounding_overlap"] > 0
        )
        return question_row, judgment_row, int(question_reused and judgment_reused)

    completed = []
    total_cases = len(dataset)
    for idx, case in enumerate(dataset, 1):
        res = await one(case)
        completed.append(res)
        if idx % 5 == 0 or idx == total_cases:
            print(f"[Azure OpenAI Eval] Processed {idx}/{total_cases} cases...", flush=True)
    question_rows = [item[0] for item in completed]
    judgment_rows = [item[1] for item in completed]
    resumed_completed_cases = sum(item[2] for item in completed)
    question_texts = [row["question"]["question"] for row in question_rows]
    duplicate_metrics = duplicate_statistics(question_texts)
    question_lengths = [len(value) for value in question_texts]

    _write_jsonl(output_dir / "questions.jsonl", question_rows)
    _write_jsonl(output_dir / "judgments.jsonl", judgment_rows)
    metrics = {
        "schema_version": "cv-question-rag.questions.v1",
        **_aggregate(judgment_rows),
        "language_match_rate": statistics.fmean(
            int(row["question"]["language"] == row["language"])
            for row in question_rows
        ) if question_rows else None,
        "difficulty_label_match_rate": statistics.fmean(
            int(row["judgment"]["difficulty_label"] == row["level"])
            for row in judgment_rows
        ) if judgment_rows else None,
        "unsupported_experience_assumption_rate": statistics.fmean(
            int(row["unsupported_experience_assumption"]) for row in question_rows
        ) if question_rows else None,
        "target_topic_mention_rate": statistics.fmean(
            int(
                _normalized_text(row["target_topic"])
                in _normalized_text(row["question"]["question"])
            )
            for row in question_rows
        ) if question_rows else None,
        "mean_deterministic_grounding_overlap": statistics.fmean(
            row["deterministic_grounding_overlap"] for row in question_rows
        ) if question_rows else None,
        "retrieval_utilization_rate": statistics.fmean(
            int(row["retrieval_utilized"]) for row in question_rows
        ) if question_rows else None,
        "question_length_characters": {
            "mean": statistics.fmean(question_lengths) if question_lengths else None,
            "p95": sorted(question_lengths)[
                max(0, math.ceil(0.95 * len(question_lengths)) - 1)
            ] if question_lengths else None,
        },
        **duplicate_metrics,
        "by_category": _grouped(judgment_rows, "category"),
        "by_domain": _grouped(judgment_rows, "domain"),
        "by_language": _grouped(judgment_rows, "language"),
        "question_model": question_model,
        "question_temperature": 0.2,
        "judge_model": judge_model,
        "judge_temperature": 0.0,
        "condition": "CURRENT_PRODUCTION_LEXICAL",
        "label_source": "LLM_AS_JUDGE_ON_PUBLIC_RESUME_DERIVED_SKILLS",
        "human_review_status": "NOT_COMPLETED",
        "resumed_completed_cases": resumed_completed_cases,
        "privacy": "No filename, Resume text, or personal Candidate Profile field is sent to the question or judge prompts.",
        "claim_boundary": (
            "These are LLM-as-judge quality measurements over privacy-safe profiles derived from exact "
            "catalog terms in public Resumes; they are not human judgments or Resume extraction accuracy."
        ),
    }
    _write_json(output_dir / "QUESTION_METRICS.json", metrics)
    return metrics


def run_questions(
    *,
    repo_root: Path,
    dataset_path: Path,
    retrieval_path: Path,
    output_dir: Path,
    provider: Any,
    max_cases: int = 150,
    question_model: str = QUESTION_MODEL,
    judge_model: str = JUDGE_MODEL,
) -> dict[str, Any]:
    """Generate and judge current-production lexical questions from safe profiles."""
    if max_cases < 1:
        raise ValueError("max_cases must be positive")
    dataset = _balanced_limit(_read_jsonl(dataset_path), max_cases)
    retrieval_by_id = {
        row["resume_id"]: row for row in _read_jsonl(retrieval_path)
    }
    return asyncio.run(
        _run_questions(
            repo_root=repo_root,
            dataset=dataset,
            retrieval_by_id=retrieval_by_id,
            output_dir=output_dir,
            provider=provider,
            question_model=question_model,
            judge_model=judge_model,
        )
    )
