"""Deterministic robustness evaluation for FiPilot's current runtime contracts.

This is an evaluation harness, not a production regression suite.  A case can
execute successfully while its product status is FAIL; the JSON evidence keeps
those two concepts separate.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unicodedata
from pathlib import Path
from typing import Any, Callable
from unittest.mock import patch

import pymupdf
from fastapi.testclient import TestClient
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = ROOT.parent.parent / "backend"
sys.path.insert(0, str(BACKEND_ROOT))
os.environ["KNOWLEDGE_RETRIEVAL_BACKEND"] = "local"

from api import main as api_main
from fipilot.interview_engine import evaluate_answer, generate_question, generate_report
from fipilot.interview_planner import create_interview_plan
from fipilot.knowledge_index import _documents, search_domain
from fipilot.resume_extraction import ResumeExtract

RESULTS_PATH = ROOT / "backend_results.json"
ALLOWED_STATUSES = {"PASS", "FAIL", "PARTIAL", "BLOCKED", "NOT TESTED", "NOT EVALUATED"}
results: list[dict[str, Any]] = []


def record(
    test_id: str,
    agent: str,
    scenario: str,
    expected: str,
    actual: Any,
    status: str,
    severity: str = "",
) -> None:
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Unsupported status: {status}")
    results.append(
        {
            "test_id": test_id,
            "agent": agent,
            "scenario": scenario,
            "expected": expected,
            "actual": str(actual),
            "status": status,
            "severity": severity,
        }
    )


def attempt(
    test_id: str,
    agent: str,
    scenario: str,
    expected: str,
    operation: Callable[[], Any],
    predicate: Callable[[Any], bool],
    *,
    severity: str = "",
) -> None:
    started = time.perf_counter()
    try:
        actual = operation()
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        passed = predicate(actual)
        record(
            test_id,
            agent,
            scenario,
            expected,
            {"value": actual, "elapsed_ms": elapsed_ms},
            "PASS" if passed else "FAIL",
            "" if passed else severity,
        )
    except Exception as error:  # evidence capture must continue after a failed case
        record(
            test_id,
            agent,
            scenario,
            expected,
            f"{type(error).__name__}: {error}",
            "FAIL",
            severity,
        )


def write_pdf(path: Path, pages: list[list[tuple[float, float, str] | str]]) -> None:
    document = pymupdf.open()
    for lines in pages:
        page = document.new_page()
        for index, item in enumerate(lines):
            if isinstance(item, tuple):
                x, y, text = item
            else:
                x, y, text = 72, 72 + index * 24, item
            page.insert_text((x, y), text)
    document.save(path)
    document.close()


class ExtractionLLM:
    def __init__(self, response: dict[str, Any]):
        self.response = response
        self.text = ""

    def extract_info(self, text_content, extract_types, resume_id):
        self.text = text_content
        return self.response


class SequenceLLM:
    def __init__(self, *responses: str | dict[str, Any] | Exception):
        self.responses = iter(responses)
        self.prompts: list[dict[str, str]] = []

    def generate_text(self, system_prompt, user_prompt, **_kwargs):
        self.prompts.append({"system": system_prompt, "user": user_prompt})
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        if isinstance(response, str):
            return response
        return json.dumps(response, ensure_ascii=False)


QUESTION = {
    "company": "FiPilot",
    "project": "FiPilot",
    "topic": "HTTP status",
    "question": "HTTP status nao bieu thi Not Found?",
    "rubric": {
        "evaluation_goal": "Xac dinh HTTP Not Found",
        "critical_points": ["Status 404"],
        "met": "Neu dung 404.",
        "partially_met": "Hieu la loi client nhung khong neu 404.",
        "not_met": "Neu sai status.",
    },
}


VALID_QUESTION = {
    "company": "Portfolio",
    "topic": "React rendering",
    "question": "Ban giam re-render trong project React nay nhu the nao?",
    "rubric": {
        "evaluation_goal": "Danh gia quyet dinh toi uu rendering",
        "critical_points": ["Do luong", "Memoization"],
        "met": "Co do luong va giai thich trade-off.",
        "partially_met": "Co mot co che nhung thieu trade-off.",
        "not_met": "Khong neu duoc co che.",
    },
}


def run_resume_cases() -> None:
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        normal = temp / "normal.pdf"
        write_pdf(normal, [["Candidate", "Platform API", "Built FastAPI with PostgreSQL"]])
        llm = ExtractionLLM(
            {
                "skills": ["Python", "python", "FastAPI"],
                "workExperience": [
                    {
                        "type": "Project",
                        "name": "Platform API",
                        "position": "",
                        "description_refer_index_range": [1, 2],
                    }
                ],
            }
        )
        profile = json.loads(ResumeExtract(llm).pipeline(normal))
        record(
            "RESUME-001",
            "ResumeExtract",
            "Normal text PDF",
            "Preserve evidence, schema, and deduplicate skills",
            profile,
            "PASS" if profile["skills"] == ["Python", "FastAPI"] and "Built FastAPI" in profile["workExperience"][0]["jobDescription"] else "FAIL",
            "HIGH",
        )

        blank = temp / "blank.pdf"
        write_pdf(blank, [[]])
        try:
            ResumeExtract(llm).pipeline(blank)
            record("RESUME-002", "PDF extractor", "Blank/scanned PDF", "Clear OCR-required rejection", "accepted", "FAIL", "MEDIUM")
        except ValueError as error:
            record("RESUME-002", "PDF extractor", "Blank/scanned PDF", "Clear OCR-required rejection", error, "PASS")

        vietnamese = temp / "unicode.pdf"
        document = pymupdf.open()
        page = document.new_page()
        font_path = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "arial.ttf"
        page.insert_font(fontname="arial", fontfile=str(font_path))
        for index, line in enumerate(("Nguyễn Văn Trí", "Kỹ sư Trí tuệ Nhân tạo", "Python và FastAPI")):
            page.insert_text((72, 72 + index * 24), line, fontname="arial")
        document.save(vietnamese)
        document.close()
        unicode_llm = ExtractionLLM(
            {
                "skills": ["Python"],
                "workExperience": [{"type": "Project", "name": "Đồ án AI", "position": "", "description_refer_index_range": [0, 2]}],
            }
        )
        unicode_profile = json.loads(ResumeExtract(unicode_llm).pipeline(vietnamese))
        record(
            "RESUME-003",
            "PDF extractor",
            "Vietnamese and emoji text layer",
            "Preserve extractable Vietnamese text without crashing",
            {"prompt": unicode_llm.text, "profile": unicode_profile},
            "PASS" if "Nguyễn" in unicode_llm.text and "Kỹ sư" in unicode_llm.text else "PARTIAL",
            "MEDIUM",
        )

        many_pages = temp / "many-pages.pdf"
        write_pdf(many_pages, [[f"PAGE-{page}"] for page in range(12)])
        pages_llm = ExtractionLLM(
            {"skills": [], "workExperience": [{"type": "Project", "name": "Long CV", "position": "", "description_refer_index_range": [0, 11]}]}
        )
        ResumeExtract(pages_llm).pipeline(many_pages)
        record(
            "RESUME-004",
            "PDF extractor",
            "12-page text PDF",
            "Keep all pages in order",
            pages_llm.text,
            "PASS" if pages_llm.text.index("PAGE-0") < pages_llm.text.index("PAGE-11") else "FAIL",
            "HIGH",
        )

        two_column = temp / "two-column.pdf"
        write_pdf(two_column, [[(72, 72, "LEFT-1"), (300, 72, "RIGHT-1"), (72, 96, "LEFT-2"), (300, 96, "RIGHT-2")]])
        columns_llm = ExtractionLLM(
            {"skills": [], "workExperience": [{"type": "Project", "name": "Columns", "position": "", "description_refer_index_range": [0, 1]}]}
        )
        ResumeExtract(columns_llm).pipeline(two_column)
        record(
            "RESUME-005",
            "PDF extractor",
            "Two-column text PDF",
            "Preserve all four text blocks with deterministic order",
            columns_llm.text,
            "PASS" if all(token in columns_llm.text for token in ("LEFT-1", "RIGHT-1", "LEFT-2", "RIGHT-2")) else "FAIL",
            "HIGH",
        )

        very_long = temp / "very-long.pdf"
        long_lines = [f"Evidence {index} " + ("x" * 80) for index in range(1_600)]
        write_pdf(very_long, [long_lines[index : index + 8] for index in range(0, 1_600, 8)])
        long_llm = ExtractionLLM(
            {"skills": [], "workExperience": [{"type": "Project", "name": "Long", "position": "", "description_refer_index_range": [0, 1_599]}]}
        )
        ResumeExtract(long_llm).pipeline(very_long)
        record(
            "BOUNDARY-001",
            "ResumeExtract",
            "Very long extracted resume context",
            "Bound or reject context before the LLM call",
            f"LLM received {len(long_llm.text)} characters",
            "FAIL" if len(long_llm.text) > 100_000 else "PASS",
            "HIGH",
        )

    client = TestClient(api_main.app)
    record("RESUME-006", "Resume API", "DOCX upload", "Reject unsupported type clearly", client.post("/api/v1/resume/upload", files={"file": ("cv.docx", b"docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}).status_code, "PASS" if client.post("/api/v1/resume/upload", files={"file": ("cv.docx", b"docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}).status_code == 400 else "FAIL")
    over = b"%PDF-" + b"x" * (api_main.MAX_FILE_SIZE - 4)
    response = client.post("/api/v1/resume/upload", files={"file": ("cv.pdf", over, "application/pdf")})
    record("BOUNDARY-002", "Resume API", "File size limit +1", "HTTP 413", response.status_code, "PASS" if response.status_code == 413 else "FAIL", "HIGH")
    exact = b"%PDF-" + b"x" * (api_main.MAX_FILE_SIZE - 5)
    fake_payload = json.dumps({"skills": [], "workExperience": [{"type": "Project", "name": "Boundary", "position": "", "jobDescription": "Exact limit"}], "roleMatches": []})
    fake_extractor = type("Extractor", (), {"pipeline": lambda _self, _path: fake_payload})()
    with patch("api.main.get_extractor", return_value=fake_extractor):
        response = client.post("/api/v1/resume/upload", files={"file": ("cv.pdf", exact, "application/pdf")})
    record("BOUNDARY-003", "Resume API", "File size exact limit", "Accepted", response.status_code, "PASS" if response.status_code == 200 else "FAIL", "HIGH")
    corrupt = client.post("/api/v1/resume/upload", files={"file": ("broken.pdf", b"%PDF-corrupt", "application/pdf")})
    record("RESUME-007", "Resume API", "Corrupted PDF", "Clear client-data rejection (4xx)", {"status": corrupt.status_code, "body": corrupt.text[:200]}, "FAIL" if corrupt.status_code >= 500 else "PASS", "MEDIUM")


def run_profile_and_plan_cases() -> None:
    skills_only = ExtractionLLM({"skills": ["Python", "FastAPI"], "workExperience": []})
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "skills.pdf"
        write_pdf(path, [["Python", "FastAPI"]])
        profile = json.loads(ResumeExtract(skills_only).pipeline(path))
    actual = {
        "workExperience": profile["workExperience"],
        "skillEvidence": profile["skillEvidence"],
    }
    status = "PASS" if not profile["workExperience"] and all(
        item["scope"] == "unknown" for item in profile["skillEvidence"]
    ) else "FAIL"
    record("PROFILE-001", "ResumeExtract", "Skills only, no experience", "Preserve skill evidence without inventing company or experience", actual, status, "CRITICAL")

    composed = "Café"
    decomposed = unicodedata.normalize("NFD", composed)
    llm = ExtractionLLM(
        {"skills": [composed, decomposed], "workExperience": [{"type": "Project", "name": "Unicode", "position": "", "description_refer_index_range": [0, 0]}]}
    )
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "unicode-skills.pdf"
        write_pdf(path, [["Unicode project"]])
        profile = json.loads(ResumeExtract(llm).pipeline(path))
    record("PROFILE-002", "ResumeExtract", "Canonically equivalent duplicate skills", "Normalize to one skill", profile["skills"], "PASS" if len(profile["skills"]) == 1 else "FAIL", "LOW")

    plan = create_interview_plan(
        work_experience=[{"type": "Project", "name": "React portfolio", "position": "Frontend Developer", "jobDescription": "Built React and CSS screens."}],
        role="Data Engineer",
        level="Senior",
        retrieve=lambda *_args: [],
    )
    record("PLAN-001", "create_interview_plan", "Frontend fresher selected as Senior Data Engineer", "Detect mismatch or avoid asserting senior data-engineering fit", plan, "FAIL" if plan["rounds"][0]["difficulty"] == "hard" and "Data Engineer" in plan["rounds"][0]["objective"] else "PASS", "HIGH")

    no_description = create_interview_plan(
        work_experience=[{"type": "Project", "name": "Student project", "position": "", "jobDescription": ""}],
        role="Backend Developer",
        level="Junior",
        retrieve=lambda *_args: (_ for _ in ()).throw(AssertionError("retriever must not run")),
    )
    record("PLAN-002", "create_interview_plan", "Empty project description", "No crash and explicit weak-evidence handling", no_description, "PARTIAL" if no_description["rounds"] else "FAIL", "MEDIUM")

    six = [
        {"type": "Project", "name": f"P{index}", "position": "", "jobDescription": "Python API"}
        for index in range(6)
    ]
    bounded = create_interview_plan(work_experience=six, role="Backend Developer", level="Junior", retrieve=lambda *_args: [])
    record("BOUNDARY-004", "create_interview_plan", "max_rounds default +1", "Return at most 5 rounds", len(bounded["rounds"]), "PASS" if len(bounded["rounds"]) == 5 else "FAIL", "MEDIUM")

    malformed = create_interview_plan(work_experience=[{}], role="Backend Developer", level="Junior", retrieve=lambda *_args: [])
    record("FLOW-001", "Profile -> Plan", "Missing all experience fields", "Reject unusable evidence before planning", malformed, "FAIL" if malformed["rounds"] else "PASS", "HIGH")


def run_rag_cases() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "Knowledge"
        domain = root / "Domains" / "Backend Developer"
        domain.mkdir(parents=True)
        (domain / "Transactions.md").write_text("# Transactions\nPostgreSQL transaction rollback and isolation.", encoding="utf-8")
        (domain / "CSS.md").write_text("# CSS\nResponsive grid and colors.", encoding="utf-8")
        _documents.cache_clear()
        with patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root), patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing"):
            exact = search_domain("PostgreSQL transaction rollback", "Backend Developer", 2)
        record("RAG-001", "search_domain", "Exact match with irrelevant noise", "Relevant transaction chunk ranks first", exact, "PASS" if exact and exact[0]["source"].endswith("Transactions.md") else "FAIL", "HIGH")

        (domain / "Scale.md").write_text("Reduced API response time with Redis caching and horizontal scaling.", encoding="utf-8")
        _documents.cache_clear()
        with patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root), patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing"):
            semantic = search_domain("How did the candidate improve system scalability?", "Backend Developer", 3)
        record("RAG-002", "search_domain", "Semantic match without shared key terms", "Retrieve caching/horizontal scaling chunk", semantic, "PASS" if any(hit["source"].endswith("Scale.md") for hit in semantic) else "FAIL", "HIGH")

        (domain / "Duplicate-A.md").write_text("# Cache\nRedis cache invalidation ownership.", encoding="utf-8")
        (domain / "Duplicate-B.md").write_text("# Cache\nRedis cache invalidation ownership.", encoding="utf-8")
        _documents.cache_clear()
        with patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root), patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing"):
            duplicates = search_domain("Redis cache invalidation ownership", "Backend Developer", 5)
        duplicate_contents = [hit["content"] for hit in duplicates]
        record("RAG-003", "search_domain", "Duplicate chunks", "Deduplicate near-identical content", duplicates, "PASS" if len(duplicate_contents) == len(set(duplicate_contents)) else "FAIL", "MEDIUM")

        _documents.cache_clear()
        with patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root), patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing"):
            none = search_domain("quantum entanglement satellite", "Backend Developer", 3)
        record("RAG-004", "search_domain", "No matching knowledge", "Return [] without invented evidence", none, "PASS" if none == [] else "FAIL", "HIGH")


def run_llm_contract_cases() -> None:
    project = {"type": "Project", "name": "Portfolio", "position": "", "jobDescription": "Built React screens."}
    q = generate_question(SequenceLLM(VALID_QUESTION), project, "Web Developer", "Junior", [])
    record("QGEN-001", "generate_question", "Empty RAG result", "Generate schema-valid grounded question", q, "PASS" if q["rubric"]["critical_points"] else "FAIL", "HIGH")

    fenced = "```json\n" + json.dumps(VALID_QUESTION) + "\n```"
    try:
        parsed = generate_question(SequenceLLM(fenced), project, "Web Developer", "Junior", [])
        record("LLM-001", "Question parser", "Markdown-wrapped JSON", "Recover valid JSON", parsed, "PASS")
    except Exception as error:
        record("LLM-001", "Question parser", "Markdown-wrapped JSON", "Recover valid JSON", error, "FAIL", "MEDIUM")

    preamble = "Sure! Here is the result:\n" + json.dumps(VALID_QUESTION)
    try:
        parsed = generate_question(SequenceLLM(preamble), project, "Web Developer", "Junior", [])
        record("LLM-002", "Question parser", "Text before JSON", "Recover valid JSON", parsed, "PASS")
    except Exception as error:
        record("LLM-002", "Question parser", "Text before JSON", "Recover valid JSON", error, "FAIL", "MEDIUM")

    try:
        generate_question(SequenceLLM(""), project, "Web Developer", "Junior", [])
        record("LLM-003", "Question parser", "Empty provider response", "Reject malformed output", "accepted", "FAIL", "HIGH")
    except Exception as error:
        record("LLM-003", "Question parser", "Empty provider response", "Reject malformed output", type(error).__name__, "PASS")

    distinct_question = {
        **VALID_QUESTION,
        "topic": "Accessibility",
        "question": "Ban kiem tra keyboard accessibility trong project nay nhu the nao?",
    }
    repeated = SequenceLLM(VALID_QUESTION, VALID_QUESTION, distinct_question)
    first = generate_question(repeated, project, "Web Developer", "Junior", [])
    second = generate_question(
        repeated,
        project,
        "Web Developer",
        "Junior",
        [],
        previous_questions=[first["question"]],
    )
    record("QGEN-002", "generate_question", "Duplicate across interview history", "Detect or prevent semantic duplicate", [first["question"], second["question"]], "FAIL" if first["question"] == second["question"] else "PASS", "HIGH")

    malicious = {
        "score": 3,
        "evidence_quote": "invented quote",
        "justification": "Correct",
        "should_follow_up": True,
        "next_direction": "More",
        "matched_points": [],
        "missing_points": [],
        "technical_errors": [],
    }
    evaluation = evaluate_answer(SequenceLLM(malicious), QUESTION, "I do not know.")
    record("EVAL-001", "evaluate_answer", "Hallucinated evidence quote", "Clamp to NOT_ASSESSED", evaluation, "PASS" if evaluation["score"] == 0 and not evaluation["evidence_quote"] else "FAIL", "CRITICAL")

    empty = {**malicious, "evidence_quote": ""}
    evaluation = evaluate_answer(SequenceLLM(empty), QUESTION, "")
    record("EVAL-002", "evaluate_answer", "Empty answer", "Never award a positive score", evaluation, "PASS" if evaluation["score"] == 0 else "FAIL", "CRITICAL")

    assumed_experience_question = {
        **QUESTION,
        "topic": "Unverified orchestration platform",
        "question": "How did you operate this orchestration platform in production?",
    }
    denial = "I have not used that orchestration platform directly."
    unsupported = evaluate_answer(
        SequenceLLM(
            {
                "score": 1,
                "evidence_quote": denial,
                "justification": "Candidate did not explain production operations.",
                "should_follow_up": True,
                "next_direction": "Explain production operations.",
                "matched_points": [],
                "missing_points": ["Production operations"],
                "technical_errors": [],
            }
        ),
        assumed_experience_question,
        denial,
        candidate_context={"jobDescription": "Built containerized services."},
    )
    record(
        "EVAL-REG-01",
        "evaluate_answer",
        "Candidate denies an experience absent from supplied evidence",
        "Treat the unsupported premise as NOT_ASSESSED without follow-up",
        unsupported,
        "PASS" if unsupported["score"] == 0 and not unsupported["should_follow_up"] else "FAIL",
        "HIGH",
    )

    out_of_range = {**malicious, "score": 11}
    try:
        evaluate_answer(SequenceLLM(out_of_range), QUESTION, "invented quote")
        record("FLOW-002", "Evaluation parser", "Score outside 0-10", "Reject invalid score", "accepted", "FAIL", "CRITICAL")
    except ValidationError as error:
        record("FLOW-002", "Evaluation parser", "Score outside 0-10", "Reject invalid score", error.errors()[0]["type"], "PASS")

    missing_feedback = {"score": 1, "evidence_quote": "404"}
    try:
        evaluate_answer(SequenceLLM(missing_feedback), QUESTION, "404")
        record("FLOW-003", "Evaluation parser", "Missing evaluation fields", "Reject invalid schema", "accepted", "FAIL", "HIGH")
    except ValidationError as error:
        record("FLOW-003", "Evaluation parser", "Missing evaluation fields", "Reject invalid schema", len(error.errors()), "PASS")

    report = generate_report(SequenceLLM(), "Backend Developer", "Junior", [])
    record("REPORT-001", "generate_report", "No interview turns", "Return an explicit unassessed report without LLM call", report, "PASS" if report["coverage_ratio"] == 0 and report["normalized_score"] == 0 else "FAIL", "HIGH")

    timestamp = "2026-08-23T12:00:00+07:00"
    turns = [
        {"question": QUESTION, "answer": "404", "timestamp": timestamp},
        {"question": QUESTION, "answer": "", "timestamp": timestamp + "-2"},
        {"question": QUESTION, "answer": "", "timestamp": timestamp + "-3"},
    ]
    high_one = {
        "assessments": [{"turn_index": 0, "raw_score": 10, "rationale": "Dung", "evidence": [{"timestamp": timestamp, "quote": "404"}]}],
        "solutions_summary": "Only one answer was correct.",
        "overall_assessment": "Insufficient evidence.",
        "recommendations": "Answer more questions.",
    }
    scored = generate_report(SequenceLLM(high_one), "Backend Developer", "Junior", turns)
    record("REPORT-002", "generate_report", "One strong answer and two unassessed turns", "Preserve the assessed score and expose incomplete coverage", scored, "PASS" if scored["normalized_score"] == 10.0 and scored["coverage_ratio"] < 1 else "FAIL", "CRITICAL")

    contradiction = {
        "assessments": [
            {"turn_index": 0, "raw_score": 10, "rationale": "Dung", "evidence": [{"timestamp": timestamp, "quote": "404"}]}
        ],
        "solutions_summary": "Khong co kien thuc ky thuat.",
        "overall_assessment": "Ung vien rat yeu.",
        "recommendations": "Hoc lai tu dau.",
    }
    contradictory_report = generate_report(SequenceLLM(contradiction), "Backend Developer", "Junior", [turns[0]])
    record("REPORT-003", "generate_report", "Score-summary contradiction", "Detect or reconcile contradictory narrative", contradictory_report, "FAIL" if contradictory_report["normalized_score"] >= 8.0 and "rat yeu" in contradictory_report["overall_assessment"] else "PASS", "HIGH")


def run_api_boundaries() -> None:
    base = {
        "role": "Backend Developer",
        "level": "Junior",
        "work_experience": [{"type": "Project", "name": "API", "position": "", "jobDescription": "FastAPI"}],
        "current_question": VALID_QUESTION,
        "current_project": {"name": "API", "jobDescription": "FastAPI"},
        "follow_up_count": 0,
    }
    for suffix, length, expected in (("minus-one", 19_999, True), ("limit", 20_000, True), ("plus-one", 20_001, False)):
        payload = {**base, "answer": "x" * length}
        try:
            api_main.InterviewNextRequest.model_validate(payload)
            accepted = True
        except ValidationError:
            accepted = False
        record(f"BOUNDARY-ANSWER-{suffix}", "InterviewNextRequest", f"Answer length {length}", "Accepted through 20,000; reject 20,001", accepted, "PASS" if accepted == expected else "FAIL", "HIGH")

    client = TestClient(api_main.app)
    empty = client.post("/api/v1/interview/questions", json={"role": "Backend Developer", "level": "Junior", "work_experience": []})
    record("FLOW-004", "Interview API", "Empty work_experience", "HTTP 422 before downstream agents", empty.status_code, "PASS" if empty.status_code == 422 else "FAIL", "HIGH")

    request = api_main.InterviewQuestionRequest(role="Backend Developer", level="Junior", work_experience=base["work_experience"])
    with patch("api.main.create_plan", return_value={"role": "Backend Developer", "level": "Junior", "coverage_goals": [], "rounds": [{"round_id": "round-1", "evidence_index": 0, "topic": "API", "difficulty": "medium", "objective": "Validate", "reasoning": "Resume", "knowledge": []}]}), patch("api.main.get_question_llm", return_value=SequenceLLM(TimeoutError("provider timed out"))), patch("api.main.persist"):
        try:
            api_main.generate_interview_questions(request)
            status, actual = "FAIL", "accepted"
        except Exception as error:
            status, actual = ("PARTIAL", f"{getattr(error, 'status_code', None)} generic response")
    record("FLOW-005", "Question API", "Provider timeout", "Bounded timeout with distinguishable/retryable failure", actual, status, "MEDIUM")


def main() -> None:
    run_resume_cases()
    run_profile_and_plan_cases()
    run_rag_cases()
    run_llm_contract_cases()
    run_api_boundaries()
    summary = {status: sum(item["status"] == status for item in results) for status in ALLOWED_STATUSES}
    RESULTS_PATH.write_text(json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"results": len(results), "summary": summary, "evidence": str(RESULTS_PATH)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
