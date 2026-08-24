from __future__ import annotations

import hashlib
import json
import math
import random
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


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


def _topic_id(domain: str, entry: dict[str, Any]) -> str:
    identity = "|".join(
        [domain, *entry.get("path", []), entry.get("title", "")]
    )
    return "topic_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]


class _RetrievalTraceAdapter:
    """Invoke production retrieval and resolve returned contexts to catalog IDs."""

    def __init__(
        self,
        *,
        retriever: Any,
        catalog_path: Path,
        domain_labels: dict[str, str],
    ) -> None:
        self.retriever = retriever
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        self.by_domain: dict[str, dict[str, str]] = {}
        for domain, entries in catalog["domains"].items():
            mapping: dict[str, str] = {}
            for entry in entries:
                path_text = " > ".join(
                    [*entry.get("path", []), entry.get("title", "")]
                )
                detail = f"Candidate-aligned topic: {path_text}"
                anchors = "; ".join(entry.get("anchors", [])[:5])
                if anchors:
                    detail += f" | anchors: {anchors}"
                mapping[detail] = _topic_id(domain, entry)
            self.by_domain[domain] = mapping
        self.domain_by_label = {value: key for key, value in domain_labels.items()}

    def retrieve(self, profile: Any, config: Any) -> dict[str, Any]:
        started = time.perf_counter()
        output = self.retriever.retrieve_topics(profile, config)
        latency_ms = (time.perf_counter() - started) * 1000
        selected_label = output[0].removeprefix("Domain: ") if output else ""
        selected_domain = self.domain_by_label.get(selected_label)
        mapping = self.by_domain.get(selected_domain or "", {})
        ranked = []
        for text in output:
            if text.startswith("Candidate-aligned topic: "):
                ranked.append(
                    {
                        "rank": len(ranked) + 1,
                        "topic_id": mapping.get(text),
                        "score": None,
                        "text": text,
                    }
                )
        return {
            "raw_contexts": output,
            "selected_domain": selected_domain,
            "retrieved": ranked,
            "latency_ms": latency_ms,
        }


def _percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(fraction * len(ordered)) - 1)]


def _case_metrics(row: dict[str, Any]) -> dict[str, float]:
    expected = set(row["expected_topic_ids"])
    retrieved = [item["topic_id"] for item in row["retrieved_topics"]]
    values: dict[str, float] = {}
    for cutoff in (1, 3, 5, 8):
        selected = retrieved[:cutoff]
        values[f"hit_rate_at_{cutoff}"] = float(bool(expected & set(selected)))
        values[f"recall_at_{cutoff}"] = (
            len(expected & set(selected)) / len(expected) if expected else 0.0
        )
    values["mrr_at_8"] = next(
        (1 / rank for rank, topic_id in enumerate(retrieved[:8], start=1) if topic_id in expected),
        0.0,
    )
    values["zero_result_rate"] = float(not retrieved)
    values["domain_selection_accuracy"] = float(row["selected_domain"] == row["expected_domain"])
    return values


def _aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"sample_count": 0}
    per_case = [_case_metrics(row) for row in rows]
    return {
        "sample_count": len(rows),
        **{
            key: statistics.fmean(value[key] for value in per_case)
            for key in per_case[0]
        },
    }


def _bootstrap(
    rows: list[dict[str, Any]], *, seed: int, samples: int = 1000
) -> dict[str, dict[str, float]]:
    if not rows:
        return {}
    randomizer = random.Random(seed)
    keys = ("hit_rate_at_5", "hit_rate_at_8", "mrr_at_8")
    observed = {key: [] for key in keys}
    for _ in range(samples):
        sample = [rows[randomizer.randrange(len(rows))] for _ in rows]
        metrics = _aggregate(sample)
        for key in keys:
            observed[key].append(float(metrics[key]))
    return {
        key: {
            "lower_95": sorted(values)[math.floor(0.025 * (samples - 1))],
            "upper_95": sorted(values)[math.ceil(0.975 * (samples - 1))],
        }
        for key, values in observed.items()
    }


def run_retrieval(
    *,
    repo_root: Path,
    dataset_path: Path,
    output_dir: Path,
    seed: int = 20260820,
) -> dict[str, Any]:
    """Run the current production lexical retriever over privacy-safe profiles."""
    backend = repo_root / "backend"
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))
    from services.interview_knowledge.local import DOMAIN_LABELS, LocalKnowledgeRetriever
    from shared.schemas import CandidateProfile, InterviewConfig

    catalog_path = backend / "services/interview_knowledge/catalog.json"
    trace = _RetrievalTraceAdapter(
        retriever=LocalKnowledgeRetriever(catalog_path=catalog_path, topic_limit=8),
        catalog_path=catalog_path,
        domain_labels=DOMAIN_LABELS,
    )
    dataset = _read_jsonl(dataset_path)
    rows: list[dict[str, Any]] = []
    for case in dataset:
        profile = CandidateProfile.model_validate(case["candidate_profile"])
        config = InterviewConfig(
            mode="text",
            language=case["language"],
            experience_level=case["level"].casefold(),
            duration_minutes=30,
            interview_style="technical",
            question_count=6,
            objective="Evaluate Resume-derived technical skills",
            interviewer_personality="professional",
        )
        result = trace.retrieve(profile, config)
        expected = [item["topic_id"] for item in case["matched_topics"]]
        retrieved_contexts = [
            {
                "rank": item["rank"],
                "chunk_id": item["topic_id"],
                "topic_id": item["topic_id"],
                "topic": item["text"],
                "content": item["text"],
            }
            for item in result["retrieved"]
            if item.get("topic_id")
        ]
        retrieved = [
            {"rank": item["rank"], "topic_id": item["topic_id"]}
            for item in retrieved_contexts
        ]
        retrieved_ids = [item["topic_id"] for item in retrieved]
        reciprocal_rank = next(
            (1 / rank for rank, topic_id in enumerate(retrieved_ids, start=1) if topic_id in set(expected)),
            0.0,
        )
        rows.append(
            {
                "resume_id": case["resume_id"],
                "category": case["category"],
                "expected_domain": case["domain"],
                "selected_domain": result["selected_domain"],
                "level": case["level"],
                "language": case["language"],
                "label_source": case["label_source"],
                "system": "production_lexical",
                "top_k": 8,
                "expected_topic_ids": expected,
                "retrieved_topics": retrieved,
                "retrieved_contexts": retrieved_contexts,
                "hit_at_1": bool(set(expected) & set(retrieved_ids[:1])),
                "hit_at_3": bool(set(expected) & set(retrieved_ids[:3])),
                "hit_at_5": bool(set(expected) & set(retrieved_ids[:5])),
                "hit_at_8": bool(set(expected) & set(retrieved_ids[:8])),
                "reciprocal_rank_at_8": reciprocal_rank,
                "latency_ms": float(result["latency_ms"]),
            }
        )

    aggregate = _aggregate(rows)
    latencies = [row["latency_ms"] for row in rows]
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_domain[row["expected_domain"]].append(row)
        by_category[row["category"]].append(row)
    metrics = {
        "schema_version": "cv-question-rag.retrieval.v1",
        **aggregate,
        "latency_ms": {
            "mean": statistics.fmean(latencies) if latencies else None,
            "median": statistics.median(latencies) if latencies else None,
            "p95": _percentile(latencies, 0.95),
        },
        "confidence_intervals": _bootstrap(rows, seed=seed),
        "by_domain": {key: _aggregate(value) for key, value in sorted(by_domain.items())},
        "by_category": {key: _aggregate(value) for key, value in sorted(by_category.items())},
        "label_source": "resume_exact_catalog_title",
        "human_relevance_labels": False,
        "claim_boundary": (
            "Measures current lexical retrieval against Resume-derived exact catalog-title labels; "
            "it is not a human-labelled relevance benchmark."
        ),
    }
    _write_jsonl(output_dir / "retrieval.jsonl", rows)
    _write_json(output_dir / "RETRIEVAL_METRICS.json", metrics)
    return metrics
