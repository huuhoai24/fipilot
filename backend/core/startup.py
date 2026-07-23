from __future__ import annotations

from urllib.parse import urlparse

from sqlalchemy import text

from core.dependencies import build_interview_repository
from core.exceptions import ConfigurationError
from core.settings import Settings


def validate_runtime_settings(settings: Settings) -> None:
    if not settings.google_cloud_project:
        raise ConfigurationError("GOOGLE_CLOUD_PROJECT is required")
    if settings.repository_backend not in {"sqlite", "firestore"}:
        raise ConfigurationError(
            f"Unsupported repository backend: {settings.repository_backend}"
        )
    if settings.auth_enabled:
        if settings.auth_provider != "firebase":
            raise ConfigurationError(
                f"Unsupported authentication provider: {settings.auth_provider}"
            )
        if not settings.firebase_project_id:
            raise ConfigurationError(
                "FIREBASE_PROJECT_ID or GOOGLE_CLOUD_PROJECT is required"
            )
    if settings.app_env == "production":
        if settings.repository_backend != "firestore":
            raise ConfigurationError(
                "Production requires REPOSITORY_BACKEND=firestore"
            )
        if not settings.auth_enabled or settings.auth_provider != "firebase":
            raise ConfigurationError(
                "Production requires Firebase authentication"
            )
        if len(settings.cors_allowed_origins) != 1:
            raise ConfigurationError(
                "Production requires exactly one CORS_ALLOWED_ORIGINS value"
            )
        origin = urlparse(settings.cors_allowed_origins[0])
        if (
            origin.scheme != "https"
            or not origin.netloc
            or origin.path not in {"", "/"}
            or origin.query
            or origin.fragment
            or origin.hostname in {"localhost", "127.0.0.1"}
        ):
            raise ConfigurationError(
                "Production CORS_ALLOWED_ORIGINS must be one HTTPS origin"
            )


def initialize_runtime(settings: Settings) -> None:
    validate_runtime_settings(settings)
    if settings.repository_backend == "sqlite":
        from database import Base, engine

        Base.metadata.create_all(bind=engine)
        return
    build_interview_repository(settings)


def check_runtime_readiness(settings: Settings) -> dict[str, str]:
    validate_runtime_settings(settings)
    if settings.repository_backend == "sqlite":
        from database import engine

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    else:
        repository = build_interview_repository(settings)
        repository.check_ready()
    return {
        "status": "ready",
        "repository": settings.repository_backend,
    }
