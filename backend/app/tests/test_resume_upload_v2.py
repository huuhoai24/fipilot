import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from core.dependencies import get_current_user
from app.api.routes.resume import get_document_service, get_resume_agent
from app.repositories import SQLiteInterviewRepository
from app.schemas import CandidateProfile, CurrentUser
from database import Base, get_db
from models import User
from services.profile_scanner.exceptions import NonResumeDocumentError


class MockDocumentService:
    def extract_text(self, file_path: str, filename: str | None = None) -> str:
        return "Tran Thi B\nAI Engineer\nPython FastAPI\nBuilt an AI interview platform."


class MockResumeAgent:
    def __init__(self):
        self.calls = 0

    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        self.calls += 1
        return CandidateProfile(
            name="Tran Thi B",
            skills=["Python", "FastAPI"],
            skill_evidence=[
                {
                    "skill": "Python",
                    "evidence": ["Built an AI interview platform with Python FastAPI."],
                    "source_section": "Projects",
                }
            ],
            specialization="AI Interview",
            confidence_score=0.93,
        )


class MockNonResumeAgent:
    async def extract_profile(self, resume_text: str) -> CandidateProfile:
        raise NonResumeDocumentError


class ResumeUploadV2Tests(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

        def override_get_db():
            yield self.db

        main.app.dependency_overrides[get_db] = override_get_db
        main.app.dependency_overrides[get_document_service] = lambda: MockDocumentService()
        self.resume_agent = MockResumeAgent()
        main.app.dependency_overrides[get_resume_agent] = lambda: self.resume_agent
        main.app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-1")
        self.client = TestClient(main.app)

    def tearDown(self):
        main.app.dependency_overrides.clear()
        self.db.close()

    def test_upload_resume_v2_saves_candidate_profile(self):
        with self.assertLogs("gateway.api.resume", level="INFO") as logs:
            response = self.client.post(
                "/api/v2/resume/upload",
                files={"file": ("resume.pdf", b"%PDF mocked resume content", "application/pdf")},
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["profile"]["name"], "Tran Thi B")
        self.assertEqual(body["profile"]["skill_evidence"][0]["skill"], "Python")
        self.assertEqual(body["confidence_score"], 0.93)

        repository = SQLiteInterviewRepository(self.db)
        saved_profile = repository.get_candidate_profile(
            body["candidate_id"], user_id="user-1"
        )
        saved_resume_text = repository.get_candidate_resume_text(
            body["candidate_id"], user_id="user-1"
        )
        self.assertEqual(saved_profile.name, "Tran Thi B")
        self.assertEqual(saved_profile.skill_evidence[0].skill, "Python")
        self.assertEqual(saved_profile.specialization, "AI Interview")
        self.assertIn("Python FastAPI", saved_resume_text)
        events = {record.event for record in logs.records}
        self.assertTrue(
            {
                "cv.file_parse",
                "cv.profile_extraction",
                "cv.persistence",
                "cv.total",
            }.issubset(events)
        )
        self.assertTrue(all(record.duration_ms >= 0 for record in logs.records))
        self.assertTrue(all(not hasattr(record, "resume_text") for record in logs.records))

    def test_project_report_is_rejected_without_creating_candidate(self):
        main.app.dependency_overrides[get_resume_agent] = lambda: MockNonResumeAgent()

        response = self.client.post(
            "/api/v2/resume/upload",
            files={
                "file": (
                    "AI_Interview_Platform_Capstone_Report.docx",
                    b"PK mocked capstone report content",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "not_a_resume")
        self.assertIn("10 ngành nghề", response.json()["error"]["message"])
        self.assertEqual(self.db.query(User).count(), 0)

    def test_identical_successful_resume_reuses_extraction_for_a_new_candidate(self):
        upload = {
            "files": {
                "file": (
                    "same-resume.pdf",
                    b"%PDF same unique resume content for cache coverage",
                    "application/pdf",
                )
            }
        }

        first = self.client.post("/api/v2/resume/upload", **upload)
        second = self.client.post("/api/v2/resume/upload", **upload)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertNotEqual(second.json()["candidate_id"], first.json()["candidate_id"])
        self.assertEqual(self.resume_agent.calls, 1)
        self.assertEqual(self.db.query(User).count(), 2)

    def test_processed_resume_cache_is_scoped_to_the_authenticated_user(self):
        files = {
            "file": (
                "shared-bytes.pdf",
                b"%PDF same bytes uploaded by two different owners",
                "application/pdf",
            )
        }
        first = self.client.post("/api/v2/resume/upload", files=files)
        main.app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-2")
        second = self.client.post("/api/v2/resume/upload", files=files)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertNotEqual(second.json()["candidate_id"], first.json()["candidate_id"])
        self.assertEqual(self.resume_agent.calls, 2)
        self.assertEqual(self.db.query(User).count(), 2)


if __name__ == "__main__":
    unittest.main()
