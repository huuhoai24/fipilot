"""Regression tests for voice failures found while driving a real interview.

Each test here pins a bug that made the voice interview unusable:

* Both audio pipelines raised AttributeError out of close(), which killed the
  WebSocket after the first question.
* A full audio queue tore the connection down instead of dropping a frame.
* Late audio frames (the VAD endpoints mid-sentence while the client is still
  streaming) produced one error event per frame.
* The WebSocket ignored AUTH_ENABLED, so local development could not use voice.
* The current question was never spoken; only follow-ups were.
"""
from __future__ import annotations

import asyncio
import json
import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.dependencies import (
    get_app_settings,
    get_auth_service,
    get_interview_repository,
    get_question_speech_streamer_factory,
    get_question_streaming_service,
    get_voice_answer_submission_service,
    get_voice_session_manager,
)
from core.settings import Settings
from gateway.api.voice import router
from infrastructure.speech.remote import RemoteAudioPipeline
from infrastructure.speech.stt.base import StreamingSTT
from services.voice_session.audio_pipeline import (
    AudioPipeline,
    VADFrameResult,
    VoiceActivityDetector,
)
from services.voice_session.manager import VoiceSessionManager
from services.voice_session.schemas import VoiceSessionStatus
from services.voice_session.transcript_service import TranscriptService

from app.tests.test_voice_websocket import (
    MockQuestionStreamingService,
    MockVoiceAuthService,
    MockVoiceOrchestrator,
    MockVoiceRepository,
    MockVoiceTTS,
)
from services.voice_session.question_speech import QuestionSpeechStreamerFactory
from services.voice_session.answer_service import VoiceAnswerSubmissionService


class _IdleSTT(StreamingSTT):
    async def start_session(self) -> None: ...

    async def process_audio_chunk(self, audio_bytes: bytes):
        return None

    async def finish_session(self):
        return None


class _SilentVAD(VoiceActivityDetector):
    async def reset(self) -> None: ...

    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        return VADFrameResult(is_speech=False)


class _BlockedVAD(VoiceActivityDetector):
    """Never returns, so the consumer cannot drain the queue."""

    async def reset(self) -> None: ...

    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        await asyncio.Event().wait()
        raise AssertionError("unreachable")


class _FakeRemoteWebSocket:
    def __init__(self) -> None:
        self.sent: list[object] = []

    async def send(self, payload) -> None:
        self.sent.append(payload)

    async def recv(self) -> str:
        return json.dumps({"type": "stt_started"})

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.Event().wait()
        raise StopAsyncIteration


class _FakeRemoteContext:
    def __init__(self) -> None:
        self.websocket = _FakeRemoteWebSocket()
        self.exited = False

    async def __aenter__(self):
        return self.websocket

    async def __aexit__(self, *exc_info):
        self.exited = True
        return False


class AudioPipelineShutdownTests(unittest.IsolatedAsyncioTestCase):
    def _pipeline(self, vad: VoiceActivityDetector, queue_size: int = 8) -> AudioPipeline:
        return AudioPipeline(
            stt=_IdleSTT(),
            vad=vad,
            transcript_service=TranscriptService(lambda payload: asyncio.sleep(0)),
            queue_size=queue_size,
        )

    async def test_close_does_not_raise_from_the_worker(self):
        pipeline = self._pipeline(_SilentVAD())
        await pipeline.start()
        pipeline.enqueue(b"\x00\x00" * 256)
        await asyncio.sleep(0)
        worker = pipeline._worker

        await pipeline.close()

        self.assertIsNotNone(worker)
        self.assertTrue(worker.done())
        # A cancelled worker is fine; an AttributeError from `finally` is not.
        if not worker.cancelled():
            self.assertIsNone(worker.exception())

    async def test_close_while_the_consumer_is_mid_frame_does_not_raise(self):
        pipeline = self._pipeline(_BlockedVAD())
        await pipeline.start()
        pipeline.enqueue(b"\x00\x00" * 256)
        await asyncio.sleep(0.02)
        worker = pipeline._worker

        await pipeline.close()

        self.assertTrue(worker.done())
        if not worker.cancelled():
            self.assertIsNone(worker.exception())

    async def test_full_queue_drops_the_frame_instead_of_raising(self):
        pipeline = self._pipeline(_BlockedVAD(), queue_size=2)
        await pipeline.start()
        await asyncio.sleep(0.02)

        accepted = [pipeline.enqueue(b"\x00\x00" * 8) for _ in range(6)]

        self.assertIn(False, accepted)
        self.assertGreater(pipeline.dropped_chunks, 0)
        await pipeline.close()


class RemoteAudioPipelineShutdownTests(unittest.IsolatedAsyncioTestCase):
    def _pipeline(self, context: _FakeRemoteContext, queue_size: int = 8):
        return RemoteAudioPipeline(
            service_url="http://speech.invalid:9000",
            service_token=None,
            queue_size=queue_size,
            transcript_publisher=lambda payload: asyncio.sleep(0),
            endpoint_callback=None,
            speech_started_callback=None,
            speech_end_callback=None,
            stt_final_callback=None,
            connector=lambda url, **kwargs: context,
        )

    async def test_close_does_not_raise(self):
        context = _FakeRemoteContext()
        pipeline = self._pipeline(context)
        await pipeline.start()
        pipeline.enqueue(b"\x00\x00" * 128)
        await asyncio.sleep(0.02)

        await pipeline.close()

        self.assertTrue(context.exited)

    async def test_finish_then_close_does_not_raise(self):
        context = _FakeRemoteContext()
        pipeline = self._pipeline(context)
        await pipeline.start()
        pipeline.enqueue(b"\x00\x00" * 128)
        await asyncio.sleep(0.02)
        pipeline._complete.set()

        await pipeline.finish()

        self.assertTrue(context.exited)

    async def test_full_queue_drops_the_frame(self):
        context = _FakeRemoteContext()
        pipeline = self._pipeline(context, queue_size=1)
        await pipeline.start()
        # Stop the sender so nothing drains.
        pipeline._sender.cancel()
        await asyncio.sleep(0.01)

        accepted = [pipeline.enqueue(b"\x00\x00" * 8) for _ in range(4)]

        self.assertIn(False, accepted)
        self.assertGreater(pipeline.dropped_chunks, 0)


class LateAudioFrameTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.manager = VoiceSessionManager(
            max_chunk_bytes=1024,
            max_session_bytes=1024 * 64,
        )
        await self.manager.connect("s1", "u1")

    async def test_announce_after_listening_stopped_is_not_an_error(self):
        await self.manager.start_listening("s1", "u1")
        await self.manager.stop_listening("s1", "u1")

        accepted = await self.manager.announce_audio_chunk("s1", "u1", 0)

        self.assertFalse(accepted)

    async def test_binary_after_listening_stopped_is_ignored(self):
        await self.manager.start_listening("s1", "u1")
        await self.manager.stop_listening("s1", "u1")
        await self.manager.announce_audio_chunk("s1", "u1", 0)

        result = await self.manager.receive_audio_chunk("s1", "u1", b"\x00\x00" * 16)

        self.assertIsNone(result)

    async def test_binary_without_metadata_while_listening_still_errors(self):
        await self.manager.start_listening("s1", "u1")

        with self.assertRaises(Exception):
            await self.manager.receive_audio_chunk("s1", "u1", b"\x00\x00" * 16)


class VoiceWebSocketBehaviourTests(unittest.TestCase):
    origin = "http://testserver"

    def _build(self, *, auth_enabled: bool) -> None:
        self.app = FastAPI()
        self.app.include_router(router)
        self.repository = MockVoiceRepository()
        self.tts_service = MockVoiceTTS()
        self.manager = VoiceSessionManager(max_chunk_bytes=64, max_session_bytes=4096)
        self.app.dependency_overrides[get_app_settings] = lambda: Settings(
            APP_ENV="test",
            AUTH_ENABLED=auth_enabled,
            AUTH_DEV_USER_ID="user-a",
            CORS_ALLOWED_ORIGINS=[self.origin],
            MAX_VOICE_MESSAGE_CHARS=256,
        )
        self.app.dependency_overrides[get_auth_service] = lambda: MockVoiceAuthService()
        self.app.dependency_overrides[get_interview_repository] = lambda: self.repository
        self.app.dependency_overrides[get_voice_session_manager] = lambda: self.manager
        self.app.dependency_overrides[get_voice_answer_submission_service] = (
            lambda: VoiceAnswerSubmissionService(
                repository=self.repository,
                orchestrator=MockVoiceOrchestrator(),
            )
        )
        self.app.dependency_overrides[get_question_streaming_service] = (
            lambda: MockQuestionStreamingService()
        )
        self.app.dependency_overrides[get_question_speech_streamer_factory] = (
            lambda: QuestionSpeechStreamerFactory(
                tts_service=self.tts_service,
                queue_size=4,
                chunk_min_words=3,
                chunk_max_chars=80,
            )
        )
        self.client = TestClient(self.app)
        self.addCleanup(self.client.close)
        self.addCleanup(self.app.dependency_overrides.clear)

    def test_auth_disabled_allows_connection_without_a_token(self):
        self._build(auth_enabled=False)

        with self.client.websocket_connect(
            "/api/v2/voice/interview/voice-session",
            headers={"origin": self.origin},
        ) as websocket:
            self.assertEqual(websocket.receive_json()["type"], "connected")
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )

    def test_auth_enabled_still_requires_a_token(self):
        self._build(auth_enabled=True)

        with self.assertRaises(Exception):
            with self.client.websocket_connect(
                "/api/v2/voice/interview/voice-session",
                headers={"origin": self.origin},
            ):
                pass

    def test_speak_question_reads_the_current_question_aloud(self):
        self._build(auth_enabled=True)

        with self.client.websocket_connect(
            "/api/v2/voice/interview/voice-session",
            subprotocols=["firebase-auth", "user-a-token"],
            headers={"origin": self.origin},
        ) as websocket:
            self.assertEqual(websocket.receive_json()["type"], "connected")
            self.assertEqual(
                websocket.receive_json(),
                {"type": "state", "value": "WAITING_FOR_USER"},
            )

            websocket.send_json({"type": "speak_question"})

            types: list[str] = []
            audio_frames = 0
            for _ in range(40):
                message = websocket.receive()
                if "bytes" in message and message["bytes"] is not None:
                    audio_frames += 1
                    continue
                payload = json.loads(message["text"])
                types.append(payload["type"])
                if payload["type"] == "tts_complete":
                    break

            self.assertIn("question_start", types)
            self.assertIn("question_delta", types)
            self.assertIn("question_complete", types)
            self.assertIn("tts_start", types)
            self.assertIn("tts_complete", types)
            self.assertGreater(audio_frames, 0)


if __name__ == "__main__":
    unittest.main()
