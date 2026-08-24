from __future__ import annotations

import json
from pathlib import Path

from evaluation.cv_question_rag.provider import ProviderResult
from evaluation.cv_question_rag.questions import run_questions


REPO_ROOT = Path(__file__).resolve().parents[3]


class FakeProvider:
    async def generate_json(
        self,
        prompt,
        schema,
        *,
        model,
        temperature,
        system_instruction,
        thinking_budget=0,
        timeout_seconds=60.0,
    ) -> ProviderResult:
        if schema.__name__ == "GeneratedQuestion":
            parsed = {
                "question": "Trong dự án của bạn, bạn đã dùng FastAPI để xử lý dependency failure như thế nào?",
                "language": "vi",
                "topic": "FastAPI",
                "difficulty": "medium",
                "reasoning": "Targets the Resume-derived skill.",
                "expected_answer_points": ["Dependency injection", "Failure handling"],
                "follow_up_questions": [],
            }
        else:
            parsed = {
                "technical_validity": 1,
                "role_relevance": 1,
                "cv_alignment": 1,
                "difficulty_label": "Middle",
                "difficulty_score": 5,
                "clarity": 5,
                "specificity": 2,
                "rag_grounding": 2,
                "answerability": 1,
                "non_redundancy": 1,
                "knowledge_false_premise": 0,
                "grounding_chunk_ids": ["topic-fastapi"],
                "reasons": {"summary": "Valid and grounded."},
            }
        return ProviderResult(
            parsed=parsed,
            raw_provider_output=json.dumps(parsed, ensure_ascii=False),
            usage={"input_tokens": 100, "output_tokens": 50, "total_tokens": 150},
            latency_ms=12.5,
            model=model,
        )


class ProviderMustNotBeCalled:
    async def generate_json(self, *args, **kwargs):
        raise AssertionError("completed question run should resume without provider calls")


def test_run_questions_writes_traceable_privacy_safe_logs(tmp_path: Path) -> None:
    dataset_path = tmp_path / "holdout.jsonl"
    dataset_path.write_text(
        json.dumps(
            {
                "resume_id": "CV-ABCDEF123456",
                "category": "software-development",
                "domain": "Backend_Developer",
                "level": "Middle",
                "language": "vi",
                "target_topic_id": "topic-fastapi",
                "target_topic": "FastAPI",
                "matched_topics": [{"topic_id": "topic-fastapi", "title": "FastAPI"}],
                "candidate_profile": {
                    "name": "Candidate CV-ABCDEF123456",
                    "years_experience": None,
                    "recent_role": "Backend Developer",
                    "specialization": "Backend Developer",
                    "skills": ["FastAPI"],
                    "skill_evidence": [
                        {"skill": "FastAPI", "evidence": ["Exact catalog term detected in Resume"]}
                    ],
                    "projects": [
                        {
                            "name": "Redacted Resume evidence",
                            "description": "Public Resume contains the selected catalog skills.",
                            "technologies": ["FastAPI"],
                            "role": "Backend Developer",
                        }
                    ],
                    "experiences": [],
                    "education": None,
                },
                "label_source": "resume_exact_catalog_title",
                "source": "public_resume_derived",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    retrieval_path = tmp_path / "retrieval.jsonl"
    retrieval_path.write_text(
        json.dumps(
            {
                "resume_id": "CV-ABCDEF123456",
                "expected_domain": "Backend_Developer",
                "selected_domain": "Backend_Developer",
                "retrieved_contexts": [
                    {
                        "rank": 1,
                        "chunk_id": "topic-fastapi",
                        "topic_id": "topic-fastapi",
                        "topic": "Python > Web > FastAPI",
                        "content": "FastAPI dependency injection and error handling.",
                    }
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "question-run"
    summary = run_questions(
        repo_root=REPO_ROOT,
        dataset_path=dataset_path,
        retrieval_path=retrieval_path,
        output_dir=output_dir,
        provider=FakeProvider(),
        max_cases=1,
    )

    questions = [
        json.loads(line)
        for line in (output_dir / "questions.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    judgments = [
        json.loads(line)
        for line in (output_dir / "judgments.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert questions[0]["resume_id"] == "CV-ABCDEF123456"
    assert questions[0]["condition"] == "CURRENT_PRODUCTION_LEXICAL"
    assert questions[0]["target_topic_id"] == "topic-fastapi"
    assert questions[0]["question"]["question"].startswith("Trong dự án của bạn")
    assert questions[0]["unsupported_experience_assumption"] is True
    assert questions[0]["deterministic_grounding_overlap"] > 0
    assert judgments[0]["judgment"]["technical_validity"] == 1
    assert judgments[0]["judgment"]["rag_grounding"] == 2
    assert summary["sample_count"] == 1
    assert summary["technical_validity_rate"] == 1.0
    assert summary["cv_alignment_rate"] == 1.0
    assert summary["language_match_rate"] == 1.0
    assert summary["difficulty_label_match_rate"] == 1.0
    assert summary["unsupported_experience_assumption_rate"] == 1.0
    assert summary["normalized_exact_duplicate_rate"] == 0.0
    assert summary["target_topic_mention_rate"] == 1.0
    assert summary["by_category"]["software-development"]["sample_count"] == 1
    assert summary["by_language"]["vi"]["technical_validity_rate"] == 1.0

    serialized = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (output_dir / "questions.jsonl", output_dir / "judgments.jsonl")
    )
    assert "private@example.com" not in serialized
    assert "private-name.pdf" not in serialized

    resumed = run_questions(
        repo_root=REPO_ROOT,
        dataset_path=dataset_path,
        retrieval_path=retrieval_path,
        output_dir=output_dir,
        provider=ProviderMustNotBeCalled(),
        max_cases=1,
    )
    assert resumed["sample_count"] == 1
    assert resumed["resumed_completed_cases"] == 1
