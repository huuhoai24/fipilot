"""Focused semantic mutation evaluation for the current FiPilot pipeline."""

from __future__ import annotations

import copy
import json
import os
import sys
import uuid
from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from dotenv import load_dotenv
from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(BACKEND / ".env")

from api.main import resolve_interview_context
from fipilot.database import database_session
from fipilot.interview_engine import evaluate_answer, generate_question, generate_report
from fipilot.interview_planner import create_interview_plan
from fipilot.models import Resume
from fipilot.role_matching import match_resume_roles


RESULTS = ROOT / "evaluation" / "agent_robustness" / "semantic_edge_results.json"
VALID = {"PASS", "FAIL", "PARTIAL", "BLOCKED"}
results: list[dict[str, Any]] = []


def record(
    test_id: str,
    agent: str,
    mutation: str,
    expected: str,
    actual: str,
    status: str,
    failure_type: str = "",
    severity: str = "",
    first_wrong_stage: str = "",
) -> None:
    assert status in VALID
    results.append(
        {
            "test_id": test_id,
            "agent": agent,
            "mutation": mutation,
            "expected": expected,
            "actual": actual,
            "status": status,
            "failure_type": failure_type,
            "severity": severity,
            "first_wrong_stage": first_wrong_stage,
        }
    )


class StubLLM:
    def __init__(self, *responses: dict[str, Any]):
        self.responses = iter(responses)
        self.calls: list[dict[str, str]] = []

    def generate_text(self, system_prompt: str, user_prompt: str, **_kwargs) -> str:
        self.calls.append({"system": system_prompt, "user": user_prompt})
        return json.dumps(next(self.responses), ensure_ascii=False)


def question(text: str, topic: str = "Evidence scope") -> dict[str, Any]:
    return {
        "company": "Candidate evidence",
        "topic": topic,
        "question": text,
        "rubric": {
            "evaluation_goal": "Validate only the supplied evidence",
            "critical_points": ["Concrete mechanism", "Supported scope"],
            "met": "Both points are correct.",
            "partially_met": "One point is supported.",
            "not_met": "The answer is wrong or unsupported.",
        },
    }


def plan(
    work: list[dict[str, Any]] | None,
    role: str = "AI Engineer",
    level: str = "Intern",
    jd: str = "",
    *,
    skills: list[str] | None = None,
    skill_evidence: list[dict[str, Any]] | None = None,
    education: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return create_interview_plan(
        work_experience=work,
        skills=skills,
        skill_evidence=skill_evidence,
        education=education,
        role=role,
        level=level,
        job_description=jd,
        retrieve=lambda *_args: [],
    )


def accepted_bad_question(project: dict[str, Any], text: str, *, role: str = "AI Engineer", level: str = "Junior", hits: list[dict[str, Any]] | None = None) -> bool:
    output = question(text)
    try:
        generated = generate_question(
            StubLLM(output, output),
            project,
            role,
            level,
            hits or [],
            interview_round={"role": role, "level": level, "evidence_index": 0},
        )
        return generated["question"] == text
    except ValueError:
        return False


def eval_result(
    q: dict[str, Any], answer: str, context: dict[str, Any], *, score: int, matched: list[str] | None = None,
    missing: list[str] | None = None, errors: list[str] | None = None,
) -> dict[str, Any]:
    response = {
        "score": score,
        "evidence_quote": answer,
        "justification": "Synthetic semantic evidence decision.",
        "should_follow_up": score in {4, 5, 6, 7},
        "next_direction": "Clarify scope" if score in {4, 5, 6, 7} else "",
        "matched_points": matched or [],
        "missing_points": missing or [],
        "technical_errors": errors or [],
    }
    return evaluate_answer(StubLLM(response), q, answer, candidate_context=context)


def report_result(
    turns: list[dict[str, Any]],
    assessments: list[dict[str, Any]],
    narrative: str,
    *,
    candidate_context=None,
) -> dict[str, Any]:
    return generate_report(
        StubLLM(
            {
                "assessments": assessments,
                "solutions_summary": narrative,
                "overall_assessment": narrative,
                "recommendations": narrative,
            }
        ),
        "AI Engineer",
        "Intern",
        turns,
        candidate_context=candidate_context,
    )


def load_baseline() -> dict[str, Any]:
    with database_session() as db:
        if db is None:
            raise RuntimeError("PostgreSQL is not configured")
        row = db.scalar(
            select(Resume)
            .where(Resume.filename == "CV_hoainh.pdf")
            .order_by(Resume.created_at.desc())
            .limit(1)
        )
        if row is None:
            raise RuntimeError("Persisted real-CV baseline was not found")
        return copy.deepcopy(row.profile)


def run() -> None:
    baseline = load_baseline()
    work = baseline["workExperience"]
    projects = [item for item in work if item.get("type") == "Project"]
    jobs = [item for item in work if item.get("type") == "Work"]
    base_role = (baseline.get("roleMatches") or match_resume_roles(skills=baseline.get("skills", []), work_experience=work))[0]["title"]

    # A. Experience mutations.
    p = plan(projects, base_role)
    record("EXP-001", "Planner", "Remove all Work; retain projects", "Projects remain interviewable without work-history claims", f"rounds={len(p['rounds'])}, types=Project", "PASS" if len(p["rounds"]) == len(projects) else "FAIL")
    p = plan([item for item in work if "intern" not in str(item.get("position", "")).casefold()], base_role)
    record("EXP-002", "Planner", "Remove internship only", "Internship disappears and projects remain", f"rounds={len(p['rounds'])}", "PASS" if len(p["rounds"]) == len(projects) else "FAIL")
    converted = copy.deepcopy(work[0]); converted["type"] = "Project"; converted["name"] = "Personal prototype"
    p = plan([converted], base_role)
    record("EXP-003", "Planner", "Convert work to personal prototype", "Evidence remains with Prototype provenance", p["rounds"][0]["reasoning"], "PASS" if "Prototype evidence" in p["rounds"][0]["reasoning"] else "FAIL")
    no_company = copy.deepcopy(work[0]); no_company["name"] = ""
    p = plan([no_company], base_role)
    record("EXP-004", "Planner", "Work without company", "Unknown company does not erase other evidence", f"rounds={len(p['rounds'])}", "PASS" if len(p["rounds"]) == 1 else "FAIL")
    vague_project = {"type": "Project", "name": "Independent utility", "position": "", "jobDescription": "Built a small Python utility."}
    p = plan([vague_project], "Software Engineer")
    record("EXP-005", "Planner", "Project without team or role", "No team/ownership fact is invented", p["rounds"][0]["reasoning"], "PASS" if "team" not in p["rounds"][0]["reasoning"].casefold() else "FAIL")

    # B. Years and seniority mutations.
    five = [{"type": "Work", "name": "Platform", "position": "Engineer", "jobDescription": "5 years building Python services."}]
    p = plan(five, "Backend Developer", "Senior")
    record("YEAR-001", "Planner", "Add explicit 5 years", "Senior level may be supported", p["rounds"][0]["level"], "PASS" if p["rounds"][0]["level"] == "Senior" else "FAIL")
    no_year = copy.deepcopy(five); no_year[0]["jobDescription"] = "Built Python services with failure handling."
    p = plan(no_year, "Backend Developer", "Senior")
    record("YEAR-002", "Planner", "Remove numeric years; keep descriptions", "Do not invent seniority", p["rounds"][0]["level"], "PASS" if p["rounds"][0]["level"] == "Junior" else "FAIL")
    three = copy.deepcopy(five); three[0]["jobDescription"] = "3 years building Python services."
    p = plan(three, "Backend Developer", "Middle")
    record("YEAR-003", "Planner", "Increase 1 year to 3 years", "Middle may be supported by explicit evidence", p["rounds"][0]["level"], "PASS" if p["rounds"][0]["level"] == "Middle" else "FAIL")
    one = copy.deepcopy(five); one[0]["jobDescription"] = "1 year building Python services."
    p = plan(one, "Backend Developer", "Senior")
    record("YEAR-004", "Planner", "Decrease 5 years to 1 year", "Senior must be rejected", p["rounds"][0]["level"], "PASS" if p["rounds"][0]["level"] == "Junior" else "FAIL")
    two = copy.deepcopy(five); two[0]["jobDescription"] = "2 years building Python services."
    p = plan(two, "Backend Developer", "Senior")
    record("YEAR-005", "Planner", "CV says 2 years; target is Senior", "Do not promote; expose candidate-vs-target level conflict", f"candidate={p['candidate_level']}; target={p['target_level']}; level_conflict={p['level_conflict']}", "PASS" if p["candidate_level"] == "Entry" and p["target_level"] == "Senior" and p["level_conflict"] else "FAIL")
    over_two = copy.deepcopy(five); over_two[0]["jobDescription"] = "Over 2 years building Python services."
    p = plan(over_two, "Backend Developer", "Middle")
    record("YEAR-006", "Planner", "Ambiguous 'over 2 years'", "Do not round up to 3", p["rounds"][0]["level"], "PASS" if p["rounds"][0]["level"] == "Junior" else "FAIL")

    # C. Role conflicts.
    cases = {
        "ROLE-001": ({"type": "Work", "name": "Web app", "position": "Backend Developer", "jobDescription": "Implemented React UI, CSS, accessibility and browser state."}, "Backend Developer", {"Web Developer"}),
        "ROLE-002": ({"type": "Work", "name": "ML pipeline", "position": "Data Engineer", "jobDescription": "Trained neural models with PyTorch, computer vision and model evaluation."}, "Data Engineer", {"AI Engineer", "Data Scientist"}),
        "ROLE-003": ({"type": "Project", "name": "Full-stack app", "position": "Full-stack Developer", "jobDescription": "Built React UI, Python API and PostgreSQL persistence."}, "Full Stack Developer", {"Full Stack Developer", "Backend Developer", "Web Developer", "Software Engineer"}),
    }
    for test_id, (entry, target, allowed) in cases.items():
        p = plan([entry], target, "Junior")
        actual_role = p["rounds"][0]["role"]
        ok = actual_role in allowed
        record(test_id, "Role inference", entry["position"] + " vs task evidence", "Task evidence must prevent title-only role confusion", actual_role, "PASS" if ok else "FAIL", "ROLE_CONFUSION" if not ok else "", "HIGH" if not ok else "", "Role inference" if not ok else "")
    jd_only = [{"type": "Project", "name": "Frontend portfolio", "position": "Frontend Developer", "jobDescription": "Built React UI and CSS."}]
    p = plan(jd_only, "Data Engineer", "Senior", "Senior data role using distributed pipelines")
    mismatch = p["rounds"][0]
    record("ROLE-004", "Planner", "JD-only role absent from CV", "Explicit mismatch and no target-role assumption", f"role={mismatch['role']}; {mismatch['reasoning']}", "PASS" if mismatch["role"] != "Data Engineer" and "mismatch" in mismatch["reasoning"].casefold() else "FAIL")

    # D. Skills.
    strongest = baseline["skills"][0]
    removed = [s for s in baseline["skills"] if s != strongest]
    removed_evidence = [
        item
        for item in baseline.get("skillEvidence", [])
        if isinstance(item, dict) and item.get("skill") != strongest
    ]
    mutated_plan = plan(
        work,
        base_role,
        skills=removed,
        skill_evidence=removed_evidence,
    )
    skills_preserved = (
        mutated_plan["skills"] == removed
        and mutated_plan["skill_evidence"] == removed_evidence
        and strongest not in mutated_plan["skills"]
    )
    record(
        "SKILL-001",
        "Profile propagation",
        "Remove strongest skill and its structured evidence",
        "Planner receives the current authoritative skills and structured evidence",
        f"skills_before={len(baseline['skills'])}; after={len(removed)}; "
        f"skill_evidence_after={len(removed_evidence)}; preserved={skills_preserved}",
        "PASS" if skills_preserved else "FAIL",
        "DATA_LOSS" if not skills_preserved else "",
        "MEDIUM" if not skills_preserved else "",
        "Profile→Planner" if not skills_preserved else "",
    )
    familiarity = plan(
        [],
        base_role,
        skills=[strongest],
        skill_evidence=[{"skill": strongest, "scope": "familiarity", "source": "resume"}],
    )
    familiarity_round = familiarity["rounds"][0] if familiarity["rounds"] else {}
    record(
        "SKILL-002",
        "Profile propagation",
        "Change strong skill to familiarity only",
        "Skill proficiency scope must reach planning",
        f"scope={familiarity_round.get('candidate_scope')}; topic={familiarity_round.get('topic')}",
        "PASS" if familiarity_round.get("candidate_scope") == "Familiarity" else "FAIL",
    )
    kb_project = {"type": "Project", "name": "Simple API", "position": "Backend Developer", "jobDescription": "Built a small Python API."}
    bad = accepted_bad_question(kb_project, "Bạn đã vận hành công nghệ chỉ có trong JD ở production như thế nào?", hits=[{"source": "JD.md", "content": "JD-only event platform", "score": 1.0}])
    record("SKILL-003", "QGen", "Skill appears only in JD/knowledge", "Must not become a candidate claim", f"unsupported question accepted={bad}", "FAIL" if bad else "PASS", "QGEN_GROUNDING_FAILURE", "HIGH", "QGen")
    roles_once = match_resume_roles(skills=["Python"], work_experience=[])
    roles_unicode = match_resume_roles(skills=["Ｐｙｔｈｏｎ", "PYTHON"], work_experience=[])
    signature = lambda items: [(item["title"], item["score"]) for item in items]
    record("SKILL-004", "Role inference", "Unicode-width/case mismatch", "Canonicalization preserves the same role evidence", f"same_role_share={signature(roles_once) == signature(roles_unicode)}", "PASS" if signature(roles_once) == signature(roles_unicode) else "FAIL")
    roles_once = match_resume_roles(skills=["Python"], work_experience=[])
    roles_duplicate = match_resume_roles(skills=["Python", "python", "PYTHON"], work_experience=[])
    record("SKILL-005", "Role inference", "Duplicate skill spellings", "Duplicates do not change role evidence", f"same_result={roles_once == roles_duplicate}", "PASS" if roles_once == roles_duplicate else "FAIL")
    niche = [{"type": "Project", "name": "Research prototype", "position": "Research Developer", "jobDescription": "Implemented a niche symbolic optimization method."}]
    p = plan(niche, "AI Engineer")
    record("SKILL-006", "Planner", "Niche skill without knowledge hit", "Resume evidence remains interviewable", f"rounds={len(p['rounds'])}; knowledge={len(p['rounds'][0]['knowledge'])}", "PASS" if p["rounds"] and not p["rounds"][0]["knowledge"] else "FAIL")

    # E. Project mutations.
    p = plan(work[1:], base_role)
    record("PROJ-001", "Planner", "Remove flagship project", "Removed item must not appear in rounds", f"rounds={len(p['rounds'])}", "PASS" if len(p["rounds"]) == len(work) - 1 else "FAIL")
    generic = copy.deepcopy(work); generic[1] = {"type": "Project", "name": "Business dashboard", "position": "", "jobDescription": "Displayed business records and filters."}
    p = plan(generic, base_role)
    record("PROJ-002", "Planner", "Replace AI project with generic business project", "Round uses replacement evidence", p["rounds"][1]["topic"], "PASS" if p["rounds"][1]["topic"] == "Business dashboard" else "FAIL")
    metric_bad = accepted_bad_question(generic[1], "Bạn đã đạt 99.9% accuracy trong dự án này như thế nào?")
    record("PROJ-003", "QGen", "Unsupported impressive metric", "Unsupported metric must be rejected", f"accepted={metric_bad}", "FAIL" if metric_bad else "PASS", "QGEN_GROUNDING_FAILURE", "HIGH", "QGen")
    typo = [{"type": "Project", "name": "Tool", "position": "Enginer", "jobDescription": "Improved an internal workflow."}]
    p = plan(typo, "Data Engineer", "Senior")
    record("PROJ-004", "Planner", "Ambiguous role typo with no role evidence", "Role remains unknown/mismatch; target role not adopted as fact", p["rounds"][0]["role"], "FAIL" if p["rounds"][0]["role"] == "Data Engineer" else "PASS", "ROLE_CONFUSION", "HIGH", "Planner")
    old = [{"type": "Project", "name": "Legacy tool", "position": "Developer", "jobDescription": "Maintained a Python 2 utility and documented migration risks."}]
    p = plan(old, "Software Engineer", "Junior")
    record("PROJ-005", "Planner", "Outdated technology", "Keep evidence without upgrading it", p["rounds"][0]["topic"], "PASS" if p["rounds"] else "FAIL")

    # F. Education evidence reaches planning without becoming work experience.
    ai_education = [{"institution": "FPT University", "degree": "Bachelor of Engineering", "field_of_study": "Artificial Intelligence"}]
    education_only = plan([], "AI Engineer", education=ai_education)
    record("EDU-001", "Profile→Planner", "Add relevant education only", "Education can provide interviewable fresher evidence", f"rounds={len(education_only['rounds'])}; level={education_only['candidate_level']}", "PASS" if len(education_only["rounds"]) == 1 and education_only["rounds"][0]["candidate_scope"] == "Education" else "FAIL")
    conflict = plan(
        [{"type": "Work", "name": "Web product", "position": "Frontend Developer", "jobDescription": "Built React user interfaces."}],
        "AI Engineer",
        education=ai_education,
    )
    scopes = [round_["candidate_scope"] for round_ in conflict["rounds"]]
    record("EDU-002", "Profile→Planner", "Education conflicts with work direction", "Conflict remains visible to planning", f"candidate_role={conflict['candidate_role']}; scopes={scopes}", "PASS" if conflict["candidate_role"] == "Web Developer" and "Education" in scopes and "Work" in scopes else "FAIL")
    education_turn = {
        "question": question("How did your academic project use Python?", "Academic project"),
        "answer": "I used Python in the academic project.",
        "timestamp": "2026-08-24T10:00:00+07:00",
    }
    education_llm = StubLLM({
        "assessments": [{"turn_index": 0, "raw_score": 8, "rationale": "Grounded academic-project answer.", "evidence": [{"timestamp": education_turn["timestamp"], "quote": education_turn["answer"]}]}],
        "solutions_summary": "Academic evidence is available.",
        "overall_assessment": "Assessment is based on the answered rubric.",
        "recommendations": "Continue practicing.",
    })
    generate_report(
        education_llm,
        "AI Engineer",
        "Junior",
        [education_turn],
        candidate_context={"education": ai_education, "workExperience": []},
    )
    education_prompt = education_llm.calls[0]["user"]
    record("EDU-003", "Profile→Report", "Education without GPA", "Education reaches report context without invented GPA", "education visible" if "FPT University" in education_prompt and "GPA" not in education_prompt else "education missing or GPA invented", "PASS" if "FPT University" in education_prompt and "GPA" not in education_prompt else "FAIL")

    # G. Null/type drift.
    null_position = [{"type": "Project", "name": "API", "position": None, "jobDescription": "Built Python endpoints."}]
    p = plan(null_position, "Backend Developer")
    record("NULL-001", "Planner", "Null position", "Use other evidence without crash", f"rounds={len(p['rounds'])}", "PASS" if p["rounds"] else "FAIL")
    null_company = [{"type": "Work", "name": None, "position": "Backend Developer", "jobDescription": "Built Python endpoints."}]
    p = plan(null_company, "Backend Developer")
    record("NULL-002", "Planner", "Null company/name", "Use title/description without crash", f"rounds={len(p['rounds'])}", "PASS" if p["rounds"] else "FAIL")
    empty_desc = [{"type": "Work", "name": "Company", "position": "Developer", "jobDescription": ""}]
    p = plan(empty_desc, "Software Engineer")
    record("NULL-003", "Planner", "Empty description with valid title", "Bounded title-only round and no fabricated detail", f"rounds={len(p['rounds'])}; knowledge={len(p['rounds'][0]['knowledge'])}", "PASS" if p["rounds"] and not p["rounds"][0]["knowledge"] else "FAIL")
    drift = [{"type": "Work", "name": "Company", "position": "Engineer", "jobDescription": "Built Python services.", "years": "three"}]
    p = plan(drift, "Backend Developer", "Senior")
    record("NULL-004", "Planner", "Years as string plus Unicode mismatch", "No crash and no numeric seniority invention", p["rounds"][0]["level"], "PASS" if p["rounds"][0]["level"] == "Junior" else "FAIL")

    # I. QGen semantic challenge: valid-schema, semantically invalid outputs must be rejected.
    qgen_cases = [
        ("QGEN-S001", {"type": "Project", "name": "Student app", "position": "Student", "jobDescription": "Built a classroom React app."}, "Bạn đã lãnh đạo hệ thống dữ liệu senior ở production như thế nào?", "Seniority and role leap"),
        ("QGEN-S002", {"type": "Project", "name": "Personal cache demo", "position": "", "jobDescription": "Built a local cache demo."}, "Bạn đã vận hành cache production cho công ty như thế nào?", "Personal project→production"),
        ("QGEN-S003", {"type": "Project", "name": "API", "position": "Backend Developer", "jobDescription": "Built a Python API."}, "Bạn đã dùng kỹ năng chỉ còn trong JD như thế nào?", "Removed CV skill retained via JD"),
        ("QGEN-S004", {"type": "Project", "name": "API", "position": "Backend Developer", "jobDescription": "Built a Python API."}, "Bạn đã dùng công nghệ chỉ có trong knowledge base như thế nào?", "Knowledge-only technology"),
        ("QGEN-S005", {"type": "Project", "name": "First app", "position": "Student", "jobDescription": "Learned basic API routing."}, "Hãy chứng minh chiến lược consensus phân tán đa vùng của bạn.", "Complexity above evidence"),
        ("QGEN-S006", {"type": "Project", "name": "UI", "position": "Frontend Developer", "jobDescription": "Built React screens."}, "Bạn đã tối ưu data warehouse backend của mình như thế nào?", "Role mismatch"),
        ("QGEN-S007", {"type": "Project", "name": "Prototype", "position": "", "jobDescription": "Created a local prototype."}, "Bạn đã deploy prototype này ở production cho bao nhiêu người dùng?", "Prototype→deployed"),
        ("QGEN-S008", {"type": "Project", "name": "Experiment", "position": "", "jobDescription": "Explored an idea."}, "Hãy mô tả metric và kiến trúc cụ thể mà bạn đã triển khai.", "Vague evidence→specific assumptions"),
    ]
    for test_id, project, text, mutation in qgen_cases:
        accepted = accepted_bad_question(project, text)
        record(test_id, "QGen", mutation, "Semantically unsupported final question is rejected", f"accepted={accepted}", "FAIL" if accepted else "PASS", "QGEN_GROUNDING_FAILURE", "HIGH", "QGen acceptance")

    # J. Evaluator semantic challenge.
    rubric_points = question("scope")["rubric"]["critical_points"]
    def unsupported_case(test_id: str, question_text: str, topic: str, answer: str, context: dict[str, Any], expected_not_assessed: bool) -> None:
        q = question(question_text, topic)
        r = eval_result(q, answer, context, score=2, missing=rubric_points)
        ok = (r["status"] == "NOT_ASSESSED") == expected_not_assessed
        record(test_id, "Evaluator", topic, "Unsupported premise denial is not a technical failure" if expected_not_assessed else "Grounded denial remains assessable", f"status={r['status']}; score={r['score']}", "PASS" if ok else "FAIL", "UNSUPPORTED_ASSUMPTION" if not ok else "", "HIGH" if not ok else "", "Evaluator grounding" if not ok else "")

    unsupported_case("EVAL-S001", "How did you apply this in professional employment?", "Professional employment", "This was a personal project, not work experience; I did not do it for an employer.", {"type": "Project", "name": "Personal app", "jobDescription": "Built an app."}, True)
    unsupported_case("EVAL-S002", "How did you lead this team?", "Team leadership", "I did not lead a team; I worked alone.", {"type": "Project", "name": "Solo app", "jobDescription": "Individual project."}, True)
    unsupported_case("EVAL-S003", "How did you use your three years of production experience?", "Three years production", "I do not have three years of production experience.", {"type": "Project", "name": "Course app", "jobDescription": "Student project."}, True)
    unsupported_case("EVAL-S004", "How did you operate this cache in production?", "Cache", "I used cache only in a personal project, not in production.", {"type": "Project", "name": "Cache demo", "jobDescription": "Built a cache prototype."}, True)
    unsupported_case("EVAL-S005", "How did you implement and optimize this system design in production?", "System design", "I am only familiar with the concept; I did not build it.", {"skills": ["Familiar with system design"], "jobDescription": "Read about design patterns."}, True)
    unsupported_case("EVAL-S006", "How did you optimize this legacy skill in your previous work?", "Legacy skill", "That CV entry is outdated; I no longer claim this experience.", {"skills": ["Python"], "jobDescription": "Built the current Python service."}, True)
    q = question("Explain safe retry semantics", "Safe retries")
    answer = "Client dùng cùng mã yêu cầu; dịch vụ trả kết quả đã lưu nên không tạo tác dụng phụ lần hai."
    r = eval_result(q, answer, {"jobDescription": "Built retry handling."}, score=2, matched=q["rubric"]["critical_points"])
    record("EVAL-S007", "Evaluator", "Vietnamese/English mixed technical answer", "Semantic full coverage is strong", f"raw={r['raw_llm_score']}; final={r['score']}", "PASS" if r["score"] >= 8 else "FAIL")
    answer = "A stable id returns the saved result and prevents duplicate effects."
    r = eval_result(q, answer, {"jobDescription": "Built retry handling."}, score=8, matched=q["rubric"]["critical_points"])
    record("EVAL-S008", "Evaluator", "Concise correct answer", "Concise full evidence remains strong", f"score={r['score']}", "PASS" if r["score"] >= 8 else "FAIL")
    answer = "Rollback commits all partial writes after failure."
    r = eval_result(q, answer, {"jobDescription": "Built retry handling."}, score=2, missing=q["rubric"]["critical_points"], errors=["Mechanism is technically wrong"])
    record("EVAL-S009", "Evaluator", "Answer contradicts rubric", "Technically wrong answer remains low", f"score={r['score']}", "PASS" if r["score"] <= 3 else "FAIL")
    answer = "A stable id is reused, but I did not persist the prior result."
    r = eval_result(q, answer, {"topic": "Safe retries", "jobDescription": "Built retry handling."}, score=5, matched=[q["rubric"]["critical_points"][0]], missing=[q["rubric"]["critical_points"][1]])
    record("EVAL-S010", "Evaluator", "Partial answer with one missing point", "Partial score and focused follow-up remain possible", f"score={r['score']}; follow_up={r['should_follow_up']}", "PASS" if r["score"] == 5 and r["should_follow_up"] else "FAIL")

    # K. Report semantic consistency and hallucination resistance.
    timestamp = "2026-08-24T10:00:00+07:00"
    answer = "I built a personal prototype."
    project_context = {"type": "Project", "name": "Personal prototype", "jobDescription": "Built a personal prototype."}
    project_question = question("Describe the prototype"); project_question["project_context"] = project_context
    turn = {"question": project_question, "answer": answer, "timestamp": timestamp}
    assessment = {"turn_index": 0, "raw_score": 6, "rationale": "Five years of professional production leadership.", "evidence": [{"timestamp": timestamp, "quote": answer}]}
    rep = report_result([turn], [assessment], "Professional expert.")
    retained = "professional" in rep["assessments"][0]["rationale"].casefold()
    record("REPORT-S001", "Reporter", "Work history removed", "Narrative must not restore professional work", rep["assessments"][0]["rationale"], "FAIL" if retained else "PASS", "REPORT_HALLUCINATION", "HIGH", "Report rationale")
    unknown_context = {"type": "Work", "name": "API", "position": "Developer", "jobDescription": "Built APIs; dates are not supplied."}
    unknown_question = question("How did you handle API failures?", "API"); unknown_question["project_context"] = unknown_context
    unknown_turn = {"question": unknown_question, "answer": "I used rollback for failed writes.", "timestamp": timestamp}
    years_assessment = {"turn_index": 0, "raw_score": 6, "rationale": "The candidate has five years of API experience.", "evidence": [{"timestamp": timestamp, "quote": unknown_turn["answer"]}]}
    rep_years = report_result([unknown_turn], [years_assessment], "Five years.")
    record("REPORT-S002", "Reporter", "Years removed", "Narrative must not restore numeric tenure", rep_years["assessments"][0]["rationale"], "FAIL" if "five years" in rep_years["assessments"][0]["rationale"].casefold() else "PASS", "REPORT_HALLUCINATION", "HIGH", "Report rationale")
    deployment_assessment = copy.deepcopy(assessment); deployment_assessment["rationale"] = "The candidate deployed and operated this system in production."
    rep2 = report_result([turn], [deployment_assessment], "Production deployment.")
    record("REPORT-S003", "Reporter", "Prototype project", "Prototype is not promoted to production deployment", rep2["assessments"][0]["rationale"], "FAIL" if "deployed and operated" in rep2["assessments"][0]["rationale"].casefold() else "PASS", "REPORT_HALLUCINATION", "HIGH", "Report rationale")
    low_assessment = copy.deepcopy(assessment); low_assessment["raw_score"] = 2; low_assessment["rationale"] = "Weak evidence."
    rep3 = report_result([turn], [low_assessment], "Strong Hire; perfect evidence.")
    record("REPORT-S004", "Reporter", "Low evaluation with inflated model conclusion", "Validated narrative follows score", rep3["overall_assessment"], "PASS" if "did not meet" in rep3["overall_assessment"].casefold() else "FAIL")
    stale_answer = "That was old CV evidence; I no longer claim Java experience."
    stale_question = question("How did you optimize Java in production?", "Java")
    stale_turn = {
        "question": stale_question,
        "answer": stale_answer,
        "timestamp": timestamp,
        "evaluation": {
            "status": "NOT_ASSESSED", "final_score": 0, "evidence_quote": "",
            "justification": "The stale premise was corrected.",
        },
    }
    stale_assessment = {"turn_index": 0, "raw_score": 0, "rationale": "Java is a major candidate weakness.", "evidence": [{"timestamp": timestamp, "quote": stale_answer}]}
    rep4 = report_result([stale_turn], [stale_assessment], "Java weakness.", candidate_context=[{"type": "Project", "name": "Current API", "jobDescription": "Built the current Python API."}])
    record("REPORT-S005", "Reporter", "Removed skill", "Report does not restore a stale removed skill as a weakness", rep4["assessments"][0]["rationale"], "FAIL" if "java is a major candidate weakness" in rep4["assessments"][0]["rationale"].casefold() else "PASS", "REPORT_HALLUCINATION", "HIGH", "Report rationale")

    # L. State and stale profile propagation (contract-level calls).
    v1 = [{"type": "Project", "name": "Old Java service", "position": "Developer", "jobDescription": "Built a Java service."}]
    v2 = [{"type": "Project", "name": "New Python service", "position": "Developer", "jobDescription": "Built a Python service."}]
    p2 = plan(v2, "Backend Developer")
    record("STATE-S001", "Planner", "Resume V1→V2", "V2 plan excludes V1 evidence", json.dumps(p2["rounds"], ensure_ascii=False), "PASS" if "Java" not in json.dumps(p2, ensure_ascii=False) else "FAIL")
    edited = {"type": "Project", "name": "Edited", "position": "Developer", "jobDescription": "Built a Go service."}
    edited_llm = StubLLM(question("Bạn giải thích Go service này như thế nào?", "Go"))
    generate_question(edited_llm, edited, "Backend Developer", "Junior", [])
    edited_prompt = edited_llm.calls[0]["user"]
    record("STATE-S002", "QGen", "Edit experience in same logical session", "New question prompt consumes edited evidence", "Go present" if "Go service" in edited_prompt else "Go absent", "PASS" if "Go service" in edited_prompt else "FAIL")
    removed_skill_prompt_llm = StubLLM(question("Bạn giải thích Python service này như thế nào?", "Python"))
    generate_question(removed_skill_prompt_llm, v2[0], "Backend Developer", "Junior", [])
    prompt_text = removed_skill_prompt_llm.calls[0]["user"]
    record("STATE-S003", "QGen", "Delete old Java skill/context", "New prompt excludes old skill", "Java absent" if "Java" not in prompt_text else "Java present", "PASS" if "Java" not in prompt_text else "FAIL", "STALE_CONTEXT_REUSE" if "Java" in prompt_text else "", "CRITICAL" if "Java" in prompt_text else "", "QGen prompt" if "Java" in prompt_text else "")
    one_project = plan([v2[0]], "Backend Developer")
    record("STATE-S004", "Planner", "Remove one project", "Removed project is absent from new rounds", json.dumps(one_project["rounds"], ensure_ascii=False), "PASS" if "Old Java" not in json.dumps(one_project, ensure_ascii=False) else "FAIL")
    state_client_id = uuid.uuid4()
    state_resume_id = uuid.uuid4()

    class StateDatabase:
        def get(self, model, key):
            if model is Resume and key == state_resume_id:
                return SimpleNamespace(
                    id=state_resume_id,
                    client_id=state_client_id,
                    profile={"workExperience": v2},
                )
            return None

    @contextmanager
    def state_database_session():
        yield StateDatabase()

    with patch("fipilot.persistence.database_session", state_database_session):
        state_context = resolve_interview_context(
            session_id="state-s005",
            client_id=state_client_id,
            resume_id=state_resume_id,
            role="Backend Developer",
            level="Junior",
            custom_description="",
            work_experience=v1,
        )
    state_text = json.dumps(state_context["work_experience"], ensure_ascii=False)
    state_passed = "Python" in state_text and "Java" not in state_text
    record(
        "STATE-S005",
        "API/state contract",
        "Start new session after V2 while client submits V1 evidence",
        "Backend uses the owned persisted V2 profile",
        "authoritative V2 used" if state_passed else state_text,
        "PASS" if state_passed else "FAIL",
        "" if state_passed else "STALE_STATE",
        "" if state_passed else "CRITICAL",
        "" if state_passed else "API request mapping",
    )

    # M. Inference boundary outputs: schema-valid ownership/scope leaps are accepted.
    boundaries = [
        ("INFER-001", "Assisted with X", "Bạn đã tự thiết kế toàn bộ X như thế nào?", "Ownership"),
        ("INFER-002", "Familiar with X", "Bạn đã triển khai X ở production như thế nào?", "Proficiency"),
        ("INFER-003", "Learned X", "Bạn đã vận hành X cho khách hàng như thế nào?", "Real usage"),
        ("INFER-004", "Prototype using X", "Hệ thống X production của bạn phục vụ bao nhiêu người?", "Production scope"),
        ("INFER-005", "Contributed to X", "Bạn đã một mình kiến trúc toàn bộ X như thế nào?", "Ownership"),
        ("INFER-006", "Team project", "Bạn đã cá nhân thực hiện toàn bộ team project như thế nào?", "Individual attribution"),
    ]
    for test_id, phrase, output, boundary in boundaries:
        project = {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": phrase}
        accepted = accepted_bad_question(project, output)
        record(test_id, "QGen", phrase, f"Respect {boundary.lower()} boundary", f"unsupported leap accepted={accepted}", "FAIL" if accepted else "PASS", "OVER_INFERENCE", "HIGH", "QGen acceptance")

    summary = Counter(item["status"] for item in results)
    payload = {
        "baseline": {
            "profile_keys": sorted(baseline),
            "role": base_role,
            "level": "Intern",
            "skills": len(baseline.get("skills") or []),
            "work_items": len(work),
            "work_types": Counter(item.get("type") for item in work),
            "planner_rounds": len(plan(work, base_role)["rounds"]),
        },
        "summary": dict(summary),
        "results": results,
    }
    RESULTS.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=dict), encoding="utf-8")
    print(json.dumps({"summary": dict(summary), "designed": len(results), "output": str(RESULTS)}, ensure_ascii=False))


def run_live() -> None:
    from fipilot.model.llm_client import LLMClient

    baseline = load_baseline()
    work = baseline["workExperience"]
    projects = [item for item in work if item.get("type") == "Project"]
    llm = LLMClient()
    live: list[dict[str, Any]] = []

    def qgen_case(test_id: str, project: dict[str, Any], role: str, level: str, hits: list[dict[str, Any]], forbidden: list[str]) -> None:
        try:
            result = generate_question(llm, project, role, level, hits)
            text = result["question"]
            normalized = text.casefold()
            found = [term for term in forbidden if term.casefold() in normalized]
            live.append({"test_id": test_id, "status": "PASS" if not found else "FAIL", "question": text, "forbidden_found": found})
        except Exception as error:
            live.append({"test_id": test_id, "status": "BLOCKED", "error": f"{type(error).__name__}: {error}"})

    # Exactly four QGen calls and one Evaluator call.
    qgen_case("LIVE-SEM-01", projects[0], "AI Engineer", "Intern", [], ["công ty", "employer", "internship", "thực tập"])
    qgen_case("LIVE-SEM-02", projects[1], "AI Engineer", "Intern", [], ["năm kinh nghiệm", "years of experience", "senior"])
    qgen_case(
        "LIVE-SEM-03",
        {"type": "Project", "name": "Small API", "position": "Student Developer", "jobDescription": "Built a Python HTTP API with local tests."},
        "Backend Developer",
        "Junior",
        [{"source": "TargetJD.md", "content": "Operate an event-streaming message broker and consumer groups.", "score": 0.99}],
        ["event-stream", "message broker", "consumer group", "streaming"],
    )
    try:
        q = question("How did you lead this team in production?", "Team leadership")
        answer = "I did not lead a team; this was an individual prototype, not production work."
        result = evaluate_answer(
            llm,
            q,
            answer,
            candidate_context={"type": "Project", "name": "Solo prototype", "jobDescription": "Built an individual local prototype."},
        )
        live.append({"test_id": "LIVE-SEM-04", "status": "PASS" if result["status"] == "NOT_ASSESSED" else "FAIL", "answer_status": result["status"], "raw_score": result["raw_llm_score"], "final_score": result["score"]})
    except Exception as error:
        live.append({"test_id": "LIVE-SEM-04", "status": "BLOCKED", "error": f"{type(error).__name__}: {error}"})
    qgen_case(
        "LIVE-SEM-05",
        {"type": "Project", "name": "Current Python service", "position": "Developer", "jobDescription": "Built a Python service with SQL transactions and unit tests."},
        "Backend Developer",
        "Junior",
        [],
        ["java", "kafka", "old service", "legacy"],
    )

    output = ROOT / "evaluation" / "agent_robustness" / "semantic_edge_live_results.json"
    output.write_text(json.dumps({"results": live}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"live": Counter(item["status"] for item in live), "results": live, "output": str(output)}))


def run_qgen_targets() -> None:
    cases = [
        (
            "SKILL-003",
            {"type": "Project", "name": "Simple API", "position": "Backend Developer", "jobDescription": "Built a small Python API."},
            "Bạn đã vận hành công nghệ chỉ có trong JD ở production như thế nào?",
            [{"source": "JD.md", "content": "JD-only event platform", "score": 1.0}],
        ),
        (
            "PROJ-003",
            {"type": "Project", "name": "Business dashboard", "position": "", "jobDescription": "Displayed business records and filters."},
            "Bạn đã đạt 99.9% accuracy trong dự án này như thế nào?",
            [],
        ),
        ("QGEN-S001", {"type": "Project", "name": "Student app", "position": "Student", "jobDescription": "Built a classroom React app."}, "Bạn đã lãnh đạo hệ thống dữ liệu senior ở production như thế nào?", []),
        ("QGEN-S002", {"type": "Project", "name": "Personal cache demo", "position": "", "jobDescription": "Built a local cache demo."}, "Bạn đã vận hành cache production cho công ty như thế nào?", []),
        ("QGEN-S003", {"type": "Project", "name": "API", "position": "Backend Developer", "jobDescription": "Built a Python API."}, "Bạn đã dùng kỹ năng chỉ còn trong JD như thế nào?", []),
        ("QGEN-S004", {"type": "Project", "name": "API", "position": "Backend Developer", "jobDescription": "Built a Python API."}, "Bạn đã dùng công nghệ chỉ có trong knowledge base như thế nào?", []),
        ("QGEN-S005", {"type": "Project", "name": "First app", "position": "Student", "jobDescription": "Learned basic API routing."}, "Hãy chứng minh chiến lược consensus phân tán đa vùng của bạn.", []),
        ("QGEN-S006", {"type": "Project", "name": "UI", "position": "Frontend Developer", "jobDescription": "Built React screens."}, "Bạn đã tối ưu data warehouse backend của mình như thế nào?", []),
        ("QGEN-S007", {"type": "Project", "name": "Prototype", "position": "", "jobDescription": "Created a local prototype."}, "Bạn đã deploy prototype này ở production cho bao nhiêu người dùng?", []),
        ("QGEN-S008", {"type": "Project", "name": "Experiment", "position": "", "jobDescription": "Explored an idea."}, "Hãy mô tả metric và kiến trúc cụ thể mà bạn đã triển khai.", []),
        ("INFER-001", {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": "Assisted with X"}, "Bạn đã tự thiết kế toàn bộ X như thế nào?", []),
        ("INFER-002", {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": "Familiar with X"}, "Bạn đã triển khai X ở production như thế nào?", []),
        ("INFER-003", {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": "Learned X"}, "Bạn đã vận hành X cho khách hàng như thế nào?", []),
        ("INFER-004", {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": "Prototype using X"}, "Hệ thống X production của bạn phục vụ bao nhiêu người?", []),
        ("INFER-005", {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": "Contributed to X"}, "Bạn đã một mình kiến trúc toàn bộ X như thế nào?", []),
        ("INFER-006", {"type": "Project", "name": "Boundary case", "position": "", "jobDescription": "Team project"}, "Bạn đã cá nhân thực hiện toàn bộ team project như thế nào?", []),
    ]
    targeted = []
    for test_id, project, text_value, hits in cases:
        accepted = accepted_bad_question(project, text_value, hits=hits)
        targeted.append(
            {
                "test_id": test_id,
                "status": "FAIL" if accepted else "PASS",
                "unsupported_question_accepted": accepted,
            }
        )
    output = ROOT / "evaluation" / "agent_robustness" / "semantic_qgen_target_results.json"
    output.write_text(json.dumps({"results": targeted}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"summary": Counter(item["status"] for item in targeted), "results": targeted}))


def run_eval_claim_targets() -> None:
    rubric_points = question("scope")["rubric"]["critical_points"]
    cases = [
        (
            "EVAL-S004",
            question("How did you operate this cache in production?", "Cache"),
            "I used cache only in a personal project, not in production.",
            {"type": "Project", "name": "Cache demo", "jobDescription": "Built a cache prototype."},
        ),
        (
            "EVAL-S005",
            question("How did you implement and optimize this system design in production?", "System design"),
            "I am only familiar with the concept; I did not build it.",
            {"skills": ["Familiar with system design"], "jobDescription": "Read about design patterns."},
        ),
        (
            "EVAL-S006",
            question("How did you optimize this legacy skill in your previous work?", "Legacy skill"),
            "That CV entry is outdated; I no longer claim this experience.",
            {"skills": ["Python"], "jobDescription": "Built the current Python service."},
        ),
    ]
    targeted = []
    for test_id, q, answer, context in cases:
        result = eval_result(q, answer, context, score=2, missing=rubric_points)
        targeted.append(
            {
                "test_id": test_id,
                "status": "PASS" if result["status"] == "NOT_ASSESSED" else "FAIL",
                "answer_status": result["status"],
                "raw_score": result["raw_llm_score"],
                "final_score": result["score"],
            }
        )
    output = ROOT / "evaluation" / "agent_robustness" / "semantic_eval_target_results.json"
    output.write_text(json.dumps({"results": targeted}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"summary": Counter(item["status"] for item in targeted), "results": targeted}))


def run_report_claim_targets() -> None:
    timestamp = "2026-08-24T10:00:00+07:00"
    cases = []

    project_context = {"type": "Project", "name": "Course API", "jobDescription": "Built a university project."}
    project_q = question("Describe the course API", "API"); project_q["project_context"] = project_context
    project_answer = "I separated routing from persistence in the university project."
    project_assessment = {"turn_index": 0, "raw_score": 8, "rationale": "Strong professional industry experience.", "evidence": [{"timestamp": timestamp, "quote": project_answer}]}
    project_report = report_result([{"question": project_q, "answer": project_answer, "timestamp": timestamp}], [project_assessment], "Professional experience.")
    cases.append({"test_id": "REPORT-S001", "status": "PASS" if "professional industry experience" not in project_report["assessments"][0]["rationale"].casefold() else "FAIL"})

    unknown_context = {"type": "Work", "name": "API", "jobDescription": "Built APIs; dates are unknown."}
    unknown_q = question("How did you handle failures?", "API"); unknown_q["project_context"] = unknown_context
    unknown_answer = "I used rollback for failed writes."
    unknown_assessment = {"turn_index": 0, "raw_score": 8, "rationale": "The candidate has five years of API experience.", "evidence": [{"timestamp": timestamp, "quote": unknown_answer}]}
    unknown_report = report_result([{"question": unknown_q, "answer": unknown_answer, "timestamp": timestamp}], [unknown_assessment], "Five years.")
    cases.append({"test_id": "REPORT-S002", "status": "PASS" if "five years" not in unknown_report["assessments"][0]["rationale"].casefold() else "FAIL"})

    prototype_q = question("How did you evaluate the prototype?", "Search"); prototype_q["project_context"] = {"type": "Project", "name": "Search", "jobDescription": "Built a local prototype."}
    prototype_answer = "I evaluated it on a local test set."
    prototype_assessment = {"turn_index": 0, "raw_score": 8, "rationale": "The candidate deployed and operated it in production.", "evidence": [{"timestamp": timestamp, "quote": prototype_answer}]}
    prototype_report = report_result([{"question": prototype_q, "answer": prototype_answer, "timestamp": timestamp}], [prototype_assessment], "Production deployment.")
    cases.append({"test_id": "REPORT-S003", "status": "PASS" if "deployed and operated" not in prototype_report["assessments"][0]["rationale"].casefold() else "FAIL"})

    stale_answer = "That was old CV evidence; I no longer claim Java experience."
    stale_turn = {
        "question": question("How did you optimize Java in production?", "Java"),
        "answer": stale_answer,
        "timestamp": timestamp,
        "evaluation": {"status": "NOT_ASSESSED", "final_score": 0, "evidence_quote": "", "justification": "Unsupported stale premise."},
    }
    stale_assessment = {"turn_index": 0, "raw_score": 0, "rationale": "Java is a major candidate weakness.", "evidence": [{"timestamp": timestamp, "quote": stale_answer}]}
    stale_report = report_result([stale_turn], [stale_assessment], "Java weakness.", candidate_context=[{"type": "Project", "name": "Current API", "jobDescription": "Built Python API."}])
    cases.append({"test_id": "REPORT-S005", "status": "PASS" if "java is a major candidate weakness" not in stale_report["assessments"][0]["rationale"].casefold() else "FAIL"})

    output = ROOT / "evaluation" / "agent_robustness" / "semantic_report_target_results.json"
    output.write_text(json.dumps({"results": cases}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"summary": Counter(item["status"] for item in cases), "results": cases}))


def run_eval_claim_live() -> None:
    from fipilot.model.llm_client import LLMClient

    class ThreeCallBudgetLLM:
        def __init__(self):
            self.delegate = LLMClient()
            self.calls = 0

        def generate_text(self, system_prompt, user_prompt, **kwargs):
            if self.calls >= 3:
                raise RuntimeError("Live evaluator call budget exhausted")
            self.calls += 1
            return self.delegate.generate_text(system_prompt, user_prompt, **kwargs)

    llm = ThreeCallBudgetLLM()
    cases = [
        (
            "LIVE-EVAL-CLAIM-01",
            question("How did you operate Redis in production?", "Redis"),
            "I only used Redis in a personal prototype; I did not operate it in production.",
            {"type": "Project", "name": "Personal cache", "jobDescription": "Built a local Redis prototype."},
            "NOT_ASSESSED",
        ),
        (
            "LIVE-EVAL-CLAIM-02",
            question("How did you implement and optimize Kafka in production?", "Kafka"),
            "I am familiar with Kafka concepts, but I have not implemented or operated it in production.",
            {"skills": ["Familiar with Kafka"], "jobDescription": "Studied event-streaming concepts."},
            "NOT_ASSESSED",
        ),
        (
            "LIVE-EVAL-CLAIM-03",
            question("How did you keep Redis writes durable in production?", "Redis durability"),
            "I disabled persistence because Redis always writes every value permanently to disk by default.",
            {"type": "Work", "name": "Payments", "jobDescription": "Deployed and operated Redis in production."},
            "NOT_MET",
        ),
    ]
    live_results = []
    for test_id, q, answer, context, expected_status in cases:
        try:
            result = evaluate_answer(llm, q, answer, candidate_context=context)
            live_results.append(
                {
                    "test_id": test_id,
                    "status": "PASS" if result["status"] == expected_status else "FAIL",
                    "expected_status": expected_status,
                    "answer_status": result["status"],
                    "raw_score": result["raw_llm_score"],
                    "final_score": result["score"],
                }
            )
        except Exception as error:
            live_results.append({"test_id": test_id, "status": "BLOCKED", "error": f"{type(error).__name__}: {error}"})
    output = ROOT / "evaluation" / "agent_robustness" / "semantic_eval_claim_live_results.json"
    output.write_text(
        json.dumps({"provider_calls": llm.calls, "results": live_results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"provider_calls": llm.calls, "summary": Counter(item["status"] for item in live_results), "results": live_results}))


def run_qgen_grounding_live() -> None:
    from fipilot.model.llm_client import LLMClient

    class ThreeCallBudgetLLM:
        def __init__(self):
            self.delegate = LLMClient()
            self.calls = 0

        def generate_text(self, system_prompt, user_prompt, **kwargs):
            if self.calls >= 3:
                raise RuntimeError("Live QGen call budget exhausted")
            self.calls += 1
            return self.delegate.generate_text(system_prompt, user_prompt, **kwargs)

    llm = ThreeCallBudgetLLM()
    cases = [
        (
            "LIVE-QSEM-01",
            {"type": "Project", "name": "Personal cache demo", "position": "", "jobDescription": "Built a personal Redis cache demo."},
            "Backend Developer",
            "Junior",
            [],
        ),
        (
            "LIVE-QSEM-02",
            {"type": "Project", "name": "Student API", "position": "Student Developer", "jobDescription": "Built a Python HTTP API with local tests."},
            "Backend Developer",
            "Junior",
            [{"source": "TargetJD.md", "content": "Kubernetes deployment and cluster operations.", "score": 0.9}],
        ),
        (
            "LIVE-QSEM-03",
            {"type": "Project", "name": "Search experiment", "position": "Contributor", "jobDescription": "Contributed to an experimental search prototype with a team."},
            "Software Engineer",
            "Junior",
            [],
        ),
    ]
    live_results = []
    for test_id, project, role, level, hits in cases:
        try:
            result = generate_question(llm, project, role, level, hits)
            live_results.append(
                {"test_id": test_id, "status": "PASS", "question": result["question"]}
            )
        except RuntimeError as error:
            live_results.append({"test_id": test_id, "status": "BLOCKED", "error": str(error)})
        except ValueError as error:
            live_results.append({"test_id": test_id, "status": "FAIL", "error": str(error)})
    output = ROOT / "evaluation" / "agent_robustness" / "semantic_qgen_live_results.json"
    output.write_text(
        json.dumps({"provider_calls": llm.calls, "results": live_results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"provider_calls": llm.calls, "summary": Counter(item["status"] for item in live_results), "results": live_results}))


def run_report_claim_live() -> None:
    from fipilot.interview_engine import _report_claim_violations
    from fipilot.model.llm_client import LLMClient

    class ThreeCallBudgetLLM:
        def __init__(self):
            self.delegate = LLMClient()
            self.calls = 0

        def generate_text(self, system_prompt, user_prompt, **kwargs):
            if self.calls >= 3:
                raise RuntimeError("Live Report call budget exhausted")
            self.calls += 1
            return self.delegate.generate_text(system_prompt, user_prompt, **kwargs)

    timestamp = "2026-08-24T10:00:00+07:00"
    llm = ThreeCallBudgetLLM()

    def evaluated_turn(q, answer, context, *, score, status, justification):
        q["project_context"] = context
        return {
            "question": q,
            "answer": answer,
            "timestamp": timestamp,
            "evaluation": {
                "score": score,
                "validated_score": score,
                "final_score": score,
                "status": status,
                "evidence_quote": "" if status == "NOT_ASSESSED" else answer,
                "justification": justification,
            },
        }

    project_context = {"type": "Project", "name": "University API", "jobDescription": "Built and tested a Python API for a university project."}
    unknown_context = {"type": "Work", "name": "API", "position": "Developer", "jobDescription": "Built API failure handling; dates are not supplied."}
    stale_context = [{"type": "Project", "name": "Current API", "jobDescription": "Built the current Python API."}]
    cases = [
        (
            "LIVE-REPORT-CLAIM-01",
            [evaluated_turn(question("How did you test the university API?", "API testing"), "I used unit and integration tests for the university project.", project_context, score=8, status="MET", justification="Strong grounded project testing evidence.")],
            project_context,
            "Backend Developer",
        ),
        (
            "LIVE-REPORT-CLAIM-02",
            [evaluated_turn(question("How did you handle API failures?", "API failures"), "I used rollback and returned controlled errors.", unknown_context, score=8, status="MET", justification="Strong grounded API failure-handling evidence without a duration claim.")],
            unknown_context,
            "Backend Developer",
        ),
        (
            "LIVE-REPORT-CLAIM-03",
            [evaluated_turn(question("How did you optimize Java in production?", "Java"), "That was old CV evidence; I no longer claim Java experience.", stale_context, score=0, status="NOT_ASSESSED", justification="The unsupported stale premise was corrected.")],
            stale_context,
            "Backend Developer",
        ),
    ]
    live_results = []
    for test_id, turns, context, role in cases:
        try:
            report = generate_report(llm, role, "Junior", turns, candidate_context=context)
            if test_id == "LIVE-REPORT-CLAIM-03":
                valid = (
                    report["assessments"][0]["status"] == "NOT_ASSESSED"
                    and report["assessments"][0]["raw_score"] is None
                    and not report["assessments"][0]["evidence"]
                )
                violations = []
            else:
                assessment = report["assessments"][0]
                evidence_scope = {
                    "session_snapshot": context,
                    "validated_answer_evidence": turns[0]["answer"],
                }
                violations = _report_claim_violations(
                    assessment["rationale"],
                    topic=turns[0]["question"]["topic"],
                    candidate_evidence=evidence_scope,
                    role=role,
                )
                valid = assessment["status"] == "MET" and not violations
            live_results.append(
                {
                    "test_id": test_id,
                    "status": "PASS" if valid else "FAIL",
                    "assessment": report["assessments"][0],
                    "normalized_score": report["normalized_score"],
                    "claim_violations": violations,
                }
            )
        except Exception as error:
            live_results.append({"test_id": test_id, "status": "BLOCKED", "error": f"{type(error).__name__}: {error}"})
    output = ROOT / "evaluation" / "agent_robustness" / "semantic_report_live_results.json"
    output.write_text(json.dumps({"provider_calls": llm.calls, "results": live_results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"provider_calls": llm.calls, "summary": Counter(item["status"] for item in live_results), "results": live_results}, ensure_ascii=False))


if __name__ == "__main__":
    if "--live" in sys.argv:
        run_live()
    elif "--eval-claim-live" in sys.argv:
        run_eval_claim_live()
    elif "--eval-claim-targets" in sys.argv:
        run_eval_claim_targets()
    elif "--report-claim-targets" in sys.argv:
        run_report_claim_targets()
    elif "--qgen-grounding-live" in sys.argv:
        run_qgen_grounding_live()
    elif "--report-claim-live" in sys.argv:
        run_report_claim_live()
    elif "--qgen-targets" in sys.argv:
        run_qgen_targets()
    else:
        run()
