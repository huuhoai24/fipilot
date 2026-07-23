from __future__ import annotations

import unittest

from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from core.settings import Settings, get_settings
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from speech_service.dependencies import get_speech_runtime
from speech_service.main import app


class FakePipeline:
    async def start(self) -> None:
        pass

    def enqueue(self, payload: bytes) -> None:
        pass

    async def finish(self) -> None:
        pass

    async def close(self) -> None:
        pass


class FakePipelineFactory:
    def create(self, **kwargs):
        return FakePipeline()


class FakeTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        yield AudioChunk(bytes=b"\x01\x00" * 4, sample_rate=24000)


class SpeechServiceBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        app.dependency_overrides[get_settings] = lambda: Settings(
            APP_ENV="production",
            SPEECH_SERVICE_TOKEN="internal-secret",
        )
        app.dependency_overrides[get_speech_runtime] = lambda: (
            FakePipelineFactory(),
            FakeTTS(),
        )
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.client.close()

    def test_health_is_model_independent(self):
        response = self.client.get("/internal/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "speech-inference")

    def test_local_health_and_readiness_aliases(self):
        health = self.client.get("/health")
        ready = self.client.get("/ready")

        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "ok")
        self.assertEqual(ready.status_code, 200)
        self.assertEqual(ready.json()["status"], "ready")

    def test_internal_websocket_requires_service_token(self):
        with self.assertRaises(WebSocketDisconnect) as context:
            with self.client.websocket_connect("/internal/v1/inference"):
                pass
        self.assertEqual(context.exception.code, 4401)

    def test_tts_streams_metadata_binary_and_completion(self):
        with self.client.websocket_connect(
            "/internal/v1/inference",
            headers={"authorization": "Bearer internal-secret"},
        ) as websocket:
            websocket.send_json(
                {"type": "tts_synthesize", "text": "Internal test"}
            )
            self.assertEqual(websocket.receive_json(), {"type": "tts_start"})
            self.assertEqual(
                websocket.receive_json(),
                {
                    "type": "audio_format",
                    "sample_rate": 24000,
                    "format": "pcm",
                },
            )
            self.assertEqual(websocket.receive_bytes(), b"\x01\x00" * 4)
            self.assertEqual(websocket.receive_json(), {"type": "tts_complete"})


if __name__ == "__main__":
    unittest.main()
