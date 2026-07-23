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
