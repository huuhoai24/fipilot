from __future__ import annotations

import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from core.dependencies import (
    get_current_user,
    get_interview_answer_submission_service,
)
from gateway.api.interview import router
from shared.schemas import (
    CandidateProfile,
    CurrentUser,
    InterviewConfig,
    InterviewMode,
    InterviewPlan,
    InterviewQuestion,
    InterviewRound,
    InterviewSessionState,
    InterviewTurn,
)


def voice_session_state(*, mode: str = "voice") -> InterviewSessionState:
    question = InterviewQuestion(
        question="Explain dependency injection.",
        language="en",
        topic="FastAPI",
        difficulty="medium",
    )
    return InterviewSessionState(
        candidate_profile=CandidateProfile(name="Voice Candidate"),
        interview_config=InterviewConfig(
            mode=mode,
            language="en",
            experience_level="junior",
            question_count=2,
        ),
        interview_plan=InterviewPlan(
            rounds=[
                InterviewRound(round_id="round-1", topic="FastAPI"),
                InterviewRound(round_id="round-2", topic="Testing"),
            ]
        ),
        current_turn=InterviewTurn(
            turn_id="turn-1",
            round_id="round-1",
            question=question,
            difficulty="medium",
            topic="FastAPI",
        ),
    )


class StubAnswerService:
    """Captures the expected mode the route resolves for the session."""

    def __init__(self, state_payload: dict | None) -> None:
        self._state_payload = state_payload
        self.seen_expected_mode: InterviewMode | None = None
        captured_payload = state_payload

        class _Repository:
            def get_session(self, session_id: str, *, user_id: str):
                if captured_payload is None:
                    return None
                return SimpleNamespace(state_payload=captured_payload)

        self.repository = _Repository()

    async def submit_answer(
        self,
        session_id: str,
        user_id: str,
        turn_id: str,
        answer: str,
        *,
        expected_mode: InterviewMode,
    ):
        self.seen_expected_mode = expected_mode
        state = voice_session_state()
        return SimpleNamespace(
            state=state,
            started_at=datetime.now(timezone.utc),
            replayed=False,
        )


class AnswerRouteModeTests(unittest.TestCase):
    def _client_with(self, service: StubAnswerService) -> TestClient:
        application = FastAPI()
        application.include_router(router)
        application.dependency_overrides[get_current_user] = lambda: CurrentUser(
            uid="user-1"
        )
        application.dependency_overrides[
            get_interview_answer_submission_service
        ] = lambda: service
        return TestClient(application)

    def test_voice_session_answer_expects_voice_mode(self) -> None:
        state = voice_session_state(mode="voice")
        service = StubAnswerService(state.model_dump(mode="json"))
        client = self._client_with(service)

        response = client.post(
            "/api/v2/interview/session-27/answer",
            json={"turn_id": "turn-1", "answer": "Dependency injection is..."},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(service.seen_expected_mode, InterviewMode.VOICE)

    def test_text_session_answer_still_expects_text_mode(self) -> None:
        state = voice_session_state(mode="text")
        service = StubAnswerService(state.model_dump(mode="json"))
        client = self._client_with(service)

        response = client.post(
            "/api/v2/interview/session-27/answer",
            json={"turn_id": "turn-1", "answer": "Text answer"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(service.seen_expected_mode, InterviewMode.TEXT)

    def test_unreadable_state_falls_back_to_text_expectation(self) -> None:
        service = StubAnswerService({"interview_config": {"mode": "???"}})
        # Sanity: the payload must genuinely fail validation for this fallback.
        with self.assertRaises(ValidationError):
            InterviewSessionState.model_validate(service._state_payload)
        client = self._client_with(service)

        response = client.post(
            "/api/v2/interview/session-27/answer",
            json={"turn_id": "turn-1", "answer": "Answer"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(service.seen_expected_mode, InterviewMode.TEXT)


if __name__ == "__main__":
    unittest.main()
