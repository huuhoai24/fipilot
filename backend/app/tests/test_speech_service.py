from __future__ import annotations

import unittest

from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from core.exceptions import ConfigurationError
from core.settings import Settings, get_settings
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from speech_service.dependencies import get_speech_runtime
from speech_service.main import app, validate_speech_service_settings, warm_up_models


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


class WarmableFakeTTS(FakeTTS):
    def __init__(self) -> None:
        self.warmed = False

    async def warm_up(self) -> None:
        self.warmed = True


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
        # app is module-level, so warm-up state set by a previous test leaks.
        app.state.models_ready = False
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        app.state.models_ready = False
        self.client.close()

    def test_health_is_model_independent(self):
        response = self.client.get("/internal/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "speech-inference")

    def test_local_health_and_readiness_aliases(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "ok")

        # /ready now reports whether model weights are resident, so it needs the
        # lifespan (which warms them) to have run.
        with TestClient(app) as client:
            ready = client.get("/ready")
        self.assertEqual(ready.status_code, 200)
        self.assertEqual(ready.json()["status"], "ready")
        self.assertEqual(ready.json()["models_loaded"], "true")

    def test_readiness_is_503_before_models_are_warm(self):
        response = self.client.get("/ready")
        self.assertEqual(response.status_code, 503)

    def test_startup_warms_tts_before_marking_models_ready(self):
        tts = WarmableFakeTTS()
        app.dependency_overrides[get_speech_runtime] = lambda: (
            FakePipelineFactory(),
            tts,
        )

        __import__("asyncio").run(warm_up_models(app))

        self.assertTrue(tts.warmed)

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


class SpeechServiceTokenPolicyTests(unittest.TestCase):
    """A missing SPEECH_SERVICE_TOKEN must only be tolerated locally."""

    def test_startup_rejects_missing_token_outside_local(self):
        for app_env in ("development", "staging", "production"):
            with self.subTest(app_env=app_env):
                with self.assertRaises(ConfigurationError):
                    validate_speech_service_settings(
                        Settings(APP_ENV=app_env, SPEECH_SERVICE_TOKEN="")
                    )

    def test_startup_allows_missing_token_locally(self):
        for app_env in ("local", "test"):
            with self.subTest(app_env=app_env):
                validate_speech_service_settings(
                    Settings(APP_ENV=app_env, SPEECH_SERVICE_TOKEN="")
                )

    def test_startup_allows_any_env_with_token(self):
        validate_speech_service_settings(
            Settings(APP_ENV="production", SPEECH_SERVICE_TOKEN="internal-secret")
        )

    def test_tokenless_socket_is_closed_outside_local(self):
        app.dependency_overrides[get_settings] = lambda: Settings(
            APP_ENV="development",
            SPEECH_SERVICE_TOKEN="",
        )
        app.dependency_overrides[get_speech_runtime] = lambda: (
            FakePipelineFactory(),
            FakeTTS(),
        )
        self.addCleanup(app.dependency_overrides.clear)
        # The startup guard is bypassed here on purpose: this asserts the
        # per-request check independently of lifespan validation.
        with TestClient(app) as client:
            with self.assertRaises(WebSocketDisconnect) as context:
                with client.websocket_connect("/internal/v1/inference"):
                    pass
        self.assertEqual(context.exception.code, 4401)

    def test_wrong_token_is_rejected(self):
        app.dependency_overrides[get_settings] = lambda: Settings(
            APP_ENV="production",
            SPEECH_SERVICE_TOKEN="internal-secret",
        )
        app.dependency_overrides[get_speech_runtime] = lambda: (
            FakePipelineFactory(),
            FakeTTS(),
        )
        self.addCleanup(app.dependency_overrides.clear)
        with TestClient(app) as client:
            with self.assertRaises(WebSocketDisconnect) as context:
                with client.websocket_connect(
                    "/internal/v1/inference",
                    headers={"authorization": "Bearer wrong-secret"},
                ):
                    pass
        self.assertEqual(context.exception.code, 4401)


if __name__ == "__main__":
    unittest.main()
