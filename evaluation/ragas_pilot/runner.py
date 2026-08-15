from __future__ import annotations

import importlib.metadata
import importlib.util
import json
import platform
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluation.ragas_pilot.answers import QUALITY_ORDER, build_controlled_answers
from evaluation.ragas_pilot.dataset import (
    ControlledCaseSpec,
    build_controlled_case_specs,
)
from evaluation.ragas_pilot.evidence_io import append_jsonl, write_jsonl
from evaluation.ragas_pilot.judges import PilotJudge, RUBRIC_VERSION
from evaluation.ragas_pilot.metrics import (
    context_precision_without_reference,
    is_strictly_monotonic,
)
from evaluation.ragas_pilot.retrieval import (
    BACKEND_ROOT,
    REPO_ROOT,
    build_interview_config,
    build_synthetic_profile,
    evaluate_retrieval_spec,
)
from evaluation.ragas_pilot.runtime_config import resolve_evaluation_settings
from evaluation.ragas_pilot.summaries import (
    summarize_answer_samples,
    summarize_question_samples,
    summarize_rag_samples,
)
from evaluation.ragas_pilot.tracking import (
    PRICING_ACCESSED_AT,
    PRICING_SOURCE,
    TrackingLLM,
    estimate_visible_token_cost_usd,
)


if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from core.settings import get_settings  # noqa: E402
from infrastructure.llm.vertex_gemini import (  # noqa: E402
    RetryConfig,
    VertexGeminiService,
)
from services.answer_evaluator.agent import EvaluatorAgent  # noqa: E402
from services.interview_knowledge.local import LocalKnowledgeRetriever  # noqa: E402
from services.interview_planner.agent import InterviewPlannerAgent  # noqa: E402
from services.question_generator.agent import QuestionGeneratorAgent  # noqa: E402
from shared.schemas import CandidateProfile, InterviewConfig, InterviewQuestion  # noqa: E402


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def _ragas_version() -> str | None:
    if importlib.util.find_spec("ragas") is None:
        return None
    return importlib.metadata.version("ragas")


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _profile_summary(profile: CandidateProfile) -> str:
    return (
        f"Synthetic profile; role={profile.recent_role}; "
        f"skills={', '.join(profile.skills)}; projects={len(profile.projects)}"
    )


def _validate_rag_judgment(sample: dict[str, Any], judgment: Any) -> None:
    expected_ranks = [value["rank"] for value in sample["retrieved_contexts"]]
    actual_ranks = [value.rank for value in judgment.context_judgments]
    if sorted(actual_ranks) != sorted(expected_ranks) or len(actual_ranks) != len(
        set(actual_ranks)
    ):
        raise ValueError("Retrieval judge must return every context rank exactly once")


def _validate_answer_judgment(judgment: Any) -> None:
    tiers = [value.quality_tier for value in judgment.judgments]
    if sorted(tiers) != sorted(QUALITY_ORDER) or len(tiers) != len(set(tiers)):
        raise ValueError("Answer judge must return every quality tier exactly once")


class PilotRunner:
    def __init__(
        self,
        *,
        output_root: Path,
        catalog_path: Path,
        smoke_size: int = 10,
        target_size: int = 30,
        robustness_subset: int = 2,
    ) -> None:
        if smoke_size < 1 or smoke_size > target_size:
            raise ValueError("smoke_size must be between 1 and target_size")
        self.output_root = output_root
        self.catalog_path = catalog_path
        self.smoke_size = smoke_size
        self.target_size = target_size
        self.robustness_subset = min(robustness_subset, smoke_size)
        self.settings = resolve_evaluation_settings(get_settings())
        delegate = VertexGeminiService(
            settings=self.settings,
            retry_config=RetryConfig(
                max_attempts=3,
                initial_backoff_seconds=0.5,
                max_backoff_seconds=4.0,
                jitter_seconds=0.1,
            ),
        )
        self.llm = TrackingLLM(delegate)
        retriever = LocalKnowledgeRetriever(catalog_path=catalog_path, topic_limit=8)
        self.planner = InterviewPlannerAgent(self.llm, knowledge_retriever=retriever)
        self.question_generator = QuestionGeneratorAgent(self.llm)
        self.answer_evaluator = EvaluatorAgent(
            self.llm, task_type=self.settings.evaluator_task_type
        )
        self.judge = PilotJudge(self.llm, model=self.settings.gemini_simple_model)
        self.specs = build_controlled_case_specs(
            catalog_path, limit=self.target_size
        )[: self.smoke_size]

    def _paths(self) -> dict[str, Path]:
        return {
            "rag": self.output_root / "rag" / "samples.jsonl",
            "question": self.output_root
            / "question_generation"
            / "samples.jsonl",
            "answer": self.output_root / "answer_evaluation" / "samples.jsonl",
            "calls": self.output_root / "model_calls.jsonl",
        }

    def _initialize_outputs(self) -> None:
        for path in self._paths().values():
            write_jsonl(path, [])

    async def _run_rag(self) -> list[dict[str, Any]]:
        path = self._paths()["rag"]
        rows: list[dict[str, Any]] = []
        for index, spec in enumerate(self.specs):
            sample = evaluate_retrieval_spec(spec, self.catalog_path)
            sample.update(
                {
                    "timestamp": _utc_now(),
                    "evidence_classification": ["A", "B", "C"],
                    "judge_model": self.judge.model,
                    "judge_temperature": 0.0,
                    "rubric_version": RUBRIC_VERSION,
                }
            )
            try:
                vote_count = 3 if index < self.robustness_subset else 1
                votes = [
                    await self.judge.judge_retrieval(sample)
                    for _ in range(vote_count)
                ]
                for vote in votes:
                    _validate_rag_judgment(sample, vote)
                primary = votes[0]
                ordered = sorted(primary.context_judgments, key=lambda value: value.rank)
                labels = [value.label for value in ordered]
                scores = [value.relevance_score for value in ordered]
                count = len(ordered)
                sample.update(
                    {
                        "status": "completed",
                        "metrics": {
                            "metric_name": (
                                "RAGAS-inspired context precision without reference"
                            ),
                            "official_ragas_metric": False,
                            "context_precision_without_reference": (
                                context_precision_without_reference(labels)
                            ),
                            "mean_context_relevance": sum(scores) / count
                            if count
                            else None,
                            "relevant_at_k_count": labels.count("relevant"),
                            "relevant_at_k_rate": labels.count("relevant") / count
                            if count
                            else None,
                            "irrelevant_at_k_count": labels.count("irrelevant"),
                            "irrelevant_at_k_rate": labels.count("irrelevant") / count
                            if count
                            else None,
                        },
                        "judge_votes": [value.model_dump(mode="json") for value in votes],
                        "primary_judgment": primary.model_dump(mode="json"),
                    }
                )
            except Exception as exc:
                sample.update(
                    {
                        "status": "failed",
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "metrics": None,
                        "judge_votes": [],
                    }
                )
            rows.append(sample)
            append_jsonl(path, sample)
            print(
                f"RAG {index + 1}/{len(self.specs)} {sample['status']}", flush=True
            )
        return rows

    async def _run_questions(
        self, rag_rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        path = self._paths()["question"]
        rag_by_id = {row["sample_id"].removeprefix("rag-"): row for row in rag_rows}
        rows: list[dict[str, Any]] = []
        for index, spec in enumerate(self.specs):
            profile = build_synthetic_profile(spec)
            config = build_interview_config(spec)
            rag_sample = rag_by_id[spec.sample_id.removeprefix("pilot-")]
            record: dict[str, Any] = {
                "sample_id": "question-" + spec.sample_id.removeprefix("pilot-"),
                "source_type": "synthetic_controlled",
                "timestamp": _utc_now(),
                "candidate_profile_summary": _profile_summary(profile),
                "candidate_profile": profile.model_dump(mode="json"),
                "role": spec.candidate_role,
                "level": spec.candidate_level,
                "language": spec.language,
                "interview_config": config.model_dump(mode="json"),
                "retrieved_contexts": rag_sample["retrieved_contexts"],
                "retrieval_to_question_path": (
                    "retrieved contexts -> InterviewPlannerAgent -> selected "
                    "InterviewRound -> QuestionGeneratorAgent"
                ),
                "planner_model": self.settings.gemini_simple_model,
                "question_model": self.settings.gemini_simple_model,
                "judge_model": self.judge.model,
                "judge_temperature": 0.0,
                "rubric_version": RUBRIC_VERSION,
                "evidence_classification": ["B", "C"],
            }
            try:
                planner_started = time.perf_counter()
                plan = await self.planner.create_plan(profile, config)
                planner_latency_ms = (time.perf_counter() - planner_started) * 1000
                if not plan.rounds:
                    raise ValueError("Planner returned no interview rounds")
                selected_round = plan.rounds[0]
                generation_started = time.perf_counter()
                question = await self.question_generator.generate_question(
                    profile, selected_round, config
                )
                generation_latency_ms = (
                    time.perf_counter() - generation_started
                ) * 1000
                judge_evidence = {
                    "candidate_profile_summary": record["candidate_profile_summary"],
                    "candidate_profile": record["candidate_profile"],
                    "role": spec.candidate_role,
                    "level": spec.candidate_level,
                    "retrieved_contexts": [
                        {
                            "rank": value["rank"],
                            "topic_id": value["topic_id"],
                            "text": value["text"],
                        }
                        for value in rag_sample["retrieved_contexts"]
                    ],
                    "interview_plan": plan.model_dump(mode="json"),
                    "selected_round": selected_round.model_dump(mode="json"),
                    "generated_question": question.model_dump(mode="json"),
                }
                vote_count = 3 if index < self.robustness_subset else 1
                votes = [
                    await self.judge.judge_question(judge_evidence)
                    for _ in range(vote_count)
                ]
                valid_context_ranks = {
                    value["rank"] for value in rag_sample["retrieved_contexts"]
                }
                for vote in votes:
                    if not set(vote.grounding_context_ranks) <= valid_context_ranks:
                        raise ValueError(
                            "Question judge cited a context rank that was not retrieved"
                        )
                primary = votes[0]
                record.update(
                    {
                        "status": "completed",
                        "interview_plan": plan.model_dump(mode="json"),
                        "selected_round": selected_round.model_dump(mode="json"),
                        "generated_question": question.model_dump(mode="json"),
                        "raw_generator_output_at_public_seam": question.model_dump(
                            mode="json"
                        ),
                        "provider_raw_text_available": False,
                        "planner_latency_ms": planner_latency_ms,
                        "generation_latency_ms": generation_latency_ms,
                        "metrics": {
                            "role_relevance": primary.role_relevance,
                            "cv_alignment": primary.cv_alignment,
                            "rag_grounding": primary.rag_grounding,
                            "difficulty_alignment": primary.difficulty_alignment,
                            "technical_validity": primary.technical_validity,
                            "clarity": primary.clarity,
                            "hallucinated_candidate_claim": (
                                primary.hallucinated_candidate_claim
                            ),
                        },
                        "judge_reasons": primary.judge_reasons,
                        "grounding_context_ranks": primary.grounding_context_ranks,
                        "judge_votes": [value.model_dump(mode="json") for value in votes],
                    }
                )
            except Exception as exc:
                record.update(
                    {
                        "status": "failed",
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "metrics": None,
                        "judge_votes": [],
                    }
                )
            rows.append(record)
            append_jsonl(path, record)
            print(
                f"QUESTION {index + 1}/{len(self.specs)} {record['status']}",
                flush=True,
            )
        return rows

    async def _run_answers(
        self, question_rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        path = self._paths()["answer"]
        rows: list[dict[str, Any]] = []
        successful_questions = [
            row for row in question_rows if row.get("status") == "completed"
        ]
        for group_index, question_record in enumerate(successful_questions):
            profile = CandidateProfile.model_validate(question_record["candidate_profile"])
            config = InterviewConfig.model_validate(question_record["interview_config"])
            question = InterviewQuestion.model_validate(
                question_record["generated_question"]
            )
            controlled_answers = build_controlled_answers(
                expected_points=question.expected_answer_points,
                language=config.language,
            )
            group_id = f"answer-group-{group_index + 1:03d}"
            group_records: list[dict[str, Any]] = []
            for answer_spec in controlled_answers:
                tier = answer_spec["quality_tier"]
                answer_record: dict[str, Any] = {
                    "sample_id": f"{group_id}-{tier}",
                    "group_id": group_id,
                    "source_question_id": question_record["sample_id"],
                    "source_type": "synthetic_controlled",
                    "timestamp": _utc_now(),
                    "quality_tier": tier,
                    "expected_quality_order": QUALITY_ORDER,
                    "controlled_intent": answer_spec["controlled_intent"],
                    "candidate_profile_summary": question_record[
                        "candidate_profile_summary"
                    ],
                    "candidate_profile": question_record["candidate_profile"],
                    "interview_config": question_record["interview_config"],
                    "question": question.model_dump(mode="json"),
                    "expected_points": question.expected_answer_points,
                    "answer": answer_spec["answer"],
                    "evaluator_model": self.settings.gemini_complex_model,
                    "evaluator_temperature": 0.1,
                    "judge_model": self.judge.model,
                    "judge_temperature": 0.0,
                    "rubric_version": RUBRIC_VERSION,
                    "evidence_classification": ["A", "B", "C"],
                    "human_score": None,
                }
                try:
                    started = time.perf_counter()
                    evaluation = await self.answer_evaluator.evaluate_answer(
                        profile, question, answer_spec["answer"], config
                    )
                    latency_ms = (time.perf_counter() - started) * 1000
                    answer_record.update(
                        {
                            "status": "completed",
                            "evaluation": evaluation.model_dump(mode="json"),
                            "raw_evaluator_output_at_public_seam": evaluation.model_dump(
                                mode="json"
                            ),
                            "provider_raw_text_available": False,
                            "evaluation_latency_ms": latency_ms,
                        }
                    )
                except Exception as exc:
                    answer_record.update(
                        {
                            "status": "failed",
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        }
                    )
                group_records.append(answer_record)

            completed_group = [
                row for row in group_records if row.get("status") == "completed"
            ]
            if len(completed_group) == len(QUALITY_ORDER):
                try:
                    good_record = next(
                        row for row in group_records if row["quality_tier"] == "good"
                    )
                    repeat_outputs = [good_record["evaluation"]]
                    repeat_latencies = [good_record["evaluation_latency_ms"]]
                    for _ in range(2):
                        started = time.perf_counter()
                        repeated = await self.answer_evaluator.evaluate_answer(
                            profile, question, good_record["answer"], config
                        )
                        repeat_latencies.append(
                            (time.perf_counter() - started) * 1000
                        )
                        repeat_outputs.append(repeated.model_dump(mode="json"))
                    repeat_scores = [
                        value["overall_score"] for value in repeat_outputs
                    ]
                    good_record["repeatability"] = {
                        "run_count": 3,
                        "scores": repeat_scores,
                        "score_range": max(repeat_scores) - min(repeat_scores),
                        "latencies_ms": repeat_latencies,
                        "outputs": repeat_outputs,
                    }

                    judge_evidence = {
                        "question": question.model_dump(mode="json"),
                        "expected_points": question.expected_answer_points,
                        "answer_evaluations": [
                            {
                                "quality_tier": row["quality_tier"],
                                "answer": row["answer"],
                                "evaluator_output": row["evaluation"],
                            }
                            for row in group_records
                        ],
                    }
                    vote_count = 3 if group_index < self.robustness_subset else 1
                    votes = [
                        await self.judge.judge_answer_group(judge_evidence)
                        for _ in range(vote_count)
                    ]
                    for vote in votes:
                        _validate_answer_judgment(vote)
                    primary_by_tier = {
                        value.quality_tier: value for value in votes[0].judgments
                    }
                    ordered_scores = [
                        next(
                            row["evaluation"]["overall_score"]
                            for row in group_records
                            if row["quality_tier"] == tier
                        )
                        for tier in QUALITY_ORDER
                    ]
                    group_metrics = {
                        "ordered_scores": dict(
                            zip(QUALITY_ORDER, ordered_scores, strict=True)
                        ),
                        "strict_monotonic": is_strictly_monotonic(ordered_scores),
                    }
                    serialized_votes = [
                        value.model_dump(mode="json") for value in votes
                    ]
                    for row in group_records:
                        judgment = primary_by_tier[row["quality_tier"]]
                        row.update(
                            {
                                "group_metrics": group_metrics,
                                "judge_metrics": {
                                    "rubric_adherence": judgment.rubric_adherence,
                                    "evidence_grounding": judgment.evidence_grounding,
                                    "unsupported_feedback": (
                                        judgment.unsupported_feedback
                                    ),
                                    "feedback_actionability": (
                                        judgment.feedback_actionability
                                    ),
                                    "score_feedback_consistency": (
                                        judgment.score_feedback_consistency
                                    ),
                                },
                                "judge_reasons": judgment.reasons,
                                "judge_votes": serialized_votes,
                            }
                        )
                except Exception as exc:
                    for row in group_records:
                        row.update(
                            {
                                "group_metrics": None,
                                "judge_metrics": None,
                                "judge_votes": [],
                                "group_error_type": type(exc).__name__,
                                "group_error": str(exc),
                            }
                        )
            else:
                for row in group_records:
                    row.setdefault("group_metrics", None)
                    row.setdefault("judge_metrics", None)
                    row.setdefault("judge_votes", [])

            for row in group_records:
                rows.append(row)
                append_jsonl(path, row)
            print(
                f"ANSWER GROUP {group_index + 1}/{len(successful_questions)} "
                f"completed_samples={len(completed_group)}",
                flush=True,
            )
        return rows

    async def run(self) -> dict[str, Any]:
        self._initialize_outputs()
        run_started = time.perf_counter()
        started_at = _utc_now()
        initial_manifest = self._manifest(
            status="running", started_at=started_at, duration_seconds=None
        )
        _write_json(self.output_root / "run_manifest.json", initial_manifest)

        rag_rows = await self._run_rag()
        question_rows = await self._run_questions(rag_rows)
        answer_rows = await self._run_answers(question_rows)
        duration_seconds = time.perf_counter() - run_started

        for call in self.llm.calls:
            append_jsonl(self._paths()["calls"], call)

        rag_summary = summarize_rag_samples(rag_rows)
        question_summary = summarize_question_samples(question_rows)
        answer_summary = summarize_answer_samples(answer_rows)
        _write_json(self.output_root / "rag" / "summary.json", rag_summary)
        _write_json(
            self.output_root / "question_generation" / "summary.json",
            question_summary,
        )
        _write_json(
            self.output_root / "answer_evaluation" / "summary.json",
            answer_summary,
        )
        manifest = self._manifest(
            status="smoke_completed",
            started_at=started_at,
            duration_seconds=duration_seconds,
        )
        _write_json(self.output_root / "run_manifest.json", manifest)
        self._write_markdown_summaries(
            manifest, rag_summary, question_summary, answer_summary
        )
        return {
            "manifest": manifest,
            "rag": rag_summary,
            "question_generation": question_summary,
            "answer_evaluation": answer_summary,
        }

    def _manifest(
        self,
        *,
        status: str,
        started_at: str,
        duration_seconds: float | None,
    ) -> dict[str, Any]:
        call_counts = Counter(call["operation"] for call in self.llm.calls)
        model_counts = Counter(call["model"] for call in self.llm.calls)
        judge_calls = sum("judge" in call["operation"] for call in self.llm.calls)
        generation_calls = len(self.llm.calls) - judge_calls
        estimated_cost = estimate_visible_token_cost_usd(self.llm.calls)
        scale = self.target_size / self.smoke_size
        return {
            "schema_version": "1.0",
            "project": "FiPilot",
            "pilot": "RAGAS-style pilot evaluation",
            "status": status,
            "evaluation_set": "synthetic controlled evaluation set",
            "started_at": started_at,
            "updated_at": _utc_now(),
            "duration_seconds": duration_seconds,
            "git_commit": _git_commit(),
            "python_version": platform.python_version(),
            "ragas_installed": _ragas_version() is not None,
            "ragas_version": _ragas_version(),
            "official_ragas_metrics_used": [],
            "custom_ragas_style_metrics": [
                "RAGAS-inspired context precision without reference",
                "context relevance classification",
                "FiPilot question quality rubric",
                "FiPilot Answer Evaluator behavior rubric",
            ],
            "pilot_size": {
                "target_per_primary_group": self.target_size,
                "smoke_case_groups": self.smoke_size,
                "executed_rag_queries": self.smoke_size,
                "executed_question_generations": self.smoke_size,
                "planned_answer_quality_groups": self.smoke_size,
                "planned_answer_samples": self.smoke_size * 4,
                "repeatability_subset": self.smoke_size,
                "judge_robustness_subset": self.robustness_subset,
                "scaled_to_30": False,
                "scale_decision": "requires review of smoke cost/runtime/results",
            },
            "provider": "Google Vertex AI Gemini",
            "vertex_location": self.settings.google_cloud_location,
            "models": {
                "planner": self.settings.gemini_simple_model,
                "question_generator": self.settings.gemini_simple_model,
                "answer_evaluator_text": self.settings.gemini_complex_model,
                "pilot_judge": self.settings.gemini_simple_model,
            },
            "temperatures": {
                "planner": 0.1,
                "question_generator": 0.2,
                "answer_evaluator": 0.1,
                "pilot_judge": 0.0,
            },
            "retry": {
                "max_attempts": 3,
                "initial_backoff_seconds": 0.5,
                "max_backoff_seconds": 4.0,
                "jitter_seconds": 0.1,
                "timeout_seconds": 60.0,
            },
            "rubric_version": RUBRIC_VERSION,
            "logical_api_calls": {
                "total": len(self.llm.calls),
                "judge": judge_calls,
                "generation_and_evaluation": generation_calls,
                "by_operation": dict(sorted(call_counts.items())),
                "by_model": dict(sorted(model_counts.items())),
            },
            "estimated_visible_tokens": {
                "input": sum(
                    call.get("estimated_input_tokens", 0) for call in self.llm.calls
                ),
                "output": sum(
                    call.get("estimated_output_tokens", 0) for call in self.llm.calls
                ),
            },
            "estimated_visible_token_cost_usd": estimated_cost,
            "projected_30_case_logical_calls": round(len(self.llm.calls) * scale),
            "projected_30_case_visible_token_cost_usd": estimated_cost * scale,
            "cost_estimate_warning": (
                "Character/4 visible-token estimate only. Provider thinking tokens, "
                "billing tiers, retries, caching, taxes, and account discounts are not "
                "observable here; use Cloud Billing for actual cost."
            ),
            "pricing_source": PRICING_SOURCE,
            "pricing_accessed_at": PRICING_ACCESSED_AT,
            "privacy": {
                "real_user_data_used": False,
                "real_resume_text_saved": False,
                "secrets_or_tokens_saved": False,
                "fake_human_labels_created": False,
                "historical_aggregate_reused": False,
            },
            "production_behavior_changed": False,
            "production_model_changed": False,
        }

    def _write_markdown_summaries(
        self,
        manifest: dict[str, Any],
        rag: dict[str, Any],
        question: dict[str, Any],
        answer: dict[str, Any],
    ) -> None:
        rag_md = f"""# RAG Retrieval Pilot Summary

Evaluation set: **synthetic controlled evaluation set**

- Samples: {rag['sample_count']}
- Successful: {rag['successful_count']}
- RAGAS-inspired context precision without reference: {rag['ragas_inspired_context_precision_without_reference']}
- Mean context relevance: {rag['mean_context_relevance']}
- Empty retrieval rate: {rag['empty_retrieval_rate']}
- Controlled HitRate@8: {rag['controlled_retrieval']['hit_rate_at_8']}
- Controlled Recall@8: {rag['controlled_retrieval']['recall_at_8']}
- Controlled MRR@8: {rag['controlled_retrieval']['mrr_at_8']}
- Context Recall: **NOT EVALUATED**

Reason: {rag['context_recall_reason']}
"""
        question_md = f"""# Question Generation Pilot Summary

Evaluation set: **synthetic controlled evaluation set**

- Samples: {question['sample_count']}
- Role relevance pass rate: {question['role_relevance_pass_rate']}
- CV alignment pass rate: {question['cv_alignment_pass_rate']}
- Technical validity pass rate: {question['technical_validity_pass_rate']}
- Mean RAG grounding: {question['mean_rag_grounding']} / 2
- Mean difficulty alignment: {question['mean_difficulty_alignment']} / 5
- Mean clarity: {question['mean_clarity']} / 5
- Hallucinated candidate claim rate: {question['hallucinated_candidate_claim_rate']}
"""
        answer_md = f"""# Answer Evaluator Pilot Summary

Evaluation set: **synthetic controlled evaluation set**

- Answer samples: {answer['sample_count']}
- Quality-order groups: {answer['group_count']}
- Controlled monotonicity: {answer['controlled_monotonicity_rate']}
- Mean rubric adherence: {answer['mean_rubric_adherence']} / 5
- Evidence grounding pass rate: {answer['evidence_grounding_pass_rate']}
- Unsupported feedback rate: {answer['unsupported_feedback_rate']}
- Mean feedback actionability: {answer['mean_feedback_actionability']} / 5
- Mean score-feedback consistency: {answer['mean_score_feedback_consistency']} / 5
- Repeatability range <= 1: {answer['repeatability']['range_le_one_rate']}
- Mean repeatability score standard deviation: {answer['repeatability']['mean_score_stddev']}
- Human MAE: **NOT EVALUATED**
- Human correlation: **NOT EVALUATED**

Reason: {answer['human_metrics_reason']}
"""
        (self.output_root / "rag" / "summary.md").write_text(rag_md, encoding="utf-8")
        (self.output_root / "question_generation" / "summary.md").write_text(
            question_md, encoding="utf-8"
        )
        (self.output_root / "answer_evaluation" / "summary.md").write_text(
            answer_md, encoding="utf-8"
        )
        overall = f"""# FiPilot RAGAS-Style Pilot Evaluation

## Run Metadata

- Git commit: `{manifest['git_commit']}`
- Evaluator/judge: `{manifest['models']['pilot_judge']}` on Vertex AI, temperature 0
- Ragas version: not installed
- Pilot size: {self.smoke_size} smoke case groups; target 30 pending review
- Date: {manifest['started_at']}
- Logical model calls: {manifest['logical_api_calls']['total']}
- Approximate runtime: {manifest['duration_seconds']} seconds
- Estimated visible-token cost: ${manifest['estimated_visible_token_cost_usd']:.6f} USD

## RAG Retrieval

- Samples: {rag['sample_count']}
- RAGAS-inspired reference-free context precision: {rag['ragas_inspired_context_precision_without_reference']}
- Mean context relevance: {rag['mean_context_relevance']}
- Empty retrieval rate: {rag['empty_retrieval_rate']}
- Median latency: {(rag['retrieval_latency'] or {}).get('median_ms')} ms
- P95 latency: {(rag['retrieval_latency'] or {}).get('p95_ms')} ms
- Controlled HitRate@8: {rag['controlled_retrieval']['hit_rate_at_8']}
- Controlled MRR@8: {rag['controlled_retrieval']['mrr_at_8']}
- Reference-based Context Recall: **NOT EVALUATED**

Reason: {rag['context_recall_reason']}

## Question Generation

- Samples: {question['sample_count']}
- Role relevance: {question['role_relevance_pass_rate']}
- CV alignment: {question['cv_alignment_pass_rate']}
- Technical validity: {question['technical_validity_pass_rate']}
- RAG grounding: {question['mean_rag_grounding']} / 2
- Difficulty alignment: {question['mean_difficulty_alignment']} / 5
- Clarity: {question['mean_clarity']} / 5
- Unsupported candidate claim rate: {question['hallucinated_candidate_claim_rate']}

## Answer Evaluation

- Samples: {answer['sample_count']} across {answer['group_count']} controlled groups
- Controlled monotonicity: {answer['controlled_monotonicity_rate']}
- Rubric adherence: {answer['mean_rubric_adherence']} / 5
- Evidence grounding: {answer['evidence_grounding_pass_rate']}
- Unsupported feedback rate: {answer['unsupported_feedback_rate']}
- Feedback actionability: {answer['mean_feedback_actionability']} / 5
- Score-feedback consistency: {answer['mean_score_feedback_consistency']} / 5
- Repeatability range <= 1: {answer['repeatability']['range_le_one_rate']}
- Mean score standard deviation: {answer['repeatability']['mean_score_stddev']}
- Human MAE: **NOT EVALUATED**
- Human correlation: **NOT EVALUATED**

Reason: {answer['human_metrics_reason']}

## Defense Classification

- A: deterministic retrieval latency, empty rate, controlled HitRate/Recall/MRR, monotonicity, repeatability arithmetic
- B: LLM-as-judge relevance and rubric scores
- C: all Candidate Profiles and answer quality tiers are synthetic controlled
- D: none; no human-labelled benchmark was used

## Scale Decision

The run intentionally stopped after the 10-case smoke pilot. Scaling to 30
requires review of the measured logical call count, runtime, failures, and
estimated cost in `run_manifest.json`.
"""
        (self.output_root / "overall_summary.md").write_text(
            overall, encoding="utf-8"
        )
