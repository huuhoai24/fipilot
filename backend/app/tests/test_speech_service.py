from __future__ import annotations

import asyncio
import threading
import unittest
from unittest.mock import patch

from fastapi import FastAPI
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
    def __init__(self) -> None:
        self.languages: list[str | None] = []

    def create(self, **kwargs):
        self.languages.append(kwargs.get("language"))
        return FakePipeline()


class FakeTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        yield AudioChunk(bytes=b"\x01\x00" * 4, sample_rate=24000)


class WarmableFakeTTS(FakeTTS):
    def __init__(self) -> None:
        self.warmed = False
        self.warm_up_calls = 0

    async def warm_up(self) -> None:
        self.warm_up_calls += 1
        self.warmed = True


class BlockingWarmableFakeTTS(FakeTTS):
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def warm_up(self) -> None:
        self.started.set()
        await self.release.wait()


class FailingWarmableFakeTTS(FakeTTS):
    def __init__(self) -> None:
        self.attempted = threading.Event()

    async def warm_up(self) -> None:
        self.attempted.set()
        raise RuntimeError("sensitive model path must not escape")


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

        asyncio.run(warm_up_models(app))

        self.assertTrue(tts.warmed)

    def test_startup_skips_optional_tts_prewarm_when_disabled(self):
        tts = WarmableFakeTTS()
        app.dependency_overrides[get_speech_runtime] = lambda: (
            FakePipelineFactory(),
            tts,
        )
        disabled = Settings(
            APP_ENV="test",
            SPEECH_SERVICE_TOKEN="",
            TTS_PREWARM=False,
        )

        with patch("speech_service.main.get_settings", return_value=disabled):
            with TestClient(app) as client:
                self.assertEqual(client.get("/health").status_code, 200)

        self.assertEqual(tts.warm_up_calls, 0)

    def test_enabled_tts_prewarm_runs_after_service_becomes_operational(self):
        async def scenario() -> None:
            from speech_service.main import lifespan

            tts = BlockingWarmableFakeTTS()
            test_app = FastAPI()
            test_app.dependency_overrides[get_speech_runtime] = lambda: (
                FakePipelineFactory(),
                tts,
            )
            enabled = Settings(
                APP_ENV="test",
                SPEECH_SERVICE_TOKEN="",
                TTS_PREWARM=True,
            )
            entered = asyncio.Event()

            async def run_lifespan() -> None:
                async with lifespan(test_app):
                    entered.set()
                    await tts.release.wait()

            with patch("speech_service.main.get_settings", return_value=enabled):
                task = asyncio.create_task(run_lifespan())
                await tts.started.wait()
                try:
                    self.assertTrue(entered.is_set())
                finally:
                    tts.release.set()
                    await task

        asyncio.run(scenario())

    def test_tts_prewarm_failure_keeps_readiness_and_lazy_synthesis_available(self):
        tts = FailingWarmableFakeTTS()
        app.dependency_overrides[get_speech_runtime] = lambda: (
            FakePipelineFactory(),
            tts,
        )
        enabled = Settings(
            APP_ENV="test",
            SPEECH_SERVICE_TOKEN="",
            TTS_PREWARM=True,
        )

        with self.assertLogs("speech_service.main", level="WARNING") as logs:
            with patch("speech_service.main.get_settings", return_value=enabled):
                with TestClient(app) as client:
                    self.assertTrue(tts.attempted.wait(timeout=1))
                    self.assertEqual(client.get("/ready").status_code, 200)
                    with client.websocket_connect(
                        "/internal/v1/inference",
                        headers={"authorization": "Bearer internal-secret"},
                    ) as websocket:
                        websocket.send_json(
                            {"type": "tts_synthesize", "text": "Retry lazily"}
                        )
                        self.assertEqual(websocket.receive_json()["type"], "tts_start")
                        self.assertEqual(websocket.receive_json()["type"], "audio_format")
                        self.assertTrue(websocket.receive_bytes())
                        self.assertEqual(websocket.receive_json()["type"], "tts_complete")

        self.assertEqual(app.state.tts_prewarm_status, "failed")
        self.assertNotIn("sensitive model path", " ".join(logs.output))

    def test_internal_websocket_requires_service_token(self):
        with self.assertRaises(WebSocketDisconnect) as context:
            with self.client.websocket_connect("/internal/v1/inference"):
                pass
        self.assertEqual(context.exception.code, 4401)

    def test_stt_start_uses_requested_session_language(self):
        factory = FakePipelineFactory()
        app.dependency_overrides[get_speech_runtime] = lambda: (factory, FakeTTS())

        with self.client.websocket_connect(
            "/internal/v1/inference",
            headers={"authorization": "Bearer internal-secret"},
        ) as websocket:
            websocket.send_json({"type": "stt_start", "language": "vi"})
            self.assertEqual(websocket.receive_json(), {"type": "stt_started"})

        self.assertEqual(factory.languages, ["vi"])

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
