import json
import unittest
import uuid
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import patch

from api.main import (
    InterviewQuestionRequest,
    InterviewReportRequest,
    generate_interview_report,
    generate_interview_questions,
    resolve_interview_context,
)
from fipilot.interview_planner import create_interview_plan
from fipilot.models import InterviewSession, Resume
from fipilot.persistence import save_interview_session


def fake_database_session(*, resume=None, interview=None):
    class FakeDatabase:
        def get(self, model, key):
            if model is Resume and resume is not None and key == resume.id:
                return resume
            if model is InterviewSession and interview is not None and key == interview.id:
                return interview
            return None

        def add(self, _value):
            return None

    @contextmanager
    def session():
        yield FakeDatabase()

    return session


class FakeQuestionLLM:
    def __init__(self):
        self.prompt = ""

    def generate_text(self, _system_prompt, user_prompt, **_kwargs):
        self.prompt = user_prompt
        return json.dumps(
            {
                "company": "Platform API",
                "topic": "Transaction handling",
                "question": "Bạn thiết kế transaction boundary cho API này như thế nào?",
                "rubric": {
                    "evaluation_goal": "Đánh giá transaction handling",
                    "critical_points": ["Boundary", "Rollback"],
                    "met": "Giải thích đúng boundary và rollback.",
                    "partially_met": "Nêu được một phần cơ chế.",
                    "not_met": "Không giải thích được transaction.",
                },
            },
            ensure_ascii=False,
        )


class InterviewRagApiTest(unittest.TestCase):
    def test_report_uses_persisted_session_snapshot_turns_and_evaluations(self):
        client_id = uuid.uuid4()
        persisted_turn = {
            "question": {
                "company": "Historical service",
                "topic": "Java transactions",
                "question": "How did you handle Java transactions?",
                "rubric": {
                    "evaluation_goal": "Assess Java transactions",
                    "critical_points": ["Boundary", "Rollback"],
                    "met": "Correct mechanism.",
                    "partially_met": "Partial mechanism.",
                    "not_met": "Incorrect mechanism.",
                },
            },
            "answer": "I used transaction boundaries and rollback.",
            "timestamp": "2026-08-24T10:00:00+07:00",
            "evaluation": {
                "status": "MET",
                "final_score": 9,
                "evidence_quote": "transaction boundaries and rollback",
                "justification": "Strong grounded Java transaction evidence.",
            },
        }
        historical_snapshot = [
            {
                "type": "Work",
                "name": "Historical service",
                "position": "Java Developer",
                "jobDescription": "Built a Java transaction service.",
            }
        ]
        source = {
            "role": "Backend Developer",
            "level": "Senior",
            "candidate_context": historical_snapshot,
            "turns": [persisted_turn],
        }
        captured = {}

        def capture_report(_llm, role, level, turns, *, candidate_context=None):
            captured.update(
                role=role,
                level=level,
                turns=turns,
                candidate_context=candidate_context,
            )
            return {"normalized_score": 9.0, "score_scale": 10}

        request = InterviewReportRequest(
            client_id=client_id,
            session_id="historical-v1",
            role="Data Engineer",
            level="Junior",
            turns=[
                {
                    "question": {"question": "Stale client question"},
                    "answer": "Stale client answer",
                    "timestamp": "2026-08-24T11:00:00+07:00",
                }
            ],
        )
        with (
            patch("fipilot.persistence.get_interview_report_source", return_value=source),
            patch("fipilot.interview_engine.generate_report", side_effect=capture_report),
            patch("api.main.get_question_llm", return_value=object()),
            patch("api.main.persist"),
        ):
            result = generate_interview_report(request)

        self.assertEqual(result["normalized_score"], 9.0)
        self.assertEqual(captured["role"], "Backend Developer")
        self.assertEqual(captured["level"], "Senior")
        self.assertEqual(captured["turns"], [persisted_turn])
        self.assertEqual(captured["candidate_context"], historical_snapshot)

    def test_state_s005_state_auth_01_resume_id_uses_authoritative_profile_not_stale_payload(self):
        client_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        stale_v1 = [
            {
                "type": "Work",
                "name": "Old Java service",
                "position": "Java Developer",
                "jobDescription": "Built a Java service.",
            }
        ]
        current_v2 = [
            {
                "type": "Project",
                "name": "Current Python service",
                "position": "Student Developer",
                "jobDescription": "Built a Python service.",
            }
        ]
        llm = FakeQuestionLLM()
        captured_work_experience = []

        class FakeDatabase:
            def get(self, model, key):
                if model is Resume and key == resume_id:
                    return SimpleNamespace(
                        id=resume_id,
                        client_id=client_id,
                        profile={"workExperience": current_v2, "skills": ["Python"]},
                    )
                return None

        @contextmanager
        def fake_database_session():
            yield FakeDatabase()

        def capture_plan(work_experience, role, level, custom_description="", **_evidence):
            captured_work_experience.extend(work_experience)
            return {
                "role": role,
                "level": level,
                "coverage_goals": [],
                "rounds": [
                    {
                        "round_id": "round-1",
                        "evidence_index": 0,
                        "role": role,
                        "level": level,
                        "topic": "Current evidence",
                        "difficulty": "medium",
                        "objective": "Validate current evidence.",
                        "reasoning": "Authoritative resume evidence.",
                        "knowledge": [],
                    }
                ],
            }

        request = InterviewQuestionRequest(
            client_id=client_id,
            session_id="state-auth-01",
            resume_id=resume_id,
            role="Backend Developer",
            level="Junior",
            work_experience=stale_v1,
        )

        with (
            patch("fipilot.persistence.database_session", fake_database_session),
            patch("api.main.create_plan", side_effect=capture_plan),
            patch("api.main.get_question_llm", return_value=llm),
            patch("api.main.persist"),
        ):
            generate_interview_questions(request)

        self.assertEqual(captured_work_experience, current_v2)
        self.assertIn("Built a Python service", llm.prompt)
        self.assertNotIn("Java", llm.prompt)

    def test_state_auth_02_v2_without_work_does_not_restore_v1_employment(self):
        client_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        current_project = {
            "type": "Project",
            "name": "Student project",
            "position": "",
            "jobDescription": "Built a Python project for a course.",
        }
        resume = SimpleNamespace(
            id=resume_id,
            client_id=client_id,
            profile={"workExperience": [current_project]},
        )

        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(resume=resume),
        ):
            context = resolve_interview_context(
                session_id="state-auth-02",
                client_id=client_id,
                resume_id=resume_id,
                role="Backend Developer",
                level="Intern",
                custom_description="",
                work_experience=[
                    {
                        "type": "Work",
                        "name": "Old employer",
                        "position": "Java Developer",
                        "jobDescription": "Professional Java work.",
                    }
                ],
            )

        self.assertEqual(context["work_experience"], [current_project])
        self.assertTrue(all(item["type"] == "Project" for item in context["work_experience"]))

    def test_state_auth_03_removed_years_do_not_survive_from_v1_payload(self):
        client_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        current_v2 = [
            {
                "type": "Project",
                "name": "Current project",
                "position": "Developer",
                "jobDescription": "Built a Python utility without employment dates.",
            }
        ]
        resume = SimpleNamespace(
            id=resume_id,
            client_id=client_id,
            profile={"workExperience": current_v2},
        )

        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(resume=resume),
        ):
            context = resolve_interview_context(
                session_id="state-auth-03",
                client_id=client_id,
                resume_id=resume_id,
                role="Backend Developer",
                level="Junior",
                custom_description="",
                work_experience=[
                    {
                        "type": "Work",
                        "name": "Old employer",
                        "position": "Developer",
                        "jobDescription": "3 years building Java services.",
                    }
                ],
            )

        serialized = json.dumps(context["work_experience"])
        self.assertNotIn("3 years", serialized)
        self.assertEqual(context["work_experience"], current_v2)

    def test_state_auth_04_current_resume_can_start_multiple_sessions(self):
        client_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        current_v2 = [
            {
                "type": "Project",
                "name": "Current API",
                "position": "Developer",
                "jobDescription": "Built a Python API.",
            }
        ]
        resume = SimpleNamespace(
            id=resume_id,
            client_id=client_id,
            profile={"workExperience": current_v2},
        )

        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(resume=resume),
        ):
            contexts = [
                resolve_interview_context(
                    session_id=session_id,
                    client_id=client_id,
                    resume_id=resume_id,
                    role="Backend Developer",
                    level="Junior",
                    custom_description="",
                    work_experience=current_v2,
                )
                for session_id in ("state-auth-04-a", "state-auth-04-b")
            ]

        self.assertEqual([item["work_experience"] for item in contexts], [current_v2, current_v2])

    def test_state_auth_05_resume_ownership_keeps_candidates_isolated(self):
        owner_id = uuid.uuid4()
        other_client_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        resume = SimpleNamespace(
            id=resume_id,
            client_id=owner_id,
            profile={
                "workExperience": [
                    {
                        "type": "Project",
                        "name": "Owner-only project",
                        "position": "Developer",
                        "jobDescription": "Private candidate evidence.",
                    }
                ]
            },
        )

        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(resume=resume),
        ):
            with self.assertRaisesRegex(ValueError, "not found for this client"):
                resolve_interview_context(
                    session_id="state-auth-05",
                    client_id=other_client_id,
                    resume_id=resume_id,
                    role="Software Engineer",
                    level="Junior",
                    custom_description="",
                    work_experience=[],
                )

    def test_state_auth_06_projects_only_fresher_v2_remains_interviewable(self):
        project = {
            "type": "Project",
            "name": "University capstone",
            "position": "",
            "jobDescription": "Built a Python scheduling application.",
        }
        plan = create_interview_plan(
            work_experience=[project],
            role="Backend Developer",
            level="Intern",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(len(plan["rounds"]), 1)
        self.assertEqual(plan["rounds"][0]["evidence_index"], 0)
        self.assertEqual(plan["rounds"][0]["level"], "Intern")

    def test_state_auth_07_existing_v1_interview_keeps_immutable_snapshot(self):
        client_id = uuid.uuid4()
        v1_resume_id = uuid.uuid4()
        v2_resume_id = uuid.uuid4()
        v1_snapshot = [
            {
                "type": "Work",
                "name": "Historical employer",
                "position": "Java Developer",
                "jobDescription": "Built a Java service.",
            }
        ]
        v2_evidence = [
            {
                "type": "Project",
                "name": "Current project",
                "position": "Developer",
                "jobDescription": "Built a Python service.",
            }
        ]
        interview = SimpleNamespace(
            id="state-auth-07",
            client_id=client_id,
            resume_id=v1_resume_id,
            role="Backend Developer",
            level="Junior",
            custom_description="",
            work_experience=v1_snapshot,
        )

        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(interview=interview),
        ):
            context = resolve_interview_context(
                session_id=interview.id,
                client_id=client_id,
                resume_id=v2_resume_id,
                role="Backend Developer",
                level="Junior",
                custom_description="",
                work_experience=v2_evidence,
            )
            save_interview_session(
                session_id=interview.id,
                client_id=client_id,
                resume_id=v2_resume_id,
                role="Backend Developer",
                level="Junior",
                custom_description="",
                work_experience=v2_evidence,
            )

        self.assertEqual(context["resume_id"], v1_resume_id)
        self.assertEqual(context["work_experience"], v1_snapshot)
        self.assertEqual(interview.resume_id, v1_resume_id)
        self.assertEqual(interview.work_experience, v1_snapshot)

    def test_first_question_exposes_plan_and_retrieval_trace(self):
        llm = FakeQuestionLLM()
        plan = {
            "role": "Backend Developer",
            "level": "Junior",
            "coverage_goals": ["Validate backend evidence."],
            "rounds": [
                {
                    "round_id": "round-1",
                    "evidence_index": 0,
                    "topic": "Transaction",
                    "difficulty": "medium",
                    "objective": "Validate transaction handling.",
                    "reasoning": "Resume-backed API evidence.",
                    "knowledge": [
                        {
                            "source": "Domains/Backend Developer/Database/Transaction.md",
                            "content": "Transaction boundaries require rollback on failure.",
                            "score": 0.8,
                            "method": "lexical",
                        }
                    ],
                }
            ],
        }
        request = InterviewQuestionRequest(
            role="Backend Developer",
            level="Junior",
            work_experience=[
                {
                    "type": "Work",
                    "name": "Platform API",
                    "position": "Backend Engineer",
                    "jobDescription": "Built FastAPI and PostgreSQL services.",
                }
            ],
        )

        with (
            patch("api.main.create_plan", return_value=plan),
            patch("api.main.get_question_llm", return_value=llm),
            patch("api.main.persist"),
        ):
            result = generate_interview_questions(request)

        question = result["questions"][0]
        self.assertEqual(result["plan"]["rounds"][0]["topic"], "Transaction")
        self.assertNotIn("knowledge", result["plan"]["rounds"][0])
        self.assertEqual(question["round_id"], "round-1")
        self.assertEqual(
            question["retrieval_sources"],
            ["Domains/Backend Developer/Database/Transaction.md"],
        )
        self.assertIn("rollback on failure", llm.prompt)
        self.assertIn("Built FastAPI and PostgreSQL services", llm.prompt)


if __name__ == "__main__":
    unittest.main()
