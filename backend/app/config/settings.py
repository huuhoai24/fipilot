"""Application settings for the V2 architecture.

The existing application still uses its current configuration. These settings
are scoped to the new V2 modules and will be wired in later milestones.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    HAS_PYDANTIC_SETTINGS = True
except ImportError:  # pragma: no cover - allows tests before dependencies are installed
    from pydantic import BaseModel as BaseSettings

    SettingsConfigDict = dict
    HAS_PYDANTIC_SETTINGS = False


class ApplicationSettings(BaseModel):
    """Application-level runtime flags."""

    app_env: Literal["local", "development", "staging", "production", "test"] = Field(
        default="local",
        description="Deployment environment. Reads APP_ENV.",
    )
    debug: bool = Field(default=False, description="Enable debug behavior. Reads DEBUG.")
    log_level: str = Field(default="INFO", description="Process log level. Reads LOG_LEVEL.")
    app_name: str = "AI Interview Platform"


class GoogleCloudSettings(BaseModel):
    """Google Cloud and Vertex AI location settings."""

    project: str | None = Field(default=None, description="Google Cloud project id. Reads GOOGLE_CLOUD_PROJECT.")
    location: str = Field(default="us-central1", description="Vertex AI region. Reads GOOGLE_CLOUD_LOCATION.")


class LLMRoutingSettings(BaseModel):
    """Model names used by future LLM routing."""

    simple_model: str = Field(default="gemini-2.5-flash", description="Reads GEMINI_SIMPLE_MODEL.")
    complex_model: str = Field(default="gemini-2.5-pro", description="Reads GEMINI_COMPLEX_MODEL.")


class DatabaseSettings(BaseModel):
    """Temporary persistence settings for the V2 MVP."""

    url: str = Field(default="sqlite:///./interview_app.db", description="Reads DATABASE_URL.")


class DevelopmentSettings(BaseModel):
    """Development limits and guardrails."""

    max_resume_bytes: int = 10 * 1024 * 1024
    max_answer_chars: int = 12000
    default_interview_turns: int = 8
    max_interview_turns: int = 12


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _take(data: dict, *names: str):
    for name in names:
        if name in data:
            return data.pop(name)
    return None


class Settings(BaseSettings):
    """Runtime configuration for V2 services.

    Environment variable groups:
    - Application: APP_ENV, DEBUG, LOG_LEVEL
    - Google Cloud: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
    - LLM routing: GEMINI_SIMPLE_MODEL, GEMINI_COMPLEX_MODEL
    - Database: DATABASE_URL
    - Development limits: MAX_RESUME_BYTES, MAX_ANSWER_CHARS, etc.
    """

    application: ApplicationSettings = Field(default_factory=ApplicationSettings)
    google_cloud: GoogleCloudSettings = Field(default_factory=GoogleCloudSettings)
    llm_routing: LLMRoutingSettings = Field(default_factory=LLMRoutingSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    development: DevelopmentSettings = Field(default_factory=DevelopmentSettings)

    if HAS_PYDANTIC_SETTINGS:
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    else:
        model_config = {"env_file": ".env", "extra": "ignore"}

    def __init__(self, **data):
        app_data = dict(data.pop("application", {}) or {})
        google_data = dict(data.pop("google_cloud", {}) or {})
        llm_data = dict(data.pop("llm_routing", {}) or {})
        database_data = dict(data.pop("database", {}) or {})
        development_data = dict(data.pop("development", {}) or {})

        app_data.setdefault("app_env", os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "local")))
        app_data.setdefault("debug", _env_bool("DEBUG", False))
        app_data.setdefault("log_level", os.getenv("LOG_LEVEL", "INFO"))
        app_data.setdefault("app_name", os.getenv("APP_NAME", "AI Interview Platform"))

        google_data.setdefault("project", os.getenv("GOOGLE_CLOUD_PROJECT"))
        google_data.setdefault("location", os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))

        llm_data.setdefault("simple_model", os.getenv("GEMINI_SIMPLE_MODEL", "gemini-2.5-flash"))
        llm_data.setdefault("complex_model", os.getenv("GEMINI_COMPLEX_MODEL", "gemini-2.5-pro"))

        database_data.setdefault("url", os.getenv("DATABASE_URL", os.getenv("SQLITE_DATABASE_URL", "sqlite:///./interview_app.db")))

        development_data.setdefault("max_resume_bytes", _env_int("MAX_RESUME_BYTES", 10 * 1024 * 1024))
        development_data.setdefault("max_answer_chars", _env_int("MAX_ANSWER_CHARS", 12000))
        development_data.setdefault("default_interview_turns", _env_int("DEFAULT_INTERVIEW_TURNS", 8))
        development_data.setdefault("max_interview_turns", _env_int("MAX_INTERVIEW_TURNS", 12))

        app_env = _take(data, "app_env", "APP_ENV", "environment")
        if app_env is not None:
            app_data["app_env"] = app_env
        debug = _take(data, "debug", "DEBUG")
        if debug is not None:
            app_data["debug"] = debug
        log_level = _take(data, "log_level", "LOG_LEVEL")
        if log_level is not None:
            app_data["log_level"] = log_level

        project = _take(data, "google_cloud_project", "GOOGLE_CLOUD_PROJECT")
        if project is not None:
            google_data["project"] = project
        location = _take(data, "google_cloud_location", "GOOGLE_CLOUD_LOCATION")
        if location is not None:
            google_data["location"] = location

        simple_model = _take(data, "gemini_simple_model", "GEMINI_SIMPLE_MODEL")
        if simple_model is not None:
            llm_data["simple_model"] = simple_model
        complex_model = _take(data, "gemini_complex_model", "GEMINI_COMPLEX_MODEL")
        if complex_model is not None:
            llm_data["complex_model"] = complex_model

        database_url = _take(data, "database_url", "DATABASE_URL", "sqlite_database_url")
        if database_url is not None:
            database_data["url"] = database_url

        max_resume_bytes = _take(data, "max_resume_bytes", "MAX_RESUME_BYTES")
        if max_resume_bytes is not None:
            development_data["max_resume_bytes"] = max_resume_bytes
        max_answer_chars = _take(data, "max_answer_chars", "MAX_ANSWER_CHARS")
        if max_answer_chars is not None:
            development_data["max_answer_chars"] = max_answer_chars

        super().__init__(
            application=ApplicationSettings(**app_data),
            google_cloud=GoogleCloudSettings(**google_data),
            llm_routing=LLMRoutingSettings(**llm_data),
            database=DatabaseSettings(**database_data),
            development=DevelopmentSettings(**development_data),
            **data,
        )

    @property
    def app_env(self) -> str:
        return self.application.app_env

    @property
    def debug(self) -> bool:
        return self.application.debug

    @property
    def log_level(self) -> str:
        return self.application.log_level

    @property
    def google_cloud_project(self) -> str | None:
        return self.google_cloud.project

    @property
    def google_cloud_location(self) -> str:
        return self.google_cloud.location

    @property
    def gemini_simple_model(self) -> str:
        return self.llm_routing.simple_model

    @property
    def gemini_complex_model(self) -> str:
        return self.llm_routing.complex_model

    @property
    def database_url(self) -> str:
        return self.database.url

    @property
    def max_resume_bytes(self) -> int:
        return self.development.max_resume_bytes

    @property
    def max_answer_chars(self) -> int:
        return self.development.max_answer_chars

    @property
    def default_interview_turns(self) -> int:
        return self.development.default_interview_turns

    @property
    def max_interview_turns(self) -> int:
        return self.development.max_interview_turns


@lru_cache
def get_settings() -> Settings:
    return Settings()
