from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gateway.api.health import router as health_router
from gateway.api.auth import router as auth_v2_router
from gateway.api.interview import router as interview_v2_router
from gateway.api.report import router as report_v2_router
from gateway.api.resume import router as resume_v2_router
from gateway.api.voice import router as voice_v2_router
from core.logging import setup_logging
from core.middleware import request_correlation_middleware
from core.settings import get_settings
from core.startup import initialize_runtime


settings = get_settings()


@asynccontextmanager
async def lifespan(application: FastAPI):
    setup_logging(settings)
    initialize_runtime(settings)
    application.state.ready = True
    yield
    application.state.ready = False


app = FastAPI(title="CV-Driven AI Interviewer", lifespan=lifespan)
app.middleware("http")(request_correlation_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_v2_router)
app.include_router(interview_v2_router)
app.include_router(report_v2_router)
app.include_router(auth_v2_router)
app.include_router(voice_v2_router)
app.include_router(health_router)
