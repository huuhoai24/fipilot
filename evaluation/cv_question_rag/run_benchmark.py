from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluation.cv_question_rag.dataset import prepare_dataset
from evaluation.cv_question_rag.questions import (
    create_vertex_provider,
    plan_question_run,
    run_questions,
)
from evaluation.cv_question_rag.retrieval import run_retrieval
from evaluation.cv_question_rag.reporting import build_reports


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET_DIR = ROOT / "evaluation/cv_question_rag/datasets/public-resumes-v1"
DEFAULT_RUN_DIR = ROOT / "evaluation/cv_question_rag/raw/public-resumes-v1"
DEFAULT_DOCS_DIR = ROOT / "docs/evaluation/cv_question_rag"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Privacy-safe public-Resume Question Generation and Retrieval evaluation"
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--prepare", action="store_true")
    action.add_argument("--run-retrieval", action="store_true")
    action.add_argument("--dry-run-questions", action="store_true")
    action.add_argument("--execute-paid-questions", action="store_true")
    action.add_argument("--build-report", action="store_true")
    parser.add_argument("--corpus-dir", type=Path, default=ROOT / "resumes")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--sample-size", type=int, default=300)
    parser.add_argument("--corpus-limit", type=int, default=500)
    parser.add_argument("--development-ratio", type=float, default=0.5)
    parser.add_argument("--max-question-cases", type=int, default=150)
    parser.add_argument("--seed", type=int, default=20260820)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    dataset_dir = args.dataset_dir.resolve()
    run_dir = args.run_dir.resolve()
    if args.prepare:
        result = prepare_dataset(
            corpus_dir=args.corpus_dir.resolve(),
            catalog_path=ROOT / "backend/services/interview_knowledge/catalog.json",
            output_dir=dataset_dir,
            corpus_limit=args.corpus_limit,
            sample_size=args.sample_size,
            development_ratio=args.development_ratio,
            seed=args.seed,
        )
    elif args.run_retrieval:
        result = run_retrieval(
            repo_root=ROOT,
            dataset_path=dataset_dir / "corpus_manifest.jsonl",
            output_dir=run_dir,
            seed=args.seed,
        )
    elif args.dry_run_questions:
        result = plan_question_run(
            repo_root=ROOT,
            dataset_path=dataset_dir / "holdout.jsonl",
            retrieval_path=run_dir / "retrieval.jsonl",
            max_cases=args.max_question_cases,
        )
        run_dir.mkdir(parents=True, exist_ok=True)
        (run_dir / "QUESTION_DRY_RUN.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    elif args.build_report:
        result = build_reports(
            dataset_dir=dataset_dir,
            run_dir=run_dir,
            docs_dir=args.docs_dir.resolve(),
            review_sample_size=60,
            seed=args.seed,
        )
    else:
        result = plan_question_run(
            repo_root=ROOT,
            dataset_path=dataset_dir / "holdout.jsonl",
            retrieval_path=run_dir / "retrieval.jsonl",
            max_cases=args.max_question_cases,
        )
        provider = create_vertex_provider(ROOT)
        result = run_questions(
            repo_root=ROOT,
            dataset_path=dataset_dir / "holdout.jsonl",
            retrieval_path=run_dir / "retrieval.jsonl",
            output_dir=run_dir,
            provider=provider,
            max_cases=args.max_question_cases,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
