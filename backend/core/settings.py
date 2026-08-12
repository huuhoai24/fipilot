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
    resume_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Low-latency structured extraction model. Reads GEMINI_RESUME_MODEL.",
    )
    resume_location: str = Field(
        default="global",
        description="Vertex endpoint used only for Resume extraction. Reads GEMINI_RESUME_LOCATION.",
    )
    # The evaluator runs while a voice candidate waits in silence. Measured
    # ~25 s on the complex model versus ~13.5 s on the simple one. Kept on the
    # stronger model by default because the score is the product's output.
    evaluator_task_type: Literal["simple", "complex"] = Field(
        default="complex", description="Reads EVALUATOR_TASK_TYPE."
    )


class DatabaseSettings(BaseModel):
    """Temporary persistence settings for the V2 MVP."""

    url: str = Field(default="sqlite:///./interview_app.db", description="Reads DATABASE_URL.")


class DevelopmentSettings(BaseModel):
    """Development limits and guardrails."""

    max_resume_bytes: int = 10 * 1024 * 1024
    max_answer_chars: int = 12000
    default_interview_turns: int = 8
    max_interview_turns: int = 12
    max_voice_chunk_bytes: int = 256 * 1024
    max_voice_session_bytes: int = 64 * 1024 * 1024
    max_voice_message_chars: int = 4096
    interview_preparation_ttl_seconds: int = Field(default=300, ge=30, le=3600)
    interview_preparation_max_entries: int = Field(default=128, ge=1, le=4096)


class SpeechSettings(BaseModel):
    """Streaming speech recognition, VAD, and synthesis settings.

    Defaults are sized for a single-GPU developer laptop (~4 GB VRAM). See
    backend/.env.speech.example for the CUDA-specific overrides.
    """

    # large-v3-turbo is a distilled large-v3: far better on Vietnamese mixed with
    # English technical terms than `medium`, and small enough for 4 GB VRAM
    # (~1.0 GB at int8_float16, ~1.6 GB at float16).
    stt_model: str = "large-v3-turbo"
    stt_device: str = "cpu"
    # int8 is the portable choice. On CUDA prefer int8_float16 (see env example).
    stt_compute_type: str = "int8"
    stt_language: str = "vi"
    stt_vocabulary_profile: Literal[
        "auto",
        "ai_engineer",
        "backend",
        "frontend",
        "data_engineer",
        "devops",
    ] = "auto"
    stt_hotwords: list[str] = Field(default_factory=list)
    # 800 frames of 512 samples is ~25 s of audio for under 1 MB of RAM. The old
    # 64-frame (2 s) buffer could not absorb a single transcription pass, so any
    # normal-length answer overflowed it.
    audio_queue_size: int = 800
    # Each partial re-transcribes the utterance so far; 1 s was more often than a
    # laptop GPU can finish, which starved the audio consumer.
    partial_interval_ms: int = 2500
    # Stop spending GPU on partials past this much buffered speech and save it
    # for the final transcript, which is the one that gets scored.
    partial_max_audio_ms: int = 20000
    # Partials run greedy; the final transcript gets a real beam search.
    final_beam_size: int = 2
    vad_threshold: float = 0.5
    # 500 ms endpointed on ordinary mid-sentence pauses, cutting answers in half.
    vad_min_silence_ms: int = 900
    vad_speech_pad_ms: int = 120
    tts_mode: str = "v3turbo"
    tts_device: str = "auto"
    tts_voice: str | None = None
    tts_sample_rate: int = 24000
    tts_frame_duration_ms: int = 100
    tts_queue_size: int = 8
    tts_chunk_min_words: int = 3
    tts_chunk_max_chars: int = 80
    service_token: str | None = None
    service_url: str | None = None
    benchmark_mode: bool = False
    prewarm_models: bool = False
    tts_prewarm: bool = False


class AuthenticationSettings(BaseModel):
    """Authentication and local identity fallback settings."""

    enabled: bool = True
    provider: str = "firebase"
    firebase_project_id: str | None = None
    dev_user_id: str = "local-development-user"


class CorsSettings(BaseModel):
    """Browser origins allowed to call the FastAPI gateway."""

    allowed_origins: list[str] = Field(default_factory=list)


class RepositorySettings(BaseModel):
    """Persistence backend and Firestore collection settings."""

    backend: Literal["sqlite", "firestore"] = "sqlite"
    firestore_database: str = "(default)"
    users_collection: str = "users"
    candidates_collection: str = "candidates"
    interviews_collection: str = "interviews"


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


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_list(name: str, default: list[str]) -> list[str]:
    value = os.getenv(name)
    if value is None:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


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
    speech: SpeechSettings = Field(default_factory=SpeechSettings)
    authentication: AuthenticationSettings = Field(default_factory=AuthenticationSettings)
    cors: CorsSettings = Field(default_factory=CorsSettings)
    repository: RepositorySettings = Field(default_factory=RepositorySettings)

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
        speech_data = dict(data.pop("speech", {}) or {})
        auth_data = dict(data.pop("authentication", {}) or {})
        cors_data = dict(data.pop("cors", {}) or {})
        repository_data = dict(data.pop("repository", {}) or {})

        app_data.setdefault("app_env", os.getenv("APP_ENV", os.getenv("ENVIRONMENT", "local")))
        app_data.setdefault("debug", _env_bool("DEBUG", False))
        app_data.setdefault("log_level", os.getenv("LOG_LEVEL", "INFO"))
        app_data.setdefault("app_name", os.getenv("APP_NAME", "AI Interview Platform"))

        google_data.setdefault("project", os.getenv("GOOGLE_CLOUD_PROJECT"))
        google_data.setdefault("location", os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))

        llm_data.setdefault("simple_model", os.getenv("GEMINI_SIMPLE_MODEL", "gemini-2.5-flash"))
        llm_data.setdefault("complex_model", os.getenv("GEMINI_COMPLEX_MODEL", "gemini-2.5-pro"))
        llm_data.setdefault(
            "resume_model",
            os.getenv("GEMINI_RESUME_MODEL", "gemini-2.5-flash-lite"),
        )
        llm_data.setdefault(
            "resume_location",
            os.getenv("GEMINI_RESUME_LOCATION", "global"),
        )
        llm_data.setdefault(
            "evaluator_task_type", os.getenv("EVALUATOR_TASK_TYPE", "complex")
        )

        database_data.setdefault("url", os.getenv("DATABASE_URL", os.getenv("SQLITE_DATABASE_URL", "sqlite:///./interview_app.db")))

        development_data.setdefault("max_resume_bytes", _env_int("MAX_RESUME_BYTES", 10 * 1024 * 1024))
        development_data.setdefault("max_answer_chars", _env_int("MAX_ANSWER_CHARS", 12000))
        development_data.setdefault("default_interview_turns", _env_int("DEFAULT_INTERVIEW_TURNS", 8))
        development_data.setdefault("max_interview_turns", _env_int("MAX_INTERVIEW_TURNS", 12))
        development_data.setdefault(
            "max_voice_chunk_bytes", _env_int("MAX_VOICE_CHUNK_BYTES", 256 * 1024)
        )
        development_data.setdefault(
            "max_voice_session_bytes",
            _env_int("MAX_VOICE_SESSION_BYTES", 64 * 1024 * 1024),
        )
        development_data.setdefault(
            "max_voice_message_chars", _env_int("MAX_VOICE_MESSAGE_CHARS", 4096)
        )
        development_data.setdefault(
            "interview_preparation_ttl_seconds",
            _env_int("INTERVIEW_PREPARATION_TTL_SECONDS", 300),
        )
        development_data.setdefault(
            "interview_preparation_max_entries",
            _env_int("INTERVIEW_PREPARATION_MAX_ENTRIES", 128),
        )
        speech_data.setdefault(
            "stt_model", os.getenv("STT_MODEL", SpeechSettings.model_fields["stt_model"].default)
        )
        speech_data.setdefault("stt_device", os.getenv("STT_DEVICE", "cpu"))
        speech_data.setdefault("stt_compute_type", os.getenv("STT_COMPUTE_TYPE", "int8"))
        speech_data.setdefault("stt_language", os.getenv("STT_LANGUAGE", "vi"))
        speech_data.setdefault(
            "stt_vocabulary_profile",
            os.getenv("STT_VOCABULARY_PROFILE", "auto"),
        )
        speech_data.setdefault(
            "stt_hotwords",
            _env_list("STT_HOTWORDS", []),
        )
        speech_data.setdefault(
            "audio_queue_size", _env_int("STT_AUDIO_QUEUE_SIZE", 800)
        )
        speech_data.setdefault(
            "partial_interval_ms", _env_int("STT_PARTIAL_INTERVAL_MS", 2500)
        )
        speech_data.setdefault(
            "partial_max_audio_ms", _env_int("STT_PARTIAL_MAX_AUDIO_MS", 20000)
        )
        speech_data.setdefault(
            "final_beam_size", _env_int("STT_FINAL_BEAM_SIZE", 2)
        )
        speech_data.setdefault("vad_threshold", _env_float("VAD_THRESHOLD", 0.5))
        speech_data.setdefault(
            "vad_min_silence_ms", _env_int("VAD_MIN_SILENCE_MS", 900)
        )
        speech_data.setdefault(
            "vad_speech_pad_ms", _env_int("VAD_SPEECH_PAD_MS", 120)
        )
        speech_data.setdefault("tts_mode", os.getenv("TTS_MODE", "v3turbo"))
        speech_data.setdefault("tts_device", os.getenv("TTS_DEVICE", "auto"))
        speech_data.setdefault("tts_voice", os.getenv("TTS_VOICE") or None)
        speech_data.setdefault(
            "tts_sample_rate", _env_int("TTS_SAMPLE_RATE", 24000)
        )
        speech_data.setdefault(
            "tts_frame_duration_ms",
            _env_int("TTS_FRAME_DURATION_MS", 100),
        )
        speech_data.setdefault(
            "tts_queue_size", _env_int("TTS_QUEUE_SIZE", 8)
        )
        speech_data.setdefault(
            "tts_chunk_min_words", _env_int("TTS_CHUNK_MIN_WORDS", 3)
        )
        speech_data.setdefault(
            "tts_chunk_max_chars", _env_int("TTS_CHUNK_MAX_CHARS", 80)
        )
        speech_data.setdefault(
            "service_token", os.getenv("SPEECH_SERVICE_TOKEN") or None
        )
        speech_data.setdefault(
            "service_url", os.getenv("SPEECH_SERVICE_URL") or None
        )
        speech_data.setdefault(
            "benchmark_mode", _env_bool("SPEECH_BENCHMARK_MODE", False)
        )
        speech_data.setdefault(
            "prewarm_models", _env_bool("SPEECH_PREWARM_MODELS", False)
        )
        speech_data.setdefault("tts_prewarm", _env_bool("TTS_PREWARM", False))

        auth_data.setdefault("enabled", _env_bool("AUTH_ENABLED", True))
        auth_data.setdefault("provider", os.getenv("AUTH_PROVIDER", "firebase"))
        auth_data.setdefault("firebase_project_id", os.getenv("FIREBASE_PROJECT_ID"))
        auth_data.setdefault(
            "dev_user_id", os.getenv("AUTH_DEV_USER_ID", "local-development-user")
        )
        repository_data.setdefault(
            "backend", os.getenv("REPOSITORY_BACKEND", "sqlite")
        )
        repository_data.setdefault(
            "firestore_database", os.getenv("FIRESTORE_DATABASE", "(default)")
        )
        repository_data.setdefault(
            "users_collection", os.getenv("FIRESTORE_USERS_COLLECTION", "users")
        )
        repository_data.setdefault(
            "candidates_collection",
            os.getenv("FIRESTORE_CANDIDATES_COLLECTION", "candidates"),
        )
        repository_data.setdefault(
            "interviews_collection",
            os.getenv("FIRESTORE_INTERVIEWS_COLLECTION", "interviews"),
        )

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
        resume_model = _take(data, "gemini_resume_model", "GEMINI_RESUME_MODEL")
        if resume_model is not None:
            llm_data["resume_model"] = resume_model
        resume_location = _take(
            data, "gemini_resume_location", "GEMINI_RESUME_LOCATION"
        )
        if resume_location is not None:
            llm_data["resume_location"] = resume_location
        evaluator_task_type = _take(data, "evaluator_task_type", "EVALUATOR_TASK_TYPE")
        if evaluator_task_type is not None:
            llm_data["evaluator_task_type"] = evaluator_task_type

        database_url = _take(data, "database_url", "DATABASE_URL", "sqlite_database_url")
        if database_url is not None:
            database_data["url"] = database_url

        max_resume_bytes = _take(data, "max_resume_bytes", "MAX_RESUME_BYTES")
        if max_resume_bytes is not None:
            development_data["max_resume_bytes"] = max_resume_bytes
        max_answer_chars = _take(data, "max_answer_chars", "MAX_ANSWER_CHARS")
        if max_answer_chars is not None:
            development_data["max_answer_chars"] = max_answer_chars
        preparation_ttl = _take(
            data,
            "interview_preparation_ttl_seconds",
            "INTERVIEW_PREPARATION_TTL_SECONDS",
        )
        if preparation_ttl is not None:
            development_data["interview_preparation_ttl_seconds"] = preparation_ttl
        preparation_max_entries = _take(
            data,
            "interview_preparation_max_entries",
            "INTERVIEW_PREPARATION_MAX_ENTRIES",
        )
        if preparation_max_entries is not None:
            development_data["interview_preparation_max_entries"] = (
                preparation_max_entries
            )

        stt_model = _take(data, "stt_model", "STT_MODEL")
        if stt_model is not None:
            speech_data["stt_model"] = stt_model
        stt_device = _take(data, "stt_device", "STT_DEVICE")
        if stt_device is not None:
            speech_data["stt_device"] = stt_device
        stt_compute_type = _take(data, "stt_compute_type", "STT_COMPUTE_TYPE")
        if stt_compute_type is not None:
            speech_data["stt_compute_type"] = stt_compute_type
        stt_language = _take(data, "stt_language", "STT_LANGUAGE")
        if stt_language is not None:
            speech_data["stt_language"] = stt_language
        stt_vocabulary_profile = _take(
            data,
            "stt_vocabulary_profile",
            "STT_VOCABULARY_PROFILE",
        )
        if stt_vocabulary_profile is not None:
            speech_data["stt_vocabulary_profile"] = stt_vocabulary_profile
        stt_hotwords = _take(data, "stt_hotwords", "STT_HOTWORDS")
        if stt_hotwords is not None:
            speech_data["stt_hotwords"] = (
                [item.strip() for item in stt_hotwords.split(",") if item.strip()]
                if isinstance(stt_hotwords, str)
                else stt_hotwords
            )
        for field_name, env_name in (
            ("tts_mode", "TTS_MODE"),
            ("tts_device", "TTS_DEVICE"),
            ("tts_voice", "TTS_VOICE"),
            ("tts_sample_rate", "TTS_SAMPLE_RATE"),
            ("tts_frame_duration_ms", "TTS_FRAME_DURATION_MS"),
            ("tts_queue_size", "TTS_QUEUE_SIZE"),
            ("tts_chunk_min_words", "TTS_CHUNK_MIN_WORDS"),
            ("tts_chunk_max_chars", "TTS_CHUNK_MAX_CHARS"),
            ("service_token", "SPEECH_SERVICE_TOKEN"),
            ("service_url", "SPEECH_SERVICE_URL"),
            ("benchmark_mode", "SPEECH_BENCHMARK_MODE"),
            ("prewarm_models", "SPEECH_PREWARM_MODELS"),
            ("tts_prewarm", "TTS_PREWARM"),
        ):
            value = _take(data, field_name, env_name)
            if value is not None:
                speech_data[field_name] = value

        auth_enabled = _take(data, "auth_enabled", "AUTH_ENABLED")
        if auth_enabled is not None:
            auth_data["enabled"] = auth_enabled
        auth_provider = _take(data, "auth_provider", "AUTH_PROVIDER")
        if auth_provider is not None:
            auth_data["provider"] = auth_provider
        firebase_project_id = _take(data, "firebase_project_id", "FIREBASE_PROJECT_ID")
        if firebase_project_id is not None:
            auth_data["firebase_project_id"] = firebase_project_id
        auth_dev_user_id = _take(data, "auth_dev_user_id", "AUTH_DEV_USER_ID")
        if auth_dev_user_id is not None:
            auth_data["dev_user_id"] = auth_dev_user_id
        cors_allowed_origins = _take(data, "cors_allowed_origins", "CORS_ALLOWED_ORIGINS")
        if cors_allowed_origins is not None:
            cors_data["allowed_origins"] = (
                [item.strip() for item in cors_allowed_origins.split(",") if item.strip()]
                if isinstance(cors_allowed_origins, str)
                else cors_allowed_origins
            )
        else:
            local_origins = ["http://127.0.0.1:5173", "http://localhost:5173"]
            cors_default = [] if app_data["app_env"] == "production" else local_origins
            cors_data.setdefault(
                "allowed_origins", _env_list("CORS_ALLOWED_ORIGINS", cors_default)
            )

        repository_backend = _take(data, "repository_backend", "REPOSITORY_BACKEND")
        if repository_backend is not None:
            repository_data["backend"] = repository_backend
        firestore_database = _take(data, "firestore_database", "FIRESTORE_DATABASE")
        if firestore_database is not None:
            repository_data["firestore_database"] = firestore_database
        users_collection = _take(
            data, "firestore_users_collection", "FIRESTORE_USERS_COLLECTION"
        )
        if users_collection is not None:
            repository_data["users_collection"] = users_collection
        candidates_collection = _take(
            data,
            "firestore_candidates_collection",
            "FIRESTORE_CANDIDATES_COLLECTION",
        )
        if candidates_collection is not None:
            repository_data["candidates_collection"] = candidates_collection
        interviews_collection = _take(
            data,
            "firestore_interviews_collection",
            "FIRESTORE_INTERVIEWS_COLLECTION",
        )
        if interviews_collection is not None:
            repository_data["interviews_collection"] = interviews_collection

        super().__init__(
            application=ApplicationSettings(**app_data),
            google_cloud=GoogleCloudSettings(**google_data),
            llm_routing=LLMRoutingSettings(**llm_data),
            database=DatabaseSettings(**database_data),
            development=DevelopmentSettings(**development_data),
            speech=SpeechSettings(**speech_data),
            authentication=AuthenticationSettings(**auth_data),
            cors=CorsSettings(**cors_data),
            repository=RepositorySettings(**repository_data),
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
    def gemini_resume_model(self) -> str:
        return self.llm_routing.resume_model

    @property
    def gemini_resume_location(self) -> str:
        return self.llm_routing.resume_location

    @property
    def evaluator_task_type(self) -> str:
        return self.llm_routing.evaluator_task_type

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

    @property
    def max_voice_chunk_bytes(self) -> int:
        return self.development.max_voice_chunk_bytes

    @property
    def max_voice_session_bytes(self) -> int:
        return self.development.max_voice_session_bytes

    @property
    def max_voice_message_chars(self) -> int:
        return self.development.max_voice_message_chars

    @property
    def interview_preparation_ttl_seconds(self) -> int:
        return self.development.interview_preparation_ttl_seconds

    @property
    def interview_preparation_max_entries(self) -> int:
        return self.development.interview_preparation_max_entries

    @property
    def stt_model(self) -> str:
        return self.speech.stt_model

    @property
    def stt_device(self) -> str:
        return self.speech.stt_device

    @property
    def stt_compute_type(self) -> str:
        return self.speech.stt_compute_type

    @property
    def stt_language(self) -> str:
        return self.speech.stt_language

    @property
    def stt_vocabulary_profile(self) -> str:
        return self.speech.stt_vocabulary_profile

    @property
    def stt_hotwords(self) -> list[str]:
        return list(self.speech.stt_hotwords)

    @property
    def stt_audio_queue_size(self) -> int:
        return self.speech.audio_queue_size

    @property
    def stt_partial_interval_ms(self) -> int:
        return self.speech.partial_interval_ms

    @property
    def stt_partial_max_audio_ms(self) -> int:
        return self.speech.partial_max_audio_ms

    @property
    def stt_final_beam_size(self) -> int:
        return self.speech.final_beam_size

    @property
    def vad_threshold(self) -> float:
        return self.speech.vad_threshold

    @property
    def vad_min_silence_ms(self) -> int:
        return self.speech.vad_min_silence_ms

    @property
    def vad_speech_pad_ms(self) -> int:
        return self.speech.vad_speech_pad_ms

    @property
    def tts_mode(self) -> str:
        return self.speech.tts_mode

    @property
    def tts_device(self) -> str:
        return self.speech.tts_device

    @property
    def tts_voice(self) -> str | None:
        return self.speech.tts_voice

    @property
    def tts_sample_rate(self) -> int:
        return self.speech.tts_sample_rate

    @property
    def tts_frame_duration_ms(self) -> int:
        return self.speech.tts_frame_duration_ms

    @property
    def tts_queue_size(self) -> int:
        return self.speech.tts_queue_size

    @property
    def tts_chunk_min_words(self) -> int:
        return self.speech.tts_chunk_min_words

    @property
    def tts_chunk_max_chars(self) -> int:
        return self.speech.tts_chunk_max_chars

    @property
    def speech_service_token(self) -> str | None:
        return self.speech.service_token

    @property
    def speech_service_url(self) -> str | None:
        return self.speech.service_url

    @property
    def speech_benchmark_mode(self) -> bool:
        return self.speech.benchmark_mode

    @property
    def speech_prewarm_models(self) -> bool:
        return self.speech.prewarm_models

    @property
    def tts_prewarm(self) -> bool:
        return self.speech.tts_prewarm

    @property
    def auth_enabled(self) -> bool:
        return self.authentication.enabled

    @property
    def auth_provider(self) -> str:
        return self.authentication.provider

    @property
    def firebase_project_id(self) -> str | None:
        return self.authentication.firebase_project_id or self.google_cloud_project

    @property
    def auth_dev_user_id(self) -> str:
        return self.authentication.dev_user_id

    @property
    def cors_allowed_origins(self) -> list[str]:
        return self.cors.allowed_origins

    @property
    def repository_backend(self) -> str:
        return self.repository.backend

    @property
    def firestore_database(self) -> str:
        return self.repository.firestore_database

    @property
    def firestore_users_collection(self) -> str:
        return self.repository.users_collection

    @property
    def firestore_candidates_collection(self) -> str:
        return self.repository.candidates_collection

    @property
    def firestore_interviews_collection(self) -> str:
        return self.repository.interviews_collection


@lru_cache
def get_settings() -> Settings:
    return Settings()
