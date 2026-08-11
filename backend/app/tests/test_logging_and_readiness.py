from __future__ import annotations

import json
import logging
import unittest
from io import StringIO

from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.logging import StructuredJsonFormatter
from core.middleware import request_correlation_middleware
from core.exceptions import ConfigurationError
from core.settings import Settings
from core.startup import validate_runtime_settings


class LoggingTests(unittest.TestCase):
    def test_structured_formatter_allows_only_content_free_latency_fields(self):
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredJsonFormatter())
        logger = logging.getLogger("speech-latency-test")
        logger.handlers = [handler]
        logger.propagate = False
        logger.setLevel(logging.INFO)

        logger.info(
            "Voice turn latency measured.",
            extra={
                "event": "speech_latency",
                "stage": "answer.evaluation",
                "model": "gemini-complex",
                "task_type": "complex",
                "prompt_chars": 4200,
                "attempt": 1,
                "cache_hit": False,
                "request_id": "request-1",
                "session_id": "session-1",
                "status": "complete",
                "speech_to_stt_final_ms": 125.0,
                "audio_queue_drain_ms": 25.0,
                "stt_decode_ms": 100.0,
                "stt_to_evaluation_ms": 500.0,
                "evaluation_to_question_ms": 250.0,
                "question_to_tts_first_audio_ms": 300.0,
                "total_turn_latency_ms": 1175.0,
                "transcript": "must not be serialized",
                "prompt": "must not be serialized",
                "candidate_answer": "must not be serialized",
            },
        )
        payload = json.loads(stream.getvalue())

        self.assertEqual(payload["event"], "speech_latency")
        self.assertEqual(payload["stage"], "answer.evaluation")
        self.assertEqual(payload["model"], "gemini-complex")
        self.assertEqual(payload["task_type"], "complex")
        self.assertEqual(payload["prompt_chars"], 4200)
        self.assertEqual(payload["attempt"], 1)
        self.assertFalse(payload["cache_hit"])
        self.assertEqual(payload["request_id"], "request-1")
        self.assertEqual(payload["session_id"], "session-1")
        self.assertEqual(payload["status"], "complete")
        self.assertEqual(payload["total_turn_latency_ms"], 1175.0)
        self.assertEqual(payload["audio_queue_drain_ms"], 25.0)
        self.assertEqual(payload["stt_decode_ms"], 100.0)
        self.assertNotIn("transcript", payload)
        self.assertNotIn("prompt", payload)
        self.assertNotIn("candidate_answer", payload)

    def test_structured_formatter_redacts_email_and_bearer_token(self):
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredJsonFormatter())
        logger = logging.getLogger("structured-test")
        logger.handlers = [handler]
        logger.propagate = False
        logger.setLevel(logging.INFO)

        logger.info(
            "user@example.com Bearer secret-token",
            extra={"event": "test_event", "status_code": 200},
        )
        payload = json.loads(stream.getvalue())

        self.assertEqual(payload["severity"], "INFO")
        self.assertEqual(payload["event"], "test_event")
        self.assertNotIn("user@example.com", payload["message"])
        self.assertNotIn("secret-token", payload["message"])

    def test_exceptions_keep_message_and_stacktrace(self):
        # The formatter used to record only the exception class name, which made
        # a crash in production impossible to diagnose from the logs.
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredJsonFormatter())
        logger = logging.getLogger("structured-exception-test")
        logger.handlers = [handler]
        logger.propagate = False
        logger.setLevel(logging.INFO)

        def failing_call():
            raise ValueError("queue went missing for user@example.com")

        try:
            failing_call()
        except ValueError:
            logger.exception("Voice turn failed", extra={"event": "voice_failed"})

        payload = json.loads(stream.getvalue())

        self.assertEqual(payload["exception"], "ValueError")
        self.assertIn("queue went missing", payload["exception_message"])
        self.assertIn("failing_call", payload["stacktrace"])
        self.assertIn("ValueError", payload["stacktrace"])
        # Redaction must still apply to the new fields.
        self.assertNotIn("user@example.com", payload["exception_message"])
        self.assertNotIn("user@example.com", payload["stacktrace"])

    def test_request_id_is_accepted_or_generated_and_returned(self):
        app = FastAPI()
        app.middleware("http")(request_correlation_middleware)

        @app.get("/health")
        def health():
            return {"status": "ok"}

        client = TestClient(app)
        supplied = client.get("/health", headers={"X-Request-ID": "request-123"})
        generated = client.get("/health")

        self.assertEqual(supplied.headers["X-Request-ID"], "request-123")
        self.assertTrue(generated.headers["X-Request-ID"])


class ProductionValidationTests(unittest.TestCase):
    def production_settings(self, **overrides):
        values = {
            "APP_ENV": "production",
            "GOOGLE_CLOUD_PROJECT": "production-project",
            "REPOSITORY_BACKEND": "firestore",
            "AUTH_ENABLED": True,
            "AUTH_PROVIDER": "firebase",
            "FIREBASE_PROJECT_ID": "production-project",
            "CORS_ALLOWED_ORIGINS": "https://interview.example.com",
        }
        values.update(overrides)
        return Settings(**values)

    def test_valid_production_settings_pass(self):
        validate_runtime_settings(self.production_settings())

    def test_production_requires_firestore(self):
        with self.assertRaisesRegex(ConfigurationError, "REPOSITORY_BACKEND=firestore"):
            validate_runtime_settings(
                self.production_settings(REPOSITORY_BACKEND="sqlite")
            )

    def test_production_requires_firebase_authentication(self):
        with self.assertRaisesRegex(ConfigurationError, "Firebase authentication"):
            validate_runtime_settings(self.production_settings(AUTH_ENABLED=False))

    def test_production_requires_one_https_cors_origin(self):
        invalid_origins = (
            "",
            "http://interview.example.com",
            "https://one.example.com,https://two.example.com",
            "https://interview.example.com/path",
        )
        for origins in invalid_origins:
            with self.subTest(origins=origins):
                with self.assertRaises(ConfigurationError):
                    validate_runtime_settings(
                        self.production_settings(CORS_ALLOWED_ORIGINS=origins)
                    )


if __name__ == "__main__":
    unittest.main()
