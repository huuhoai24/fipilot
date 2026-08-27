from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from contextlib import suppress

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from gateway.api.health import router as health_router
from gateway.api.auth import router as auth_v2_router
from gateway.api.candidate_profile import router as candidate_profile_v2_router
from gateway.api.interview import router as interview_v2_router
from gateway.api.report import router as report_v2_router
from gateway.api.resume import router as resume_v2_router
from gateway.api.legacy_speech import router as legacy_speech_router
from gateway.api.voice import router as voice_v2_router
from core.logging import get_logger, get_request_id, setup_logging
from core.middleware import request_correlation_middleware
from core.settings import get_settings
from core.startup import initialize_runtime
from infrastructure.llm.vertex_gemini import LLMServiceError


settings = get_settings()
logger = get_logger(__name__)


async def _warm_local_speech_models(application: FastAPI) -> None:
    from core.dependencies import (
        get_audio_pipeline_factory,
        get_streaming_tts_service,
    )
    from services.voice_session.warmup import warm_up_speech_runtime

    try:
        metrics = await warm_up_speech_runtime(
            get_audio_pipeline_factory(),
            get_streaming_tts_service(),
            prewarm_tts=(
                settings.tts_prewarm or settings.speech_prewarm_models
            ),
            prewarm_stt_vad=settings.speech_prewarm_models,
        )
        application.state.speech_models_ready = True
        logger.info(
            "Local speech models are warm.",
            extra={
                "event": "speech_models_warm",
                "status": "ready",
                "tts_model_load_ms": getattr(metrics, "model_load_ms", None),
                "tts_prewarm_ms": getattr(metrics, "prewarm_ms", None),
            },
        )
    except asyncio.CancelledError:
        raise
    except Exception:
        application.state.speech_models_ready = False
        logger.warning(
            "Optional local speech warm-up failed; lazy loading remains available.",
            extra={"event": "speech_models_warm", "status": "failed"},
        )


@asynccontextmanager
async def lifespan(application: FastAPI):
    setup_logging(settings)
    initialize_runtime(settings)
    warmup_task: asyncio.Task[None] | None = None
    application.state.speech_models_ready = False
    if (
        settings.tts_prewarm or settings.speech_prewarm_models
    ) and not settings.speech_service_url:
        warmup_task = asyncio.create_task(_warm_local_speech_models(application))
        application.state.speech_warmup_task = warmup_task
    application.state.ready = True
    try:
        yield
    finally:
        application.state.ready = False
        if warmup_task is not None and not warmup_task.done():
            warmup_task.cancel()
            with suppress(asyncio.CancelledError):
                await warmup_task


app = FastAPI(title="CV-Driven AI Interviewer", lifespan=lifespan)
app.middleware("http")(request_correlation_middleware)


@app.exception_handler(LLMServiceError)
async def handle_llm_service_error(
    request: Request,
    error: LLMServiceError,
) -> JSONResponse:
    logger.warning(
        "AI processing request failed safely.",
        extra={"event": "llm_request_failed", "status": "transient_failure"},
    )
    return JSONResponse(
        status_code=503,
        content={
            "error": {
                "code": "transient_service_failure",
                "message": "AI processing is temporarily unavailable. Please try again.",
                "retryable": True,
                "issues": [],
            },
            "request_id": get_request_id(),
        },
    )

if settings.app_env in {"local", "test"}:
    # Reflect any localhost/127.0.0.1 origin so local frontend dev works
    # regardless of the Vite dev port.
    cors_allow_origins: list[str] = []
    cors_allow_origin_regex = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"
else:
    cors_allow_origins = settings.cors_allowed_origins
    cors_allow_origin_regex = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_origin_regex=cors_allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["ETag"],
)

app.include_router(resume_v2_router)
app.include_router(interview_v2_router)
app.include_router(report_v2_router)
app.include_router(auth_v2_router)
app.include_router(candidate_profile_v2_router)
app.include_router(voice_v2_router)
app.include_router(legacy_speech_router)
app.include_router(health_router)
