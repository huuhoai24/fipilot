from __future__ import annotations

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.dependencies import get_current_user, get_report_service
from database import Base, get_db
from gateway.api.report import router
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from services.report_generator.schemas import InterviewReport
from shared.schemas import CurrentUser


def sample_report(session_id: str) -> InterviewReport:
    return InterviewReport(
        id="report-1",
        session_id=session_id,
        overall_score=8.0,
        technical_score=8.0,
        communication_score=7.5,
        correctness_score=8.5,
        summary="Good evidence.",
        hiring_recommendation="hire",
        confidence_score=0.9,
    )


class MockReportService:
    def __init__(self, report=None):
        self.report = report

    async def generate_for_session(self, session_id, user_id=None):
        return self.report or sample_report(session_id)

    async def get_for_session(self, session_id, user_id=None):
        return self.report


class ReportApiTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.app = FastAPI()
        self.app.include_router(router)

        def override_get_db():
            yield self.db

        self.app.dependency_overrides[get_db] = override_get_db
        self.app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-1")
        self.client = TestClient(self.app)

    def tearDown(self):
        self.app.dependency_overrides.clear()
        self.db.close()

    def test_generate_report_success(self):
        self.app.dependency_overrides[get_report_service] = lambda: MockReportService()

        response = self.client.post("/api/v2/interview/42/report")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["session_id"], "42")
        self.assertEqual(response.json()["report"]["hiring_recommendation"], "hire")

    def test_get_report_404(self):
        self.app.dependency_overrides[get_report_service] = lambda: MockReportService()

        response = self.client.get("/api/v2/interview/42/report")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Interview report not found.")

    def test_history_api_pagination(self):
        repository = SQLiteInterviewRepository(self.db)
        candidate = repository.create_candidate("Candidate", user_id="user-1")
        for _ in range(3):
            repository.create_session(
                candidate.candidate_id,
                level="junior",
                language="vi",
                user_id="user-1",
            )

        response = self.client.get("/api/v2/interviews?limit=1&offset=1")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["total"], 3)
        self.assertEqual(body["limit"], 1)
        self.assertEqual(body["offset"], 1)
        self.assertEqual(len(body["items"]), 1)
        self.assertEqual(body["items"][0]["mode"], "text")


if __name__ == "__main__":
    unittest.main()
