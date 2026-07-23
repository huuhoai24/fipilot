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


class MockDocumentService:
    def extract_text(self, file_path: str, filename: str | None = None) -> str:
        return "Tran Thi B\nAI Engineer\nPython FastAPI\nBuilt an AI interview platform."


class MockResumeAgent:
    async def extract_profile(self, resume_text: str) -> CandidateProfile:
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
        main.app.dependency_overrides[get_resume_agent] = lambda: MockResumeAgent()
        main.app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-1")
        self.client = TestClient(main.app)

    def tearDown(self):
        main.app.dependency_overrides.clear()
        self.db.close()

    def test_upload_resume_v2_saves_candidate_profile(self):
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


if __name__ == "__main__":
    unittest.main()
