from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from contextlib import suppress

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.api.health import router as health_router
from gateway.api.auth import router as auth_v2_router
from gateway.api.candidate_profile import router as candidate_profile_v2_router
from gateway.api.interview import router as interview_v2_router
from gateway.api.report import router as report_v2_router
from gateway.api.resume import router as resume_v2_router
from gateway.api.voice import router as voice_v2_router
from core.logging import get_logger, setup_logging
from core.middleware import request_correlation_middleware
from core.settings import get_settings
from core.startup import initialize_runtime


settings = get_settings()
logger = get_logger(__name__)


async def _warm_local_speech_models(application: FastAPI) -> None:
    from core.dependencies import (
        get_audio_pipeline_factory,
        get_streaming_tts_service,
    )
    from services.voice_session.warmup import warm_up_speech_runtime

    try:
        await warm_up_speech_runtime(
            get_audio_pipeline_factory(),
            get_streaming_tts_service(),
        )
        application.state.speech_models_ready = True
        logger.info(
            "Local speech models are warm.",
            extra={"event": "speech_models_warm", "status": "ready"},
        )
    except asyncio.CancelledError:
        raise
    except Exception:
        application.state.speech_models_ready = False
        logger.exception(
            "Local speech model warm-up failed.",
            extra={"event": "speech_models_warm", "status": "failed"},
        )


@asynccontextmanager
async def lifespan(application: FastAPI):
    setup_logging(settings)
    initialize_runtime(settings)
    warmup_task: asyncio.Task[None] | None = None
    application.state.speech_models_ready = False
    if settings.speech_prewarm_models and not settings.speech_service_url:
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
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
app.include_router(health_router)
