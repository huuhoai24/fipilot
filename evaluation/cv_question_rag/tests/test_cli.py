from __future__ import annotations

from evaluation.cv_question_rag.run_benchmark import build_parser


def test_cli_separates_local_steps_from_explicit_paid_question_execution() -> None:
    parser = build_parser()

    prepared = parser.parse_args(["--prepare", "--corpus-dir", "resumes"])
    assert prepared.prepare is True
    assert prepared.execute_paid_questions is False

    retrieval = parser.parse_args(["--run-retrieval"])
    assert retrieval.run_retrieval is True
    assert retrieval.execute_paid_questions is False

    report = parser.parse_args(["--build-report"])
    assert report.build_report is True

    paid = parser.parse_args(
        ["--execute-paid-questions", "--max-question-cases", "150"]
    )
    assert paid.execute_paid_questions is True
    assert paid.max_question_cases == 150
