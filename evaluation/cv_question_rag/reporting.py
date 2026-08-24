from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from evaluation.cv_question_rag.question_audit import write_question_audit
from evaluation.cv_question_rag.cost import PRICES_PER_MILLION


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _usage(rows: list[dict[str, Any]], model: str) -> dict[str, Any]:
    input_tokens = sum(int(row.get("usage", {}).get("input_tokens") or 0) for row in rows)
    output_tokens = sum(int(row.get("usage", {}).get("output_tokens") or 0) for row in rows)
    complete = all(
        row.get("usage", {}).get("input_tokens") is not None
        and row.get("usage", {}).get("output_tokens") is not None
        for row in rows
    )
    prices = PRICES_PER_MILLION[model]
    cost = (
        input_tokens * prices["input"] + output_tokens * prices["output"]
    ) / 1_000_000
    return {
        "model": model,
        "calls": len(rows),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "usage_complete": complete,
        "estimated_cost_usd": cost if complete else None,
        "pricing_basis": "evaluation.cv_question_rag.cost.PRICES_PER_MILLION",
    }


def _balanced_review(rows: list[dict[str, Any]], limit: int, seed: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)
    for category, values in grouped.items():
        values.sort(
            key=lambda row: hashlib.sha256(
                f"{seed}:{category}:{row['question_id']}".encode()
            ).hexdigest()
        )
    selected: list[dict[str, Any]] = []
    while len(selected) < min(limit, len(rows)):
        progressed = False
        for category in sorted(grouped):
            if grouped[category] and len(selected) < limit:
                selected.append(grouped[category].pop())
                progressed = True
        if not progressed:
            break
    return selected


def _human_pack(
    *, docs_dir: Path, questions: list[dict[str, Any]], sample_size: int, seed: int
) -> int:
    selected = _balanced_review(questions, sample_size, seed)
    fields = [
        "review_id",
        "category",
        "domain",
        "level",
        "language",
        "target_topic",
        "question",
        "technical_validity",
        "role_relevance",
        "cv_alignment",
        "difficulty_alignment",
        "clarity",
        "rag_grounding",
        "false_premise",
        "reviewer_id",
        "notes",
    ]
    mapping: list[dict[str, str]] = []
    docs_dir.mkdir(parents=True, exist_ok=True)
    with (docs_dir / "HUMAN_REVIEW_TEMPLATE.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, row in enumerate(selected, start=1):
            review_id = "REVIEW-" + hashlib.sha256(
                f"{seed}:{row['question_id']}".encode()
            ).hexdigest()[:10].upper()
            writer.writerow(
                {
                    "review_id": review_id,
                    "category": row["category"],
                    "domain": row["domain"],
                    "level": row["level"],
                    "language": row["language"],
                    "target_topic": row["target_topic"],
                    "question": row["question"]["question"],
                    "technical_validity": "",
                    "role_relevance": "",
                    "cv_alignment": "",
                    "difficulty_alignment": "",
                    "clarity": "",
                    "rag_grounding": "",
                    "false_premise": "",
                    "reviewer_id": "",
                    "notes": "",
                }
            )
            mapping.append(
                {
                    "review_id": review_id,
                    "question_id": row["question_id"],
                    "display_order": str(index),
                }
            )
    _write_json(docs_dir / "HUMAN_REVIEW_MAPPING.json", mapping)
    return len(selected)


def build_reports(
    *,
    dataset_dir: Path,
    run_dir: Path,
    docs_dir: Path,
    review_sample_size: int = 60,
    seed: int = 20260820,
) -> dict[str, Any]:
    dataset = _read_json(dataset_dir / "DATASET_MANIFEST.json")
    retrieval = _read_json(run_dir / "RETRIEVAL_METRICS.json")
    question = _read_json(run_dir / "QUESTION_METRICS.json")
    questions = _read_jsonl(run_dir / "questions.jsonl")
    judgments = _read_jsonl(run_dir / "judgments.jsonl")
    pattern_audit = write_question_audit(rows=questions, output_dir=run_dir)
    review_count = _human_pack(
        docs_dir=docs_dir,
        questions=questions,
        sample_size=review_sample_size,
        seed=seed,
    )
    question_cost = _usage(questions, "gemini-2.5-flash")
    judge_cost = _usage(judgments, "gemini-2.5-pro")
    total_cost = (
        question_cost["estimated_cost_usd"] + judge_cost["estimated_cost_usd"]
        if question_cost["estimated_cost_usd"] is not None
        and judge_cost["estimated_cost_usd"] is not None
        else None
    )
    cost = {
        "question_generation": question_cost,
        "llm_judge": judge_cost,
        "total_estimated_cost_usd": total_cost,
        "cost_is_invoice": False,
    }
    _write_json(docs_dir / "COST_REPORT.json", cost)

    lines = [
        "# Public Resume-derived Question Generation and Retrieval Evaluation",
        "",
        "Status: **PARTIAL_PENDING_HUMAN_REVIEW**",
        "",
        "## Evaluation scope",
        "",
        f"- Resume subset scanned: {dataset['inventory']['pdf_files']} / {dataset['inventory']['source_pdf_files']} public PDFs from `CHON_LOC_CV`.",
        f"- Pseudonymized selected cases: {dataset['dataset']['selected']} ({dataset['dataset']['development']} development, {dataset['dataset']['holdout']} holdout).",
        f"- Retrieval cases: {retrieval['sample_count']} using the current production lexical retriever.",
        f"- Question cases: {question['sample_count']} holdout cases using Gemini Question Generator plus a separate LLM-as-judge pass.",
        f"- Human-review template: {review_count} stratified questions; scores remain blank and pending.",
        "",
        "No filename, raw Resume text, name, email, phone number, or other direct personal field is retained in the dataset, raw logs, prompts, or reports. IDs are deterministic truncated SHA-256 pseudonyms, so this is pseudonymization rather than irreversible anonymization.",
        "",
        "## Retrieval results",
        "",
        f"- HitRate@1/3/5/8: {retrieval['hit_rate_at_1']:.4f} / {retrieval['hit_rate_at_3']:.4f} / {retrieval['hit_rate_at_5']:.4f} / {retrieval['hit_rate_at_8']:.4f}",
        f"- Recall@5/8: {retrieval['recall_at_5']:.4f} / {retrieval['recall_at_8']:.4f}",
        f"- MRR@8: {retrieval['mrr_at_8']:.4f}",
        f"- Latency mean/P95: {retrieval['latency_ms']['mean']:.2f} / {retrieval['latency_ms']['p95']:.2f} ms",
        "",
        "The retrieval labels come from exact knowledge-catalog titles detected in each Resume. This is a source-derived coverage test, not a human-labelled relevance or semantic-search benchmark.",
        "",
        "## Question Generation results",
        "",
        f"- Technical validity: {question['technical_validity_rate']:.4f}",
        f"- Role relevance: {question.get('role_relevance_rate', 0):.4f}",
        f"- CV-derived skill alignment: {question['cv_alignment_rate']:.4f}",
        f"- Mean clarity: {question.get('mean_clarity', 0):.4f} / 5",
        f"- Mean specificity: {question.get('mean_specificity', 0):.4f} / 2",
        f"- Mean retrieval grounding: {question['mean_rag_grounding']:.4f} / 2",
        f"- Deterministic grounding overlap: {question.get('mean_deterministic_grounding_overlap', 0):.4f}",
        f"- Retrieval utilization rate: {question.get('retrieval_utilization_rate', 0):.4f}",
        f"- Target-topic mention rate: {question.get('target_topic_mention_rate', 0):.4f}",
        f"- Language match rate: {question.get('language_match_rate', 0):.4f}",
        f"- Difficulty-label exact match: {question.get('difficulty_label_match_rate', 0):.4f}",
        f"- Normalized exact duplicate rate: {question.get('normalized_exact_duplicate_rate', 0):.4f}",
        f"- Opening-phrase repetition rate: {question.get('opening_phrase_repetition_rate', 0):.4f}",
        f"- Unsupported experience-assumption rate: {question.get('unsupported_experience_assumption_rate', 0):.4f}",
        f"- False-premise rate: {question.get('false_premise_rate', 0):.4f}",
        f"- Pattern audit counts: {pattern_audit['exact_duplicate_excess_count']} exact-duplicate excess, {pattern_audit['opening_repetition_excess_count']} repeated-opening excess, {pattern_audit['unsupported_experience_assumption_count']} unsupported-experience flags.",
        "",
        "Quality scores are LLM-as-judge measurements; overlap, utilization, duplication, repetition, language, difficulty, and unsupported-assumption values are deterministic rule-based audits. Neither group must be presented as human agreement until at least two independent technical reviewers complete the frozen template and disagreements are adjudicated.",
        "",
        "## Claim boundary and limitations",
        "",
        "- Resume exact-title matching selects eligible cases and therefore favors lexical retrieval; high HitRate is expected and must not be generalized to paraphrases.",
        "- The redacted Candidate Profile retains detected catalog skills but removes real project/experience prose, so this evaluates skill alignment rather than deep personal-experience grounding.",
        "- The deterministic unsupported-experience check is conservative and pattern-based; flagged questions require human review rather than automatic rejection.",
        "- The source corpus is public per project-owner confirmation, but public availability is not a substitute for a documented consent, retention, and research-ethics protocol.",
        "- Domain/category slices with fewer than 30 cases are descriptive only.",
        "- Human review is pending; overall status remains partial.",
    ]
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "CV_QUESTION_RAG_REPORT.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    manifest = {
        "schema_version": "cv-question-rag.run.v1",
        "status": "PARTIAL_PENDING_HUMAN_REVIEW",
        "seed": seed,
        "dataset_hash": dataset["dataset"].get("dataset_hash"),
        "artifacts": {
            "dataset_manifest_sha256": _sha(dataset_dir / "DATASET_MANIFEST.json"),
            "retrieval_log_sha256": _sha(run_dir / "retrieval.jsonl"),
            "retrieval_metrics_sha256": _sha(run_dir / "RETRIEVAL_METRICS.json"),
            "questions_log_sha256": _sha(run_dir / "questions.jsonl"),
            "judgments_log_sha256": _sha(run_dir / "judgments.jsonl"),
            "question_metrics_sha256": _sha(run_dir / "QUESTION_METRICS.json"),
            "question_pattern_audit_sha256": _sha(
                run_dir / "QUESTION_PATTERN_AUDIT.json"
            ),
            "exact_duplicate_groups_sha256": _sha(
                run_dir / "exact_duplicate_groups.jsonl"
            ),
            "opening_repetition_groups_sha256": _sha(
                run_dir / "opening_repetition_groups.jsonl"
            ),
            "unsupported_experience_assumptions_sha256": _sha(
                run_dir / "unsupported_experience_assumptions.jsonl"
            ),
        },
        "provider_calls": {
            "question_generation": len(questions),
            "llm_judge": len(judgments),
        },
        "human_review": {"selected": review_count, "completed": 0},
        "commands": {
            "prepare": "python -m evaluation.cv_question_rag.run_benchmark --prepare --corpus-dir resumes --corpus-limit 500 --sample-size 300 --development-ratio 0.5 --seed 20260820",
            "retrieval": "python -m evaluation.cv_question_rag.run_benchmark --run-retrieval --seed 20260820",
            "questions": "python -m evaluation.cv_question_rag.run_benchmark --execute-paid-questions --max-question-cases 150",
        },
    }
    _write_json(docs_dir / "RUN_MANIFEST.json", manifest)
    return {"status": manifest["status"], "review_sample_count": review_count}
