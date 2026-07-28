from __future__ import annotations

import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
from core.dependencies import get_current_user, get_interview_repository
from database import Base
from gateway.main import app
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from shared.schemas import CandidateProfile, CurrentUser


class CandidateProfileApiTests(unittest.TestCase):
    def setUp(self) -> None:
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.repository = SQLiteInterviewRepository(self.db, auth_enabled=True)
        candidate = self.repository.create_candidate("Nguyen An", user_id="user-a")
        self.candidate_id = candidate.candidate_id
        self.repository.save_candidate_profile(
            self.candidate_id,
            CandidateProfile(
                name="Nguyen An",
                years_experience=1.5,
                recent_role="Backend Engineering Intern",
                specialization="Backend systems",
                skills=["Python", "FastAPI"],
                projects=[
                    {
                        "name": "Campus Interview Practice API",
                        "description": "Built interview session APIs for students.",
                        "technologies": ["Python", "FastAPI"],
                    }
                ],
                experiences=[],
                education=[
                    {
                        "institution": "Ho Chi Minh City University of Technology",
                        "degree": "Bachelor of Engineering",
                        "field_of_study": "Computer Science",
                    }
                ],
                confidence=0.82,
            ),
            user_id="user-a",
        )
        foreign_candidate = self.repository.create_candidate(
            "Foreign Candidate",
            user_id="user-b",
        )
        self.foreign_candidate_id = foreign_candidate.candidate_id
        self.repository.save_candidate_profile(
            self.foreign_candidate_id,
            CandidateProfile(name="Foreign Candidate", skills=["Java"]),
            user_id="user-b",
        )
        app.dependency_overrides[get_interview_repository] = lambda: self.repository
        app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-a")
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.db.close()

    def test_owner_can_load_the_persisted_canonical_profile(self) -> None:
        response = self.client.get(
            f"/api/v2/candidates/{self.candidate_id}/profile"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["etag"], '"1"')
        body = response.json()
        self.assertEqual(body["profile"]["candidate_id"], self.candidate_id)
        self.assertEqual(body["profile"]["profile_version"], 1)
        self.assertEqual(body["profile"]["name"], "Nguyen An")
        self.assertEqual(body["profile"]["recent_role"], "Backend Engineering Intern")
        self.assertEqual(body["profile"]["skills"], ["Python", "FastAPI"])
        self.assertNotIn("full_name", body["profile"])
        stored_candidate = self.db.query(models.User).filter(
            models.User.id == int(self.candidate_id)
        ).one()
        self.assertEqual(stored_candidate.profile_version, 1)

    def test_foreign_and_missing_profiles_share_the_same_not_found_contract(self) -> None:
        foreign = self.client.get(
            f"/api/v2/candidates/{self.foreign_candidate_id}/profile"
        )
        missing = self.client.get("/api/v2/candidates/999999/profile")

        self.assertEqual(foreign.status_code, 404)
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(
            foreign.json()["error"],
            {
                "code": "candidate_profile_not_found",
                "message": "Candidate Profile not found.",
                "retryable": False,
                "issues": [],
            },
        )
        self.assertEqual(foreign.json()["error"], missing.json()["error"])

    def test_profile_etag_is_exposed_to_the_authenticated_frontend_origin(self) -> None:
        response = self.client.get(
            f"/api/v2/candidates/{self.candidate_id}/profile",
            headers={"Origin": "http://localhost:5173"},
        )

        self.assertEqual(response.status_code, 200)
        exposed_headers = response.headers.get("access-control-expose-headers", "")
        self.assertIn(
            "etag",
            {header.strip().lower() for header in exposed_headers.split(",")},
        )

    def test_profile_get_returns_backend_authoritative_readiness(self) -> None:
        candidate = self.repository.create_candidate(
            "Candidate",
            user_id="user-a",
        )
        self.repository.save_candidate_profile(
            candidate.candidate_id,
            CandidateProfile(
                name="Candidate",
                skills=[],
                skill_evidence=[],
                projects=[],
                experiences=[],
                education=None,
            ),
            user_id="user-a",
        )

        response = self.client.get(
            f"/api/v2/candidates/{candidate.candidate_id}/profile"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["etag"], '"1"')
        self.assertEqual(
            response.json()["readiness"],
            {
                "is_ready": False,
                "issues": [
                    {
                        "code": "fallback_name",
                        "origin": "interview_readiness",
                        "field_path": "name",
                    },
                    {
                        "code": "missing_skills",
                        "origin": "interview_readiness",
                        "field_path": "skills",
                    },
                    {
                        "code": "missing_interviewable_evidence",
                        "origin": "interview_readiness",
                        "field_path": "skill_evidence",
                    },
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
