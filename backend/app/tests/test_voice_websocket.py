from __future__ import annotations

import asyncio
import json
import threading
import unittest
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from core.dependencies import (
    get_app_settings,
    get_auth_service,
    get_interview_repository,
    get_question_speech_streamer_factory,
    get_question_streaming_service,
    get_voice_answer_submission_service,
    get_voice_session_manager,
)
from core.exceptions import AuthenticationError
from core.settings import Settings
from gateway.api.voice import router
from infrastructure.repositories.base import InterviewSessionRecord
from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from services.voice_session.audio_pipeline import (
    AudioPipelineFactory,
    VADFrameResult,
    VoiceActivityDetector,
    VoiceActivityDetectorFactory,
)
from services.voice_session.answer_service import VoiceAnswerSubmissionService
from services.voice_session.manager import VoiceSessionManager
from services.voice_session.question_speech import QuestionSpeechStreamerFactory
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


def voice_interview_state(*, active_turn: bool = True) -> InterviewSessionState:
    question = InterviewQuestion(
        question="Explain dependency injection.",
        language="en",
        topic="FastAPI",
        difficulty="medium",
    )
    return InterviewSessionState(
        candidate_profile=CandidateProfile(name="Voice Candidate"),
        interview_config=InterviewConfig(
            mode="voice",
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
        current_turn=(
            InterviewTurn(
                turn_id="turn-1",
                round_id="round-1",
                question=question,
                difficulty="medium",
                topic="FastAPI",
            )
            if active_turn
            else None
        ),
    )


def text_interview_state() -> InterviewSessionState:
    state = voice_interview_state()
    return state.model_copy(
        update={
            "interview_config": state.interview_config.model_copy(
                update={"mode": InterviewMode.TEXT}
            )
        }
    )


class MockVoiceAuthService:
    def verify_id_token(self, token: str) -> CurrentUser:
        users = {
            "user-a-token": CurrentUser(uid="user-a"),
            "user-b-token": CurrentUser(uid="user-b"),
        }
        if token not in users:
            raise AuthenticationError("Invalid authentication token.")
        return users[token]


class MockVoiceRepository:
    def __init__(self) -> None:
        self.updated_states: list[dict] = []
        self.saved_turns: list[InterviewTurn] = []
        self.sessions = {
            ("user-a", "voice-session"): InterviewSessionRecord(
                session_id="voice-session",
                candidate_id="candidate-a",
                user_id="user-a",
                state_payload=voice_interview_state().model_dump(mode="json"),
            ),
            ("user-a", "text-session"): InterviewSessionRecord(
                session_id="text-session",
                candidate_id="candidate-a",
                user_id="user-a",
                state_payload=text_interview_state().model_dump(mode="json"),
            ),
            ("user-b", "other-session"): InterviewSessionRecord(
                session_id="other-session",
                candidate_id="candidate-b",
                user_id="user-b",
                state_payload={"interview_config": {"mode": "voice"}},
            ),
        }

    def get_session(self, session_id: str, *, user_id: str | None = None):
        return self.sessions.get((user_id, session_id))

    def update_session_state(
        self,
        session_id: str,
        state: str,
        state_payload: dict | None = None,
        status: str | None = None,
        user_id: str | None = None,
    ):
        record = self.get_session(session_id, user_id=user_id)
        if record is None:
            return None
        updated = record.model_copy(
            update={
                "state": state,
                "state_payload": state_payload or {},
                "status": status or record.status,
            }
        )
        self.sessions[(user_id, session_id)] = updated
        self.updated_states.append(updated.state_payload)
        return updated

    def save_turn(
        self,
        session_id: str,
        turn: InterviewTurn,
        *,
        user_id: str | None = None,
    ) -> InterviewTurn:
        if self.get_session(session_id, user_id=user_id) is None:
            raise ValueError("Session not found")
        self.saved_turns.append(turn)
        return turn


class MockVoiceOrchestrator:
    def __init__(self) -> None:
        self.calls: list[tuple[InterviewSessionState, str]] = []
        self.complete = False

    async def submit_answer(
        self,
        session_state: InterviewSessionState,
        answer: str,
        *,
        question_provider=None,
    ) -> InterviewSessionState:
        self.calls.append((session_state, answer))
        answered_turn = session_state.current_turn.model_copy(
            update={
                "answer": answer,
                "candidate_answer": answer,
                "status": "answered",
            }
        )
        next_turn = None
        if not self.complete:
            next_round = session_state.interview_plan.rounds[1]
            next_question = (
                await question_provider(
                    session_state.candidate_profile,
                    next_round,
                    session_state.interview_config,
                )
                if question_provider is not None
                else InterviewQuestion(
                    question="How do you test an async API?",
                    language="en",
                    topic="Testing",
                    difficulty="medium",
                )
            )
            next_turn = InterviewTurn(
                turn_id="turn-2",
                round_id="round-2",
                question=next_question,
                difficulty="medium",
                topic="Testing",
            )
        return session_state.model_copy(
            update={
                "current_turn": next_turn,
                "completed_turns": [
                    *session_state.completed_turns,
                    answered_turn,
                ],
                "current_question_index": 1,
            }
        )


class MockQuestionStreamingService:
    def __init__(self) -> None:
        self.calls = 0

    async def generate_question(
        self,
        candidate_profile,
        interview_round,
        interview_config,
        *,
        delta_publisher,
    ) -> InterviewQuestion:
        self.calls += 1
        await delta_publisher("How do you test")
        await delta_publisher(" an async API?")
        return InterviewQuestion(
            question="How do you test an async API?",
            language=interview_config.language,
            topic=interview_round.topic,
            difficulty=interview_round.difficulty,
        )


class MockVoiceTTS(StreamingTTS):
    def __init__(self) -> None:
        self.texts: list[str] = []

    async def synthesize_stream(self, text: str):
        self.texts.append(text)
        yield AudioChunk(
            bytes=b"\x01\x00" * 8,
            sample_rate=24000,
        )


class SlowVoiceTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        yield AudioChunk(bytes=b"\x01\x00" * 8, sample_rate=24000)
        await asyncio.sleep(60)


class WebSocketMockSTT(StreamingSTT):
    async def start_session(self) -> None:
        pass

    async def process_audio_chunk(self, audio_bytes: bytes):
        return TranscriptEvent(
            type=TranscriptEventType.PARTIAL,
            text="partial voice answer",
            language="en",
            confidence=0.8,
            timestamp=datetime.now(timezone.utc),
        )

    async def finish_session(self):
        return TranscriptEvent(
            type=TranscriptEventType.FINAL,
            text="final voice answer",
            language="en",
            confidence=0.9,
            timestamp=datetime.now(timezone.utc),
        )


class WebSocketMockSTTFactory(StreamingSTTFactory):
    def __init__(self) -> None:
        self.requested_languages: list[str | None] = []

    def create(self) -> StreamingSTT:
        return WebSocketMockSTT()

    def create_for_language(self, language: str | None) -> StreamingSTT:
        self.requested_languages.append(language)
        return self.create()


class WebSocketMockVAD(VoiceActivityDetector):
    async def reset(self) -> None:
        pass

    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        return VADFrameResult(
            is_speech=True,
            speech_started=True,
            speech_ended=True,
        )


class WebSocketMockVADFactory(VoiceActivityDetectorFactory):
    def create(self) -> VoiceActivityDetector:
        return WebSocketMockVAD()


class BlockingFinishPipeline:
    def __init__(self) -> None:
        self.finish_started = threading.Event()
        self.release_finish = threading.Event()
        self.closed = threading.Event()

    async def start(self) -> None:
        pass

    def enqueue(self, audio_bytes: bytes) -> bool:
        return True

    async def finish(self) -> None:
        self.finish_started.set()
        await asyncio.to_thread(self.release_finish.wait)

    async def close(self) -> None:
        self.release_finish.set()
        self.closed.set()


class BlockingFinishPipelineFactory:
    def __init__(self) -> None:
        self.instances: list[BlockingFinishPipeline] = []

    def create(self, **_kwargs) -> BlockingFinishPipeline:
        pipeline = BlockingFinishPipeline()
        self.instances.append(pipeline)
        return pipeline


class VoiceWebSocketTests(unittest.TestCase):
    origin = "http://testserver"

    def setUp(self) -> None:
        self.app = FastAPI()
        self.app.include_router(router)
        self.repository = MockVoiceRepository()
        self.orchestrator = MockVoiceOrchestrator()
        self.question_streaming_service = MockQuestionStreamingService()
        self.tts_service = MockVoiceTTS()
        self.question_speech_factory = QuestionSpeechStreamerFactory(
            tts_service=self.tts_service,
            queue_size=4,
            chunk_min_words=3,
            chunk_max_chars=80,
        )
        self.manager = VoiceSessionManager(max_chunk_bytes=8, max_session_bytes=32)
        self.app.dependency_overrides[get_app_settings] = lambda: Settings(
            APP_ENV="test",
            AUTH_ENABLED=True,
            CORS_ALLOWED_ORIGINS=[self.origin],
            MAX_VOICE_MESSAGE_CHARS=256,
        )
        self.app.dependency_overrides[get_auth_service] = lambda: MockVoiceAuthService()
        self.app.dependency_overrides[get_interview_repository] = lambda: self.repository
        self.app.dependency_overrides[get_voice_session_manager] = lambda: self.manager
        self.app.dependency_overrides[get_voice_answer_submission_service] = (
            lambda: VoiceAnswerSubmissionService(
                repository=self.repository,
                orchestrator=self.orchestrator,
            )
        )
        self.app.dependency_overrides[get_question_streaming_service] = (
            lambda: self.question_streaming_service
        )
        self.app.dependency_overrides[get_question_speech_streamer_factory] = (
            lambda: self.question_speech_factory
        )
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.app.dependency_overrides.clear()
        self.client.close()

    def connect(self, session_id: str = "voice-session", token: str = "user-a-token"):
        return self.client.websocket_connect(
            f"/api/v2/voice/interview/{session_id}",
            subprotocols=["firebase-auth", token],
            headers={"origin": self.origin},
        )

    def assert_rejected(
        self,
        session_id: str,
        *,
        token: str | None,
        expected_code: int,
        origin: str | None = None,
    ) -> None:
        kwargs = {"headers": {"origin": origin or self.origin}}
        if token is not None:
            kwargs["subprotocols"] = ["firebase-auth", token]
        with self.assertRaises(WebSocketDisconnect) as context:
            with self.client.websocket_connect(
                f"/api/v2/voice/interview/{session_id}",
                **kwargs,
            ):
                pass
        self.assertEqual(context.exception.code, expected_code)

    def enable_audio_pipeline(self) -> None:
        self.stt_factory = WebSocketMockSTTFactory()
        self.manager = VoiceSessionManager(
            max_chunk_bytes=16,
            max_session_bytes=64,
            pipeline_factory=AudioPipelineFactory(
                stt_factory=self.stt_factory,
                vad_factory=WebSocketMockVADFactory(),
                queue_size=4,
            ),
        )
        self.app.dependency_overrides[get_voice_session_manager] = lambda: self.manager

    def test_session_language_is_forwarded_to_stt_pipeline(self) -> None:
        self.enable_audio_pipeline()

        with self.connect() as websocket:
            self.assertEqual(websocket.receive_json()["type"], "connected")
            self.assertEqual(websocket.receive_json()["value"], "WAITING_FOR_USER")

        self.assertEqual(self.stt_factory.requested_languages, ["en"])

    def trigger_manual_answer(
        self,
        websocket,
        *,
        consume_initial: bool = True,
    ) -> list[dict]:
        if consume_initial:
            assert websocket.receive_json()["type"] == "connected"
            assert websocket.receive_json() == {
                "type": "state",
                "value": "WAITING_FOR_USER",
            }
        websocket.send_json({"type": "start_listening"})
        assert websocket.receive_json() == {
            "type": "state",
            "value": "USER_SPEAKING",
        }
        websocket.send_json(
            {
                "type": "audio_chunk",
                "sequence": 0,
                "encoding": "pcm_s16le",
                "sample_rate": 16000,
            }
        )
        websocket.send_bytes(b"\x01\x00" * 4)
        received: list[dict] = [websocket.receive_json()]
        assert received[0]["type"] == "audio_ack"
        self.assertEqual(
            len(self.orchestrator.calls),
            0,
            "VAD silence must not auto-submit before the user presses Stop.",
        )
        websocket.send_json({"type": "stop_listening"})
        while not any(event.get("type") == "processing" for event in received):
            received.append(websocket.receive_json())
        return received

    @staticmethod
    def receive_through_tts_complete(websocket) -> list[dict]:
        received: list[dict] = []
        while not any(
            item.get("type") == "tts_complete"
            for item in received
        ):
            message = websocket.receive()
            if message.get("text") is not None:
                received.append(json.loads(message["text"]))
            elif message.get("bytes") is not None:
                received.append(
                    {
                        "type": "binary_audio",
                        "bytes": message["bytes"],
                    }
                )
        return received

    def test_rejects_missing_and_invalid_authentication(self) -> None:
        self.assert_rejected("voice-session", token=None, expected_code=4401)
        self.assert_rejected("voice-session", token="bad-token", expected_code=4401)

    def test_rejects_disallowed_origin(self) -> None:
        self.assert_rejected(
            "voice-session",
            token="user-a-token",
            expected_code=4403,
            origin="https://attacker.example",
        )

    def test_rejects_cross_user_and_missing_sessions_without_disclosure(self) -> None:
        self.assert_rejected("other-session", token="user-a-token", expected_code=4404)
        self.assert_rejected("missing-session", token="user-a-token", expected_code=4404)

    def test_rejects_non_voice_session(self) -> None:
        self.assert_rejected("text-session", token="user-a-token", expected_code=4409)

    def test_transcription_mode_returns_text_without_submitting_or_speaking(self) -> None:
        self.enable_audio_pipeline()

        with self.client.websocket_connect(
            "/api/v2/voice/interview/text-session?purpose=transcription",
            subprotocols=["firebase-auth", "user-a-token"],
            headers={"origin": self.origin},
        ) as websocket:
            self.assertEqual(websocket.receive_json()["type"], "connected")
            self.assertEqual(websocket.receive_json()["value"], "WAITING_FOR_USER")
            websocket.send_json({"type": "speak_question"})
            self.assertEqual(
                websocket.receive_json(),
                {
                    "type": "error",
                    "code": "unsupported_transcription_control",
                    "message": "This control is not available for speech input.",
                },
            )
            websocket.send_json({"type": "start_listening"})
            self.assertEqual(websocket.receive_json()["value"], "USER_SPEAKING")
            websocket.send_json(
                {
                    "type": "audio_chunk",
                    "sequence": 0,
                    "encoding": "pcm_s16le",
                    "sample_rate": 16000,
                }
            )
            websocket.send_bytes(b"\x01\x00" * 4)
            self.assertEqual(websocket.receive_json()["type"], "audio_ack")
            websocket.send_json({"type": "stop_listening"})

            received: list[dict] = []
            while not any(
                event.get("type") == "state"
                and event.get("value") == "WAITING_FOR_USER"
                for event in received
            ):
                received.append(websocket.receive_json())

        self.assertTrue(
            any(
                event.get("type") == "transcript_final"
                and event.get("text") == "final voice answer"
                for event in received
            )
        )
        self.assertFalse(
            {"processing", "question_start", "tts_start", "completed"}
            & {event.get("type") for event in received}
        )
        self.assertEqual(self.orchestrator.calls, [])
        self.assertEqual(self.tts_service.texts, [])
        self.assertEqual(self.repository.updated_states, [])

    def test_text_playback_speaks_server_owned_interviewer_dialogue_only(self) -> None:
        with self.client.websocket_connect(
            "/api/v2/voice/interview/text-session?purpose=playback",
            subprotocols=["firebase-auth", "user-a-token"],
            headers={"origin": self.origin},
        ) as websocket:
            self.assertEqual(websocket.receive_json()["type"], "connected")
            turn_id = text_interview_state().current_turn.turn_id
            websocket.send_json(
                {"type": "speak_interviewer", "turn_id": turn_id}
            )
            self.assertEqual(websocket.receive_json(), {"type": "tts_start"})
            self.assertEqual(
                websocket.receive_json(),
                {"type": "audio_format", "sample_rate": 24000, "format": "pcm"},
            )
            self.assertEqual(websocket.receive_bytes(), b"\x01\x00" * 8)
            self.assertEqual(websocket.receive_json(), {"type": "tts_complete"})

            websocket.send_json(
                {
                    "type": "speak_interviewer",
                    "turn_id": turn_id,
                    "text": "Candidate-controlled text must not be spoken.",
                }
            )
            self.assertEqual(
                websocket.receive_json(),
                {
                    "type": "error",
                    "code": "invalid_message",
                    "message": "Invalid voice control message.",
                },
            )

        self.assertEqual(self.tts_service.texts, ["Explain dependency injection."])
        self.assertEqual(self.orchestrator.calls, [])
        self.assertEqual(self.repository.updated_states, [])

    def test_text_playback_uses_same_path_for_opening_follow_up_and_closing(self) -> None:
        base = text_interview_state()
        cases = (
            ("opening", "opening-turn", "Welcome to your interview."),
            ("follow_up", "follow-up-turn", "What happened next?"),
        )
        for question_type, turn_id, question in cases:
            turn = base.current_turn.model_copy(
                update={
                    "turn_id": turn_id,
                    "question": question,
                    "question_type": question_type,
                }
            )
            state = base.model_copy(
                update={
                    "phase": "opening" if question_type == "opening" else "interviewing",
                    "current_turn": turn,
                }
            )
            session_id = f"text-{question_type}"
            self.repository.sessions[("user-a", session_id)] = InterviewSessionRecord(
                session_id=session_id,
                candidate_id="candidate-a",
                user_id="user-a",
                state_payload=state.model_dump(mode="json"),
            )
            with self.client.websocket_connect(
                f"/api/v2/voice/interview/{session_id}?purpose=playback",
                subprotocols=["firebase-auth", "user-a-token"],
                headers={"origin": self.origin},
            ) as websocket:
                websocket.receive_json()
                websocket.send_json(
                    {"type": "speak_interviewer", "turn_id": turn_id}
                )
                self.assertEqual(websocket.receive_json()["type"], "tts_start")
                self.assertEqual(websocket.receive_json()["type"], "audio_format")
                websocket.receive_bytes()
                self.assertEqual(websocket.receive_json()["type"], "tts_complete")

        closing = base.model_copy(update={"phase": "closing", "current_turn": None})
        self.repository.sessions[("user-a", "text-closing")] = InterviewSessionRecord(
            session_id="text-closing",
            candidate_id="candidate-a",
            user_id="user-a",
            state_payload=closing.model_dump(mode="json"),
        )
        with self.client.websocket_connect(
            "/api/v2/voice/interview/text-closing?purpose=playback",
            subprotocols=["firebase-auth", "user-a-token"],
            headers={"origin": self.origin},
        ) as websocket:
            websocket.receive_json()
            websocket.send_json(
                {"type": "speak_interviewer", "message_kind": "closing"}
            )
            self.assertEqual(websocket.receive_json()["type"], "tts_start")
            self.assertEqual(websocket.receive_json()["type"], "audio_format")
            while True:
                message = websocket.receive()
                if message.get("bytes") is not None:
                    continue
                event = json.loads(message["text"])
                self.assertEqual(event["type"], "tts_complete")
                break

        self.assertEqual(
            self.tts_service.texts[:2],
            ["Welcome to your interview.", "What happened next?"],
        )
        self.assertEqual(
            " ".join(self.tts_service.texts[2:]),
            (
                "Thanks, Voice Candidate. That's all the questions I have "
                "for today. Thank you for your time. Your interview is now complete."
            ),
        )

    def test_connect_stream_ack_stop_and_disconnect(self) -> None:
        with self.connect() as websocket:
            self.assertEqual(websocket.accepted_subprotocol, "firebase-auth")
            self.assertEqual(
                websocket.receive_json(),
                {"type": "connected", "session_id": "voice-session"},
            )
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )

            websocket.send_json({"type": "start_listening"})
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "USER_SPEAKING"},
            )

            websocket.send_json({"type": "audio_chunk", "sequence": 1})
            websocket.send_bytes(b"audio!")
            self.assertEqual(
                websocket.receive_json(),
                {"type": "audio_ack", "sequence": 1, "bytes_received": 6},
            )

            websocket.send_json({"type": "stop_listening"})
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "TRANSCRIBING"},
            )
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )

            websocket.send_json({"type": "start_listening"})
            self.assertEqual(websocket.receive_json()["value"], "USER_SPEAKING")
            websocket.send_json({"type": "audio_chunk", "sequence": 0})
            websocket.send_bytes(b"\x01\x00")
            self.assertEqual(websocket.receive_json()["type"], "audio_ack")

        self.assertEqual(asyncio.run(self.manager.active_session_count()), 0)

    def test_disconnect_during_stop_finalization_allows_reconnect(self) -> None:
        pipeline_factory = BlockingFinishPipelineFactory()
        self.manager = VoiceSessionManager(
            max_chunk_bytes=16,
            max_session_bytes=64,
            pipeline_factory=pipeline_factory,
        )
        self.app.dependency_overrides[get_voice_session_manager] = lambda: self.manager
        first_context = self.connect()
        first = first_context.__enter__()
        try:
            self.assertEqual(first.receive_json()["type"], "connected")
            self.assertEqual(first.receive_json()["value"], "WAITING_FOR_USER")
            first.send_json({"type": "start_listening"})
            self.assertEqual(first.receive_json()["value"], "USER_SPEAKING")
            first.send_json({"type": "stop_listening"})
            self.assertEqual(first.receive_json()["value"], "TRANSCRIBING")
            pipeline = pipeline_factory.instances[0]
            self.assertTrue(pipeline.finish_started.wait(timeout=1))

            first.close()

            with self.connect() as reconnected:
                self.assertEqual(
                    reconnected.receive_json(),
                    {"type": "connected", "session_id": "voice-session"},
                )
                self.assertEqual(
                    reconnected.receive_json(),
                    {"type": "state", "value": "WAITING_FOR_USER"},
                )
        finally:
            for pipeline in pipeline_factory.instances:
                pipeline.release_finish.set()
            first_context.__exit__(None, None, None)

    def test_second_live_connection_for_same_session_is_rejected(self) -> None:
        with self.connect() as first:
            self.assertEqual(first.receive_json()["type"], "connected")
            self.assertEqual(first.receive_json()["value"], "WAITING_FOR_USER")

            self.assert_rejected(
                "voice-session",
                token="user-a-token",
                expected_code=4429,
            )

            self.assertEqual(asyncio.run(self.manager.active_session_count()), 1)

    def test_invalid_message_returns_safe_error_and_connection_stays_open(self) -> None:
        with self.connect() as websocket:
            websocket.receive_json()
            websocket.receive_json()
            websocket.send_json({"type": "unsupported", "secret": "do-not-echo"})
            response = websocket.receive_json()
            self.assertEqual(response["type"], "error")
            self.assertEqual(response["code"], "invalid_message")
            self.assertNotIn("secret", response["message"])

            websocket.send_json({"type": "start_listening"})
            self.assertEqual(websocket.receive_json()["value"], "USER_SPEAKING")

    def test_unannounced_binary_payload_is_rejected_without_disconnect(self) -> None:
        with self.connect() as websocket:
            websocket.receive_json()
            websocket.receive_json()
            websocket.send_bytes(b"audio")
            response = websocket.receive_json()
            self.assertEqual(response["type"], "error")
            self.assertEqual(response["message"], "Unexpected binary audio payload.")

    def test_oversized_audio_chunk_returns_error_and_closes(self) -> None:
        with self.connect() as websocket:
            websocket.receive_json()
            websocket.receive_json()
            websocket.send_json({"type": "start_listening"})
            websocket.receive_json()
            websocket.send_json({"type": "audio_chunk", "sequence": 1})
            websocket.send_bytes(b"too-large")
            response = websocket.receive_json()
            self.assertEqual(response["type"], "error")
            self.assertEqual(response["code"], "audio_chunk_too_large")
            with self.assertRaises(WebSocketDisconnect) as context:
                websocket.receive_json()
            self.assertEqual(context.exception.code, 1009)

    def test_cumulative_session_audio_limit_is_enforced(self) -> None:
        with self.connect() as websocket:
            websocket.receive_json()
            websocket.receive_json()
            websocket.send_json({"type": "start_listening"})
            websocket.receive_json()

            for sequence in range(4):
                websocket.send_json({"type": "audio_chunk", "sequence": sequence})
                websocket.send_bytes(b"12345678")
                self.assertEqual(websocket.receive_json()["type"], "audio_ack")

            websocket.send_json({"type": "audio_chunk", "sequence": 4})
            websocket.send_bytes(b"x")
            response = websocket.receive_json()
            self.assertEqual(response["type"], "error")
            self.assertEqual(response["code"], "voice_session_limit_exceeded")

    def test_audio_pipeline_emits_partial_and_final_transcript_events(self) -> None:
        self.enable_audio_pipeline()

        with self.connect() as websocket:
            received = self.trigger_manual_answer(websocket)
            self.assertTrue(
                any(event.get("type") == "transcript_partial" for event in received)
            )
            self.assertTrue(
                any(event.get("type") == "transcript_final" for event in received)
            )
            self.assertTrue(
                any(
                    event.get("type") == "state"
                    and event.get("value") == "TRANSCRIBING"
                    for event in received
                )
            )
            self.assertTrue(
                any(
                    event.get("type") == "state"
                    and event.get("value") == "EVALUATING"
                    for event in received
                )
            )
            self.assertEqual(len(self.orchestrator.calls), 1)

    def test_manual_stop_submits_once_and_emits_next_question(
        self,
    ) -> None:
        self.enable_audio_pipeline()
        with self.connect() as websocket:
            received = self.trigger_manual_answer(websocket)
            received.extend(self.receive_through_tts_complete(websocket))
            event_types = [event["type"] for event in received]
            self.assertLess(
                event_types.index("processing"),
                event_types.index("question_start"),
            )
            self.assertLess(
                event_types.index("question_start"),
                event_types.index("question_delta"),
            )
            self.assertLess(
                event_types.index("tts_start"),
                event_types.index("question_complete"),
            )
            self.assertLess(
                event_types.index("audio_format"),
                event_types.index("binary_audio"),
            )
            self.assertLess(
                event_types.index("binary_audio"),
                event_types.index("question_complete"),
            )
            self.assertEqual(event_types[-1], "tts_complete")
            self.assertEqual(
                next(
                    event["text"]
                    for event in received
                    if event["type"] == "question_complete"
                ),
                "How do you test an async API?",
            )
            self.assertEqual(
                next(
                    {
                        "sample_rate": event["sample_rate"],
                        "format": event["format"],
                    }
                    for event in received
                    if event["type"] == "audio_format"
                ),
                {"sample_rate": 24000, "format": "pcm"},
            )
            self.assertEqual(len(self.orchestrator.calls), 1)
            self.assertEqual(self.question_streaming_service.calls, 1)
            self.assertEqual(
                self.tts_service.texts,
                ["How do you test", "an async API?"],
            )
            self.assertEqual(
                self.orchestrator.calls[0][1],
                "final voice answer",
            )
            self.assertEqual(len(self.repository.updated_states), 1)
            self.assertEqual(len(self.repository.saved_turns), 1)
            analytics = self.repository.updated_states[0]["voice_analytics"]
            self.assertGreaterEqual(analytics["speaking_duration_ms"], 0)
            self.assertEqual(len(analytics["response_latencies_ms"]), 1)

            websocket.send_json(
                {"type": "confirm_answer", "text": "duplicate"}
            )
            self.assertEqual(
                websocket.receive_json(),
                {
                    "type": "error",
                    "code": "answer_not_ready",
                    "message": "Answer can only be submitted after transcription.",
                },
            )
            self.assertEqual(len(self.orchestrator.calls), 1)

    def test_confirm_answer_emits_completed(self) -> None:
        self.orchestrator.complete = True
        self.enable_audio_pipeline()
        with self.connect() as websocket:
            self.trigger_manual_answer(websocket)
            self.assertEqual(
                websocket.receive_json(),
                {"type": "completed"},
            )
        saved = self.repository.sessions[("user-a", "voice-session")]
        self.assertEqual(saved.status, "completed")
        self.assertEqual(len(self.orchestrator.calls), 1)

    def test_barge_in_cancels_tts_and_switches_to_listening(self) -> None:
        self.enable_audio_pipeline()
        self.question_speech_factory = QuestionSpeechStreamerFactory(
            tts_service=SlowVoiceTTS(),
            queue_size=4,
            chunk_min_words=3,
            chunk_max_chars=80,
        )
        self.app.dependency_overrides[get_voice_session_manager] = lambda: self.manager
        self.app.dependency_overrides[get_question_speech_streamer_factory] = (
            lambda: self.question_speech_factory
        )

        with self.connect() as websocket:
            received = self.trigger_manual_answer(websocket)
            while not any(event.get("type") == "tts_start" for event in received):
                message = websocket.receive()
                if message.get("text") is not None:
                    received.append(json.loads(message["text"]))

            websocket.send_json({"type": "start_barge_in"})
            websocket.send_json(
                {
                    "type": "audio_chunk",
                    "sequence": 0,
                    "encoding": "pcm_s16le",
                    "sample_rate": 16000,
                }
            )
            websocket.send_bytes(b"\x01\x00" * 4)

            while not (
                any(event.get("type") == "tts_cancelled" for event in received)
                and any(
                    event.get("type") == "state"
                    and event.get("value") == "USER_SPEAKING"
                    for event in received
                )
            ):
                message = websocket.receive()
                if message.get("text") is not None:
                    received.append(json.loads(message["text"]))

            event_types = [event["type"] for event in received]
            self.assertIn("tts_cancelled", event_types)
            self.assertIn(
                {"type": "state", "value": "INTERRUPTED"},
                received,
            )
            self.assertIn(
                {"type": "state", "value": "USER_SPEAKING"},
                received,
            )
            websocket.send_json({"type": "stop_listening"})
            processing_count = sum(
                event.get("type") == "processing" for event in received
            )
            while processing_count < 2:
                message = websocket.receive()
                if message.get("text") is not None:
                    event = json.loads(message["text"])
                    received.append(event)
                    processing_count += event.get("type") == "processing"
            self.assertEqual(len(self.orchestrator.calls), 2)

    def test_confirm_answer_rejects_empty_text(self) -> None:
        with self.connect() as websocket:
            websocket.receive_json()
            websocket.receive_json()
            websocket.send_json({"type": "confirm_answer", "text": "   "})
            response = websocket.receive_json()
            self.assertEqual(response["type"], "error")
            self.assertEqual(response["code"], "invalid_message")
        self.assertEqual(self.orchestrator.calls, [])

    def test_reconnects_after_streamed_question_completes(self) -> None:
        self.enable_audio_pipeline()
        with self.connect() as websocket:
            received = self.trigger_manual_answer(websocket)
            received.extend(self.receive_through_tts_complete(websocket))
            self.assertIn(
                "question_complete",
                [event["type"] for event in received],
            )

        with self.connect() as websocket:
            self.assertEqual(
                websocket.receive_json(),
                {"type": "connected", "session_id": "voice-session"},
            )
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )

    def test_confirm_answer_rejects_session_without_active_turn(self) -> None:
        record = self.repository.sessions[("user-a", "voice-session")]
        self.repository.sessions[("user-a", "voice-session")] = record.model_copy(
            update={
                "state_payload": voice_interview_state(
                    active_turn=False
                ).model_dump(mode="json")
            }
        )
        self.enable_audio_pipeline()
        with self.connect() as websocket:
            self.trigger_manual_answer(websocket)
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )
            self.assertEqual(
                websocket.receive_json(),
                {
                    "type": "error",
                    "code": "no_active_turn",
                    "message": "There is no active interview question.",
                },
            )
        self.assertEqual(self.orchestrator.calls, [])

    def test_confirm_answer_rechecks_session_ownership(self) -> None:
        self.enable_audio_pipeline()
        with self.connect() as websocket:
            websocket.receive_json()
            websocket.receive_json()
            record = self.repository.sessions.pop(("user-a", "voice-session"))
            self.repository.sessions[("user-b", "voice-session")] = record.model_copy(
                update={"user_id": "user-b"}
            )

            self.trigger_manual_answer(websocket, consume_initial=False)
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )
            self.assertEqual(
                websocket.receive_json(),
                {
                    "type": "error",
                    "code": "session_not_found",
                    "message": "Interview session not found.",
                },
            )
        self.assertEqual(self.orchestrator.calls, [])


if __name__ == "__main__":
    unittest.main()
