from __future__ import annotations

import ast
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ai_lab._runtime import RAW_RESPONSE_LIMITATION, write_artifacts
from ai_lab.ai_cv.agent import CVLabAgent
from ai_lab.ai_cv.prompt import build_prompt as build_cv_prompt
from ai_lab.ai_cv.runner import parse_input as parse_cv_input
from ai_lab.ai_cv.schemas import CandidateProfile as CVCandidateProfile
from ai_lab.ai_evaluator.agent import EvaluatorLabAgent
from ai_lab.ai_evaluator.prompt import build_prompt as build_evaluator_prompt
from ai_lab.ai_evaluator.runner import parse_input as parse_evaluator_input
from ai_lab.ai_evaluator.schemas import AnswerEvaluation, EvaluatorInput
from ai_lab.ai_planner.agent import PlannerLabAgent
from ai_lab.ai_planner.prompt import build_prompt as build_planner_prompt
from ai_lab.ai_planner.runner import parse_input as parse_planner_input
from ai_lab.ai_planner.schemas import InterviewPlan, PlannerInput
from ai_lab.ai_question.agent import QuestionLabAgent
from ai_lab.ai_question.prompt import build_prompt as build_question_prompt
from ai_lab.ai_question.runner import parse_input as parse_question_input
from ai_lab.ai_question.schemas import InterviewQuestion, QuestionInput
from ai_lab.ai_report.agent import ReportLabAgent
from ai_lab.ai_report.prompt import build_prompt as build_report_prompt
from ai_lab.ai_report.runner import parse_input as parse_report_input
from ai_lab.ai_report.schemas import InterviewReport, ReportInput


BACKEND_ROOT = Path(__file__).parents[2]
LAB_ROOT = BACKEND_ROOT / "ai_lab"

LAB_CASES = [
    ("ai_cv", parse_cv_input, CVCandidateProfile, build_cv_prompt),
    ("ai_planner", parse_planner_input, InterviewPlan, build_planner_prompt),
    ("ai_question", parse_question_input, InterviewQuestion, build_question_prompt),
    ("ai_evaluator", parse_evaluator_input, AnswerEvaluation, build_evaluator_prompt),
    ("ai_report", parse_report_input, InterviewReport, build_report_prompt),
]


@pytest.mark.parametrize(("name", "parse_input", "output_schema", "prompt_builder"), LAB_CASES)
def test_examples_validate_and_prompt_builds(name, parse_input, output_schema, prompt_builder):
    directory = LAB_ROOT / name

    input_data = parse_input(directory / "input.example.json")
    output_payload = json.loads((directory / "output.example.json").read_text(encoding="utf-8"))
    output = output_schema.model_validate(output_payload)

    if name == "ai_cv":
        prompt = prompt_builder(input_data.resume_text)
    else:
        prompt = prompt_builder(input_data)

    assert input_data is not None
    assert output is not None
    assert prompt.strip()
    assert "Context:" in prompt or "Untrusted uploaded document" in prompt or "Interview evidence:" in prompt


def test_standalone_agents_import():
    assert CVLabAgent.TEMPERATURE == 0.1
    assert PlannerLabAgent.TASK_TYPE == "simple"
    assert QuestionLabAgent.TEMPERATURE == 0.2
    assert EvaluatorLabAgent.TEMPERATURE == 0.1
    assert ReportLabAgent.TASK_TYPE == "complex"


def test_runner_parsers_return_local_input_contracts():
    assert isinstance(parse_planner_input(LAB_ROOT / "ai_planner/input.example.json"), PlannerInput)
    assert isinstance(parse_question_input(LAB_ROOT / "ai_question/input.example.json"), QuestionInput)
    assert isinstance(parse_evaluator_input(LAB_ROOT / "ai_evaluator/input.example.json"), EvaluatorInput)
    assert isinstance(parse_report_input(LAB_ROOT / "ai_report/input.example.json"), ReportInput)


def test_artifact_writer_creates_complete_run(tmp_path):
    output = CVCandidateProfile(name="Example", skills=["Python"], confidence_score=0.8)
    timestamp = datetime(2026, 1, 2, tzinfo=timezone.utc)

    write_artifacts(
        tmp_path,
        input_payload={"resume_text": "Example Resume"},
        prompt="Extract the Resume",
        output=output,
        ai="ai_cv",
        model="test-model",
        task_type="simple",
        temperature=0.1,
        timestamp=timestamp,
        success=True,
    )

    assert {path.name for path in tmp_path.iterdir()} == {
        "input.json",
        "prompt.txt",
        "raw_response.txt",
        "output.json",
        "metadata.json",
    }
    metadata = json.loads((tmp_path / "metadata.json").read_text(encoding="utf-8"))
    assert metadata == {
        "ai": "ai_cv",
        "model": "test-model",
        "task_type": "simple",
        "temperature": 0.1,
        "timestamp": "2026-01-02T00:00:00+00:00",
        "success": True,
        "raw_response_captured": False,
    }
    assert (tmp_path / "raw_response.txt").read_text(encoding="utf-8") == RAW_RESPONSE_LIMITATION


def test_cv_regression_samples_only_remove_target_heading():
    samples = LAB_ROOT / "ai_cv/samples"
    normal = json.loads((samples / "normal_cv.json").read_text(encoding="utf-8"))["resume_text"]
    variants = {
        "cv_without_skills_heading.json": "SKILLS",
        "cv_without_work_experience_heading.json": "WORK EXPERIENCE",
        "cv_without_projects_heading.json": "PROJECTS",
    }

    assert all(heading in normal for heading in variants.values())
    for filename, removed_heading in variants.items():
        resume_text = json.loads((samples / filename).read_text(encoding="utf-8"))["resume_text"]
        assert removed_heading not in resume_text
        assert "PyTorch" in resume_text
        assert "Vision Labs" in resume_text
        assert "Factory Vision" in resume_text


def test_lab_source_does_not_import_production_ai_implementations():
    prohibited_prefixes = (
        "services.profile_scanner",
        "services.interview_planner",
        "services.question_generator",
        "services.answer_evaluator",
        "services.report_generator",
        "services.prompt_builder",
    )

    for source_path in LAB_ROOT.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
        imported_modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.append(node.module)
        assert not any(
            module.startswith(prohibited_prefixes) for module in imported_modules
        ), f"{source_path} imports a production AI implementation"
