from __future__ import annotations

import unittest

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import crud
from core.dependencies import (
    get_app_settings,
    get_auth_service,
    get_current_user,
    get_interview_orchestrator,
    get_interview_repository,
)
from core.exceptions import AuthenticationError
from core.settings import Settings
from database import Base
from gateway.api.health import router as health_router
from gateway.api.auth import router as auth_router
from gateway.api.interview import router as interview_router
from gateway.api.report import router as report_router
from infrastructure.auth.firebase import FirebaseAuthService
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from services.report_generator.schemas import InterviewReport
from shared.schemas import (
    CandidateProfile,
    CurrentUser,
    InterviewConfig,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)


class MockAuthService:
    def verify_id_token(self, token: str) -> CurrentUser:
        if token != "valid-token":
            raise AuthenticationError("Invalid or expired authentication token.")
        return CurrentUser(
            uid="user-a",
            email="a@example.com",
            email_verified=True,
        )


class AuthDependencyTests(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()

        @self.app.get("/private")
        def private(current_user: CurrentUser = Depends(get_current_user)):
            return current_user

        self.app.include_router(health_router)
        self.app.include_router(auth_router)
        self.app.dependency_overrides[get_app_settings] = lambda: Settings(
            APP_ENV="test", AUTH_ENABLED=True, GOOGLE_CLOUD_PROJECT="test-project"
        )
        self.app.dependency_overrides[get_auth_service] = lambda: MockAuthService()
        self.client = TestClient(self.app)

    def tearDown(self):
        self.app.dependency_overrides.clear()

    def test_missing_token_returns_401(self):
        response = self.client.get("/private")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers["www-authenticate"], "Bearer")

    def test_invalid_token_returns_401(self):
        response = self.client.get(
            "/private", headers={"Authorization": "Bearer invalid-token"}
        )
        self.assertEqual(response.status_code, 401)

    def test_valid_mocked_token_returns_current_user(self):
        response = self.client.get(
            "/private", headers={"Authorization": "Bearer valid-token"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uid"], "user-a")
        self.assertNotIn("id_token", response.json()["claims"])

        me_response = self.client.get(
            "/api/v2/auth/me", headers={"Authorization": "Bearer valid-token"}
        )
        self.assertEqual(me_response.status_code, 200)
        self.assertNotIn("claims", me_response.json())

    def test_health_remains_public(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

    def test_auth_disabled_uses_development_user(self):
        self.app.dependency_overrides[get_app_settings] = lambda: Settings(
            APP_ENV="test", AUTH_ENABLED=False, AUTH_DEV_USER_ID="dev-user"
        )
        response = self.client.get("/private")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["uid"], "dev-user")

    def test_firebase_service_converts_decoded_claims(self):
        service = FirebaseAuthService(
            Settings(APP_ENV="test", GOOGLE_CLOUD_PROJECT="test-project"),
            token_verifier=lambda token: {
                "uid": "firebase-user",
                "email": "user@example.com",
                "name": "Firebase User",
                "picture": "https://example.com/avatar.png",
                "email_verified": True,
                "id_token": "must-not-be-exposed",
            },
        )
        user = service.verify_id_token("mock-token")
        self.assertEqual(user.uid, "firebase-user")
        self.assertTrue(user.email_verified)
        self.assertNotIn("id_token", user.claims)


def state_for(profile: CandidateProfile, *, completed: bool = False) -> InterviewSessionState:
    config = InterviewConfig(language="en", experience_level="junior", question_count=1)
    question = InterviewQuestion(
        question="Explain dependency injection.",
        language="en",
        topic="FastAPI",
        difficulty="medium",
    )
    turn = InterviewTurn(turn_id="turn-1", question=question, topic="FastAPI")
    return InterviewSessionState(
        candidate_profile=profile,
        interview_config=config,
        interview_plan=InterviewPlan(
            rounds=[InterviewRound(round_id="round-1", topic="FastAPI")]
        ),
        current_turn=None if completed else turn,
        completed_turns=[],
        current_question_index=1 if completed else 0,
    )


class UnexpectedOrchestrator:
    async def start_interview(self, candidate_profile, interview_config):
        raise AssertionError("Cross-user candidate must be rejected before orchestration")

    async def submit_answer(self, session_state, answer):
        raise AssertionError("Cross-user session must be rejected before orchestration")


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
        Base.metadata.create_all(bind=engine)
        self.db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        self.repository = SQLiteInterviewRepository(self.db, auth_enabled=True)

        self.profile_a = CandidateProfile(name="Candidate A", skills=["Python"])
        self.profile_b = CandidateProfile(name="Candidate B", skills=["Java"])
        self.candidate_a = self.repository.create_candidate("Candidate A", user_id="user-a")
        self.candidate_b = self.repository.create_candidate("Candidate B", user_id="user-b")
        self.repository.save_candidate_profile(
            self.candidate_a.candidate_id, self.profile_a, user_id="user-a"
        )
        self.repository.save_candidate_profile(
            self.candidate_b.candidate_id, self.profile_b, user_id="user-b"
        )

        self.session_a = self._create_session(self.candidate_a.candidate_id, self.profile_a, "user-a")
        self.session_b = self._create_session(self.candidate_b.candidate_id, self.profile_b, "user-b")
        self.repository.save_interview_report(
            InterviewReport(
                id="report-b",
                session_id=self.session_b.session_id,
                overall_score=7,
                technical_score=7,
                communication_score=7,
                correctness_score=7,
                summary="User B report.",
                hiring_recommendation="consider",
                confidence_score=0.8,
            ),
            user_id="user-b",
        )

        self.app = FastAPI()
        self.app.include_router(interview_router)
        self.app.include_router(report_router)
        self.app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-a")
        self.app.dependency_overrides[get_interview_repository] = lambda: self.repository
        self.app.dependency_overrides[get_interview_orchestrator] = lambda: UnexpectedOrchestrator()
        self.client = TestClient(self.app)

    def tearDown(self):
        self.app.dependency_overrides.clear()
        self.db.close()

    def _create_session(self, candidate_id: str, profile: CandidateProfile, user_id: str):
        session = self.repository.create_session(
            candidate_id, level="junior", language="en", user_id=user_id
        )
        state = state_for(profile)
        self.repository.update_session_state(
            session.session_id,
            "INTERVIEWING",
            state.model_dump(mode="json"),
            status="in_progress",
            user_id=user_id,
        )
        return session

    def test_user_can_access_own_candidate_but_not_another_users_candidate(self):
        own = self.repository.get_candidate(
            self.candidate_a.candidate_id, user_id="user-a"
        )
        other = self.repository.get_candidate(
            self.candidate_b.candidate_id, user_id="user-a"
        )
        self.assertIsNotNone(own)
        self.assertIsNone(other)

    def test_user_can_access_own_session_but_not_another_users_session(self):
        own = self.client.get(f"/api/v2/interview/{self.session_a.session_id}")
        other = self.client.get(f"/api/v2/interview/{self.session_b.session_id}")
        self.assertEqual(own.status_code, 200)
        self.assertEqual(other.status_code, 404)

    def test_user_cannot_submit_answer_to_another_users_session(self):
        response = self.client.post(
            f"/api/v2/interview/{self.session_b.session_id}/answer",
            json={"answer": "Attempted cross-user answer."},
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_read_another_users_report(self):
        response = self.client.get(
            f"/api/v2/interview/{self.session_b.session_id}/report"
        )
        self.assertEqual(response.status_code, 404)

    def test_history_contains_only_current_users_sessions(self):
        response = self.client.get("/api/v2/interviews")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 1)
        self.assertEqual(
            response.json()["items"][0]["session_id"], self.session_a.session_id
        )

    def test_client_user_id_cannot_override_authenticated_uid(self):
        response = self.client.post(
            "/api/v2/interview/start",
            json={
                "candidate_id": self.candidate_b.candidate_id,
                "user_id": "user-b",
                "interview_config": {"language": "en", "experience_level": "junior"},
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_prepare_another_users_candidate(self):
        response = self.client.post(
            "/api/v2/interview/prepare",
            json={
                "candidate_id": self.candidate_b.candidate_id,
                "interview_config": {
                    "language": "en",
                    "experience_level": "junior",
                },
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_legacy_unowned_rows_are_inaccessible_when_auth_enabled(self):
        legacy = crud.create_user(self.db, "Legacy Candidate", user_id=None)
        self.assertIsNone(
            self.repository.get_candidate(str(legacy.id), user_id="user-a")
        )

        local_repository = SQLiteInterviewRepository(
            self.db, auth_enabled=False, dev_user_id="dev-user"
        )
        self.assertEqual(
            local_repository.get_candidate(str(legacy.id)).name,
            "Legacy Candidate",
        )

    def test_schema_upgrade_is_idempotent_for_legacy_database(self):
        legacy_engine = create_engine("sqlite:///:memory:")
        with legacy_engine.begin() as connection:
            connection.execute(
                text("CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR)")
            )
            connection.execute(
                text(
                    "CREATE TABLE sessions (id INTEGER PRIMARY KEY, user_id INTEGER, "
                    "status VARCHAR, state VARCHAR)"
                )
            )
        legacy_db = sessionmaker(bind=legacy_engine)()
        try:
            SQLiteInterviewRepository(legacy_db, auth_enabled=True)
            SQLiteInterviewRepository(legacy_db, auth_enabled=True)
            user_columns = {item["name"] for item in inspect(legacy_engine).get_columns("users")}
            session_columns = {
                item["name"] for item in inspect(legacy_engine).get_columns("sessions")
            }
            self.assertIn("user_id", user_columns)
            self.assertIn("candidate_id", session_columns)
            self.assertIn("user_id", session_columns)
        finally:
            legacy_db.close()


if __name__ == "__main__":
    unittest.main()
