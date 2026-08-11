from __future__ import annotations

import copy
import unittest
from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.dependencies import build_interview_repository
from core.settings import Settings
from database import Base
from infrastructure.repositories.firestore import FirestoreRepository
from infrastructure.repositories.sqlite import SQLiteInterviewRepository
from services.report_generator.schemas import InterviewReport
from shared.schemas import (
    CandidateProfile,
    InterviewConfig,
    InterviewPlan,
    InterviewRound,
    InterviewSessionState,
)


class FakeSnapshot:
    def __init__(self, reference, data):
        self.reference = reference
        self.id = reference.id
        self._data = copy.deepcopy(data)
        self.exists = data is not None

    def to_dict(self):
        return copy.deepcopy(self._data) if self.exists else None


class FakeDocumentReference:
    def __init__(self, client, path):
        self.client = client
        self.path = tuple(path)
        self.id = self.path[-1]

    def collection(self, name):
        return FakeCollectionReference(self.client, (*self.path, name))

    def get(self):
        return FakeSnapshot(self, self.client.documents.get(self.path))

    def set(self, data, merge=False):
        if merge and self.path in self.client.documents:
            stored = copy.deepcopy(self.client.documents[self.path])
            stored.update(copy.deepcopy(data))
            self.client.documents[self.path] = stored
        else:
            self.client.documents[self.path] = copy.deepcopy(data)


class FakeQuery:
    def __init__(self, collection, limit):
        self.collection = collection
        self.result_limit = limit

    def stream(self):
        return iter(list(self.collection.stream())[: self.result_limit])


class FakeCollectionReference:
    def __init__(self, client, path):
        self.client = client
        self.path = tuple(path)

    def document(self, document_id=None):
        if document_id is None:
            self.client.counter += 1
            document_id = f"auto-{self.client.counter}"
        return FakeDocumentReference(self.client, (*self.path, document_id))

    def stream(self):
        expected_length = len(self.path) + 1
        snapshots = []
        for path, data in self.client.documents.items():
            if len(path) == expected_length and path[:-1] == self.path:
                snapshots.append(
                    FakeSnapshot(FakeDocumentReference(self.client, path), data)
                )
        return iter(snapshots)

    def limit(self, value):
        return FakeQuery(self, value)


class FakeFirestoreClient:
    def __init__(self):
        self.documents = {}
        self.counter = 0

    def collection(self, name):
        return FakeCollectionReference(self, (name,))


def profile(name="Candidate", candidate_id=None):
    return CandidateProfile(
        candidate_id=candidate_id,
        name=name,
        skills=["Python", "FastAPI"],
    )


def state(candidate_profile, *, completed=False, mode="text"):
    return InterviewSessionState(
        candidate_profile=candidate_profile,
        interview_config=InterviewConfig(
            mode=mode, language="en", experience_level="middle", question_count=2
        ),
        interview_plan=InterviewPlan(
            rounds=[InterviewRound(round_id="round-1", topic="FastAPI")]
        ),
        current_turn=None,
        completed_turns=[],
        current_question_index=1 if completed else 0,
    )


def report(session_id, report_id="report-1", score=8.0):
    return InterviewReport(
        id=report_id,
        session_id=session_id,
        overall_score=score,
        technical_score=score,
        communication_score=score,
        correctness_score=score,
        summary="Evidence-based report.",
        hiring_recommendation="hire",
        confidence_score=0.9,
    )


class FirestoreRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeFirestoreClient()
        self.repository = FirestoreRepository(self.client)

    def test_candidate_save_get_and_cross_user_isolation(self):
        saved = self.repository.save_candidate("user-a", profile("Candidate A"))

        own = self.repository.get_candidate(saved.candidate_id, user_id="user-a")
        owned_profile = self.repository.get_candidate_profile(
            saved.candidate_id,
            user_id="user-a",
        )
        other = self.repository.get_candidate(saved.candidate_id, user_id="user-b")

        self.assertEqual(own.profile.name, "Candidate A")
        self.assertEqual(owned_profile.candidate_id, saved.candidate_id)
        self.assertEqual(owned_profile.profile_version, 1)
        self.assertEqual(
            self.client.documents[
                ("users", "user-a", "candidates", saved.candidate_id)
            ]["profile_version"],
            1,
        )
        self.assertIsNone(other)
        candidate_paths = [path for path in self.client.documents if "candidates" in path]
        self.assertEqual(candidate_paths[0][:2], ("users", "user-a"))

    def test_reusable_artifacts_persist_and_remain_owner_scoped(self):
        candidate = self.repository.save_candidate("user-a", profile("Candidate A"))
        extracted = profile("Extracted Candidate")
        plan = InterviewPlan(
            rounds=[InterviewRound(round_id="round-1", topic="FastAPI")]
        )
        self.repository.save_resume_extraction_artifact(
            "resume-artifact",
            extracted,
            user_id="user-a",
        )
        self.repository.save_interview_blueprint(
            candidate.candidate_id,
            "blueprint-artifact",
            plan,
            user_id="user-a",
        )

        restarted = FirestoreRepository(self.client)

        self.assertEqual(
            restarted.get_resume_extraction_artifact(
                "resume-artifact",
                user_id="user-a",
            ),
            extracted,
        )
        self.assertEqual(
            restarted.get_interview_blueprint(
                candidate.candidate_id,
                "blueprint-artifact",
                user_id="user-a",
            ),
            plan,
        )
        self.assertIsNone(
            restarted.get_resume_extraction_artifact(
                "resume-artifact",
                user_id="user-b",
            )
        )
        self.assertIsNone(
            restarted.get_interview_blueprint(
                candidate.candidate_id,
                "blueprint-artifact",
                user_id="user-b",
            )
        )

    def test_session_save_get_and_cross_user_isolation(self):
        candidate = self.repository.save_candidate("user-a", profile("Candidate A"))
        session_state = state(
            profile("Candidate A", candidate.candidate_id), mode="voice"
        )

        saved = self.repository.save_interview_session(
            "user-a", "session-a", session_state
        )

        self.assertEqual(saved.candidate_id, candidate.candidate_id)
        self.assertEqual(saved.status, "completed")
        self.assertEqual(
            self.client.documents[("users", "user-a", "interviews", "session-a")][
                "mode"
            ],
            "voice",
        )
        self.assertIsNotNone(
            self.repository.get_interview_session("session-a", "user-a")
        )
        self.assertIsNone(
            self.repository.get_interview_session("session-a", "user-b")
        )

    def test_update_session_state_persists_mode_for_gateway_flow(self):
        candidate = self.repository.save_candidate("user-a", profile())
        session = self.repository.create_session(
            candidate.candidate_id, user_id="user-a"
        )
        session_state = state(
            profile(candidate_id=candidate.candidate_id), mode="voice"
        )

        self.repository.update_session_state(
            session.session_id,
            "INTERVIEWING",
            session_state.model_dump(mode="json"),
            user_id="user-a",
        )

        data = self.client.documents[
            ("users", "user-a", "interviews", session.session_id)
        ]
        self.assertEqual(data["mode"], "voice")
        self.assertEqual(data["state_payload"]["interview_config"]["mode"], "voice")

    def test_report_save_get_and_idempotency(self):
        candidate = self.repository.save_candidate("user-a", profile())
        session = self.repository.create_session(
            candidate.candidate_id, user_id="user-a", level="middle", language="en"
        )
        first = self.repository.save_interview_report(
            report(session.session_id), user_id="user-a"
        )
        second = self.repository.save_interview_report(
            report(session.session_id, report_id="report-2", score=2.0),
            user_id="user-a",
        )

        self.assertEqual(first, second)
        self.assertEqual(
            self.repository.get_interview_report(
                session.session_id, user_id="user-a"
            ).overall_score,
            8.0,
        )
        self.assertEqual(
            self.repository.get_session(session.session_id, user_id="user-a").status,
            "report_generated",
        )

    def test_history_filter_pagination_and_newest_first(self):
        candidate_a = self.repository.save_candidate("user-a", profile("A"))
        candidate_b = self.repository.save_candidate("user-a", profile("B"))
        sessions = [
            self.repository.create_session(candidate_a.candidate_id, user_id="user-a"),
            self.repository.create_session(candidate_b.candidate_id, user_id="user-a"),
            self.repository.create_session(candidate_a.candidate_id, user_id="user-a"),
        ]
        base_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
        for index, session in enumerate(sessions):
            self.repository._interview_collection("user-a").document(
                session.session_id
            ).set({"started_at": base_time + timedelta(days=index)}, merge=True)
        self.repository.update_session_state(
            sessions[2].session_id,
            "INTERVIEWING",
            state(profile("A", candidate_a.candidate_id), mode="voice").model_dump(
                mode="json"
            ),
            status="in_progress",
            user_id="user-a",
        )

        filtered = self.repository.list_interview_sessions(
            candidate_a.candidate_id, 10, 0, user_id="user-a"
        )
        first_page = self.repository.list_interview_sessions(
            None, 1, 0, user_id="user-a"
        )
        second_page = self.repository.list_interview_sessions(
            None, 1, 1, user_id="user-a"
        )

        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].session_id, sessions[2].session_id)
        self.assertEqual(filtered[0].mode, "voice")
        self.assertEqual(first_page[0].session_id, sessions[2].session_id)
        self.assertEqual(second_page[0].session_id, sessions[1].session_id)

    def test_legacy_status_serialization(self):
        candidate = self.repository.save_candidate("user-a", profile())
        session = self.repository.create_session(candidate.candidate_id, user_id="user-a")
        reference = self.repository._interview_collection("user-a").document(
            session.session_id
        )
        reference.set({"status": "ENDED"}, merge=True)

        self.assertEqual(
            self.repository.get_session(session.session_id, user_id="user-a").status,
            "completed",
        )


class RepositoryFactoryTests(unittest.TestCase):
    def test_factory_selects_sqlite(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        db = sessionmaker(bind=engine)()
        try:
            selected = build_interview_repository(
                Settings(
                    APP_ENV="test",
                    AUTH_ENABLED=False,
                    GOOGLE_CLOUD_PROJECT="project",
                    REPOSITORY_BACKEND="sqlite",
                ),
                db=db,
            )
            self.assertIsInstance(selected, SQLiteInterviewRepository)
        finally:
            db.close()

    def test_factory_selects_firestore_without_network(self):
        selected = build_interview_repository(
            Settings(
                APP_ENV="test",
                GOOGLE_CLOUD_PROJECT="project",
                REPOSITORY_BACKEND="firestore",
            ),
            firestore_client=FakeFirestoreClient(),
        )
        self.assertIsInstance(selected, FirestoreRepository)

    def test_invalid_backend_setting_fails_clearly(self):
        with self.assertRaises(ValidationError):
            Settings(REPOSITORY_BACKEND="unsupported")


if __name__ == "__main__":
    unittest.main()
