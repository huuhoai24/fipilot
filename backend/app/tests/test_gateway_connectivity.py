from __future__ import annotations

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from core.dependencies import (
    get_app_settings,
    get_auth_service,
    get_document_service,
    get_interview_repository,
    get_resume_agent,
)
from core.settings import Settings
from gateway.main import app


class GatewayConnectivityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()

    def test_health_readiness_and_required_frontend_routes_are_mounted(self) -> None:
        route_paths = set(app.openapi()["paths"])
        self.assertIn('/health', route_paths)
        self.assertIn('/ready', route_paths)
        self.assertIn('/api/v2/resume/upload', route_paths)
        self.assertIn('/api/v2/candidates/{candidate_id}/profile', route_paths)

        health = self.client.get('/health')
        with patch(
            'gateway.api.health.check_runtime_readiness',
            return_value={'status': 'ready', 'repository': 'sqlite'},
        ):
            readiness = self.client.get('/ready')

        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json(), {'status': 'ok'})
        self.assertEqual(readiness.status_code, 200)
        self.assertEqual(readiness.json()['status'], 'ready')

    def test_resume_upload_without_bearer_authentication_returns_401(self) -> None:
        app.dependency_overrides[get_app_settings] = lambda: Settings(
            APP_ENV='test',
            AUTH_ENABLED=True,
            GOOGLE_CLOUD_PROJECT='test-project',
        )
        app.dependency_overrides[get_auth_service] = lambda: object()
        app.dependency_overrides[get_interview_repository] = lambda: object()
        app.dependency_overrides[get_document_service] = lambda: object()
        app.dependency_overrides[get_resume_agent] = lambda: object()

        response = self.client.post(
            '/api/v2/resume/upload',
            files={'file': ('resume.pdf', b'%PDF mocked resume', 'application/pdf')},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['www-authenticate'], 'Bearer')

    def test_cors_allows_the_local_frontend_origin_for_resume_upload(self) -> None:
        response = self.client.options(
            '/api/v2/resume/upload',
            headers={
                'Origin': 'http://localhost:5173',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'authorization,content-type',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get('access-control-allow-origin'),
            'http://localhost:5173',
        )


if __name__ == '__main__':
    unittest.main()
