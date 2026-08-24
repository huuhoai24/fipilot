import json
import tempfile
import unittest
import uuid
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pymupdf

from api.main import resolve_interview_context
from fipilot.interview_planner import create_interview_plan
from fipilot.models import InterviewSession, Resume
from fipilot.persistence import (
    get_interview_report_source,
    get_interview_session_context,
    save_interview_session,
)
from fipilot.resume_extraction import ResumeExtract


class FakeLLM:
    def __init__(self, response):
        self.response = response

    def extract_info(self, **_kwargs):
        return self.response


def write_pdf(path: Path, lines: list[str]) -> None:
    document = pymupdf.open()
    page = document.new_page()
    for index, line in enumerate(lines):
        page.insert_text((72, 72 + index * 24), line)
    document.save(path)
    document.close()


def fake_database_session(*, resume=None, interview=None, created=None):
    class FakeDatabase:
        def get(self, model, key):
            if model is Resume and resume is not None and key == resume.id:
                return resume
            if model is InterviewSession and interview is not None and key == interview.id:
                return interview
            return None

        def add(self, value):
            if created is not None:
                created.append(value)

    @contextmanager
    def session():
        yield FakeDatabase()

    return session


class ProfileEvidencePropagationTest(unittest.TestCase):
    def test_profile_skill_01_and_02_preserve_strong_and_familiarity_evidence(self):
        response = {
            "skills": ["Python", "Event streaming"],
            "skillEvidence": [
                {"skill": "Python", "scope": "strong", "source": "work"},
                {
                    "skill": "Event streaming",
                    "scope": "familiarity",
                    "source": "resume",
                },
            ],
            "workExperience": [
                {
                    "type": "Project",
                    "name": "Candidate project",
                    "position": "Student",
                    "description_refer_index_range": [0, 0],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, ["Candidate project"])
            profile = json.loads(ResumeExtract(FakeLLM(response)).pipeline(path))

        self.assertEqual(
            profile["skillEvidence"],
            [
                {"skill": "Python", "scope": "strong", "source": "work"},
                {
                    "skill": "Event streaming",
                    "scope": "familiarity",
                    "source": "resume",
                },
            ],
        )

    def test_profile_skill_03_and_04_keep_unknown_and_project_scope(self):
        response = {
            "skills": ["Distributed systems", "TypeScript"],
            "skillEvidence": [
                {
                    "skill": "Distributed systems",
                    "scope": "unknown",
                    "source": "resume",
                },
                {"skill": "TypeScript", "scope": "demonstrated", "source": "project"},
            ],
            "workExperience": [
                {
                    "type": "Project",
                    "name": "Portfolio",
                    "position": "Student",
                    "description_refer_index_range": [0, 0],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, ["Portfolio"])
            profile = json.loads(ResumeExtract(FakeLLM(response)).pipeline(path))

        evidence = {item["skill"]: item for item in profile["skillEvidence"]}
        self.assertEqual(evidence["Distributed systems"]["scope"], "unknown")
        self.assertEqual(evidence["TypeScript"]["source"], "project")

    def test_profile_edu_04_preserves_present_fields_without_fabricating_dates(self):
        response = {
            "skills": ["Python"],
            "education": [
                {
                    "institution": "FPT University",
                    "degree": "Bachelor of Engineering",
                    "field_of_study": "Artificial Intelligence",
                }
            ],
            "workExperience": [
                {
                    "type": "Project",
                    "name": "Graduation project",
                    "position": "Student",
                    "description_refer_index_range": [0, 0],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, ["Graduation project"])
            profile = json.loads(ResumeExtract(FakeLLM(response)).pipeline(path))

        self.assertEqual(profile["education"], response["education"])
        self.assertNotIn("start_date", profile["education"][0])
        self.assertNotIn("end_date", profile["education"][0])

    def test_profile_edu_03_does_not_fabricate_absent_education(self):
        response = {
            "skills": ["Python"],
            "workExperience": [
                {
                    "type": "Project",
                    "name": "Portfolio",
                    "position": "Student",
                    "description_refer_index_range": [0, 0],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate.pdf"
            write_pdf(path, ["Portfolio"])
            profile = json.loads(ResumeExtract(FakeLLM(response)).pipeline(path))

        self.assertEqual(profile["education"], [])

    def test_profile_edu_01_education_only_candidate_receives_entry_plan(self):
        plan = create_interview_plan(
            work_experience=[],
            skills=[],
            skill_evidence=[],
            education=[
                {
                    "institution": "FPT University",
                    "degree": "Bachelor of Engineering",
                    "field_of_study": "Artificial Intelligence",
                }
            ],
            role="AI Engineer",
            level="Junior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["candidate_level"], "Entry")
        self.assertEqual(len(plan["rounds"]), 1)
        self.assertEqual(plan["rounds"][0]["candidate_scope"], "Education")

    def test_profile_edu_02_keeps_education_and_work_direction_in_planning(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Work",
                    "name": "Web product",
                    "position": "Frontend Developer",
                    "jobDescription": "Built React user interfaces.",
                }
            ],
            skills=[],
            skill_evidence=[],
            education=[
                {
                    "institution": "FPT University",
                    "degree": "Bachelor of Engineering",
                    "field_of_study": "Artificial Intelligence",
                }
            ],
            role="AI Engineer",
            level="Junior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["candidate_role"], "Web Developer")
        self.assertEqual(
            [round_["candidate_scope"] for round_ in plan["rounds"]],
            ["Work", "Education"],
        )

    def test_year_005_exposes_candidate_and_target_level_conflict(self):
        plan = create_interview_plan(
            work_experience=[
                {
                    "type": "Work",
                    "name": "API",
                    "position": "Developer",
                    "jobDescription": "2 years building Python services.",
                }
            ],
            role="Backend Developer",
            level="Senior",
            retrieve=lambda *_args: [],
        )

        self.assertEqual(plan["candidate_level"], "Entry")
        self.assertEqual(plan["target_level"], "Senior")
        self.assertTrue(plan["level_conflict"])
        self.assertTrue(plan["rounds"][0]["level_conflict"])

    def test_profile_context_and_session_snapshot_preserve_authoritative_evidence(self):
        client_id = uuid.uuid4()
        resume_id = uuid.uuid4()
        profile = {
            "skills": ["Event streaming"],
            "skillEvidence": [
                {
                    "skill": "Event streaming",
                    "scope": "familiarity",
                    "source": "resume",
                }
            ],
            "education": [
                {
                    "institution": "FPT University",
                    "degree": "Bachelor of Engineering",
                    "field_of_study": "Artificial Intelligence",
                }
            ],
            "workExperience": [],
        }
        resume = SimpleNamespace(id=resume_id, client_id=client_id, profile=profile)
        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(resume=resume),
        ):
            context = resolve_interview_context(
                session_id="profile-evidence",
                client_id=client_id,
                resume_id=resume_id,
                role="AI Engineer",
                level="Junior",
                custom_description="",
                work_experience=[],
            )

        self.assertEqual(context["skill_evidence"], profile["skillEvidence"])
        self.assertEqual(context["education"], profile["education"])
        self.assertEqual(context["candidate_profile"], profile)

    def test_session_snapshot_reuses_its_own_profile_evidence(self):
        client_id = uuid.uuid4()
        snapshot = {
            "skills": ["Python"],
            "skillEvidence": [{"skill": "Python", "scope": "strong", "source": "work"}],
            "education": [{"institution": "FPT University", "degree": "BEng"}],
            "workExperience": [],
        }
        interview = SimpleNamespace(
            id="profile-snapshot",
            client_id=client_id,
            resume_id=uuid.uuid4(),
            role="AI Engineer",
            level="Junior",
            custom_description="",
            work_experience=[],
            candidate_profile=snapshot,
        )
        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(interview=interview),
        ):
            context = get_interview_session_context(interview.id, client_id)

        self.assertEqual(context["candidate_profile"], snapshot)
        self.assertEqual(context["skill_evidence"], snapshot["skillEvidence"])
        self.assertEqual(context["education"], snapshot["education"])

    def test_edu_report_01_snapshot_education_reaches_report_context(self):
        client_id = uuid.uuid4()
        work_experience = [
            {
                "type": "Work",
                "name": "Web platform",
                "position": "Frontend Intern",
                "jobDescription": "Built accessible React user interfaces.",
            }
        ]
        snapshot = {
            "skills": ["Python"],
            "skillEvidence": [{"skill": "Python", "scope": "strong", "source": "work"}],
            "education": [
                {
                    "institution": "FPT University",
                    "degree": "Bachelor of Engineering",
                    "field_of_study": "Artificial Intelligence",
                }
            ],
            "workExperience": work_experience,
        }

        class FakeDatabase:
            def get(self, model, key):
                if model is InterviewSession and key == "education-report":
                    return SimpleNamespace(
                        id="education-report",
                        client_id=client_id,
                        role="AI Engineer",
                        level="Junior",
                        work_experience=work_experience,
                        candidate_profile=snapshot,
                    )
                return None

            def scalars(self, _query):
                return SimpleNamespace(all=lambda: [])

        @contextmanager
        def session():
            yield FakeDatabase()

        with patch("fipilot.persistence.database_session", session):
            source = get_interview_report_source("education-report", client_id)

        self.assertEqual(source["candidate_context"]["education"], snapshot["education"])
        self.assertEqual(source["candidate_context"]["workExperience"], work_experience)
        self.assertNotIn("start_date", source["candidate_context"]["education"][0])
        self.assertNotIn("end_date", source["candidate_context"]["education"][0])

    def test_edu_report_02_and_03_legacy_snapshot_stays_without_education(self):
        client_id = uuid.uuid4()
        work_snapshot = [{"type": "Project", "name": "Legacy project", "jobDescription": "Built an API."}]

        class FakeDatabase:
            def get(self, model, key):
                if model is InterviewSession and key == "legacy-report":
                    return SimpleNamespace(
                        id="legacy-report",
                        client_id=client_id,
                        role="Backend Developer",
                        level="Junior",
                        work_experience=work_snapshot,
                        candidate_profile={},
                    )
                return None

            def scalars(self, _query):
                return SimpleNamespace(all=lambda: [])

        @contextmanager
        def session():
            yield FakeDatabase()

        with patch("fipilot.persistence.database_session", session):
            source = get_interview_report_source("legacy-report", client_id)

        self.assertEqual(source["candidate_context"], work_snapshot)

    def test_session_creation_persists_candidate_profile_snapshot(self):
        client_id = uuid.uuid4()
        snapshot = {
            "skills": ["Python"],
            "skillEvidence": [{"skill": "Python", "scope": "strong", "source": "work"}],
            "education": [{"institution": "FPT University", "degree": "BEng"}],
            "workExperience": [],
        }
        created = []
        with patch(
            "fipilot.persistence.database_session",
            fake_database_session(created=created),
        ):
            save_interview_session(
                session_id="persisted-profile-snapshot",
                client_id=client_id,
                resume_id=uuid.uuid4(),
                role="AI Engineer",
                level="Junior",
                custom_description="",
                work_experience=[],
                candidate_profile=snapshot,
            )

        self.assertEqual(created[0].candidate_profile, snapshot)


if __name__ == "__main__":
    unittest.main()
