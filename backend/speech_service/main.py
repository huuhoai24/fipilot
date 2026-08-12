from __future__ import annotations

import asyncio
import json
import os
import time
from contextlib import asynccontextmanager
from contextlib import suppress
from secrets import compare_digest

from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket
from pydantic import ValidationError

from core.exceptions import ConfigurationError
from core.logging import get_logger
from core.settings import Settings, get_settings
from services.voice_session.audio_pipeline import AudioQueueFullError
from services.voice_session.warmup import warm_up_speech_runtime
from speech_service.contracts import SpeechControlMessage
from speech_service.dependencies import get_speech_runtime


# Environments where an unauthenticated internal socket is tolerated. Anything
# else (development, staging, production) must configure SPEECH_SERVICE_TOKEN.
TOKENLESS_ENVIRONMENTS = {"local", "test"}
logger = get_logger(__name__)


def validate_speech_service_settings(settings: Settings) -> None:
    if not settings.speech_service_token and settings.app_env not in TOKENLESS_ENVIRONMENTS:
        raise ConfigurationError(
            "SPEECH_SERVICE_TOKEN is required when APP_ENV is "
            f"'{settings.app_env}'. The internal inference socket would "
            "otherwise accept unauthenticated connections."
        )


async def warm_up_models(
    application: FastAPI | None = None,
    *,
    prewarm_tts: bool = True,
) -> None:
    """Load STT/VAD weights and, when requested, TTS before the first session.

    Model weights used to load lazily inside the audio consumer loop on the
    first utterance. That took tens of seconds while PCM kept arriving, so the
    bounded audio queue overflowed and the first interview of every fresh
    process died. Paying the cost here keeps the request path warm.
    """
    # Honour a dependency override so tests warm the injected fake runtime
    # instead of downloading real weights.
    provider = get_speech_runtime
    if application is not None:
        provider = application.dependency_overrides.get(
            get_speech_runtime, get_speech_runtime
        )
    pipeline_factory, tts_service = provider()
    await warm_up_speech_runtime(
        pipeline_factory,
        tts_service,
        prewarm_tts=prewarm_tts,
    )


async def _prewarm_tts(application: FastAPI) -> None:
    provider = application.dependency_overrides.get(
        get_speech_runtime,
        get_speech_runtime,
    )
    _, tts_service = provider()
    started_at = time.perf_counter()
    try:
        metrics = await tts_service.warm_up()
        elapsed_ms = (time.perf_counter() - started_at) * 1000
        application.state.tts_prewarm_status = "ready"
        logger.info(
            "Optional TTS prewarm completed.",
            extra={
                "event": "tts_prewarm",
                "status": "ready",
                "tts_model_load_ms": getattr(metrics, "model_load_ms", None),
                "tts_prewarm_ms": getattr(metrics, "prewarm_ms", elapsed_ms),
            },
        )
    except asyncio.CancelledError:
        raise
    except Exception:
        application.state.tts_prewarm_status = "failed"
        logger.warning(
            "Optional TTS prewarm failed; lazy synthesis remains available.",
            extra={"event": "tts_prewarm", "status": "failed"},
        )


@asynccontextmanager
async def lifespan(application: FastAPI):
    settings = get_settings()
    validate_speech_service_settings(settings)
    application.state.models_ready = False
    application.state.tts_prewarm_status = (
        "pending" if settings.tts_prewarm else "disabled"
    )
    tts_prewarm_task: asyncio.Task[None] | None = None
    application.state.tts_prewarm_task = None
    if settings.tts_prewarm:
        # Start optional TTS readiness as early as possible while the existing
        # STT/VAD startup work proceeds. It remains isolated from readiness.
        tts_prewarm_task = asyncio.create_task(_prewarm_tts(application))
        application.state.tts_prewarm_task = tts_prewarm_task
    try:
        await warm_up_models(application, prewarm_tts=False)
        application.state.models_ready = True
    except Exception as error:  # pragma: no cover - depends on local model files
        application.state.warm_up_error = repr(error)
    try:
        yield
    finally:
        if tts_prewarm_task is not None and not tts_prewarm_task.done():
            tts_prewarm_task.cancel()
            with suppress(asyncio.CancelledError):
                await tts_prewarm_task


app = FastAPI(title="AI Interview Speech Inference Service", lifespan=lifespan)


@app.get("/health")
@app.get("/internal/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "speech-inference"}


@app.get("/ready")
def ready(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    models_ready = bool(getattr(request.app.state, "models_ready", False))
    payload = {
        "status": "ready" if models_ready else "loading",
        "service": "speech-inference",
        "stt_model": settings.stt_model,
        "stt_device": settings.stt_device,
        "stt_compute_type": settings.stt_compute_type,
        "models_loaded": "true" if models_ready else "false",
    }
    if models_ready:
        return payload
    # Report not-ready until the weights are actually resident, otherwise an
    # orchestrator routes traffic to a process that cannot keep up yet.
    error = getattr(request.app.state, "warm_up_error", None)
    if error:
        payload["error"] = str(error)
    raise HTTPException(status_code=503, detail=payload)


@app.websocket("/internal/v1/inference")
async def inference(
    websocket: WebSocket,
    settings: Settings = Depends(get_settings),
    runtime=Depends(get_speech_runtime),
) -> None:
    if not _authorized(websocket, settings):
        await websocket.close(code=4401, reason="Internal authentication required.")
        return

    pipeline_factory, tts_service = runtime
    send_lock = asyncio.Lock()

    async def send_json(payload: dict) -> None:
        async with send_lock:
            await websocket.send_json(payload)

    pipeline = None
    pipeline_started = False
    dropped = 0
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive()
            if message["type"] == "websocket.disconnect":
                return
            if message.get("bytes") is not None:
                payload = message["bytes"]
                if (
                    not pipeline_started
                    or not payload
                    or len(payload) > settings.max_voice_chunk_bytes
                ):
                    await send_json(
                        {"type": "error", "code": "invalid_audio"}
                    )
                    continue
                # Never let backpressure escape this handler: an exception here
                # tears down the socket and ends the interview. Dropping frames
                # degrades one utterance instead.
                try:
                    accepted = pipeline.enqueue(payload)
                except (AudioQueueFullError, RuntimeError):
                    accepted = False
                if accepted is False:
                    dropped += 1
                    if dropped in (1, 10, 100) or dropped % 500 == 0:
                        await send_json(
                            {
                                "type": "audio_dropped",
                                "code": "audio_queue_full",
                                "dropped": dropped,
                            }
                        )
                continue
            if message.get("text") is None:
                continue
            try:
                control = SpeechControlMessage.model_validate(
                    json.loads(message["text"])
                )
            except (json.JSONDecodeError, ValidationError):
                await send_json(
                    {"type": "error", "code": "invalid_control"}
                )
                continue

            if control.type == "stt_start":
                if pipeline is None:
                    pipeline = pipeline_factory.create(
                        language=control.language,
                        transcript_publisher=send_json,
                        endpoint_callback=lambda: send_json({"type": "endpoint"}),
                        speech_started_callback=lambda: send_json({"type": "speech_started"}),
                        speech_end_callback=lambda: send_json(
                            {"type": "speech_end"}
                        ),
                        stt_final_callback=lambda: send_json({"type": "stt_final"}),
                    )
                await pipeline.start()
                pipeline_started = True
                await send_json({"type": "stt_started"})
            elif control.type == "stt_finish":
                if pipeline_started:
                    await pipeline.finish()
                    pipeline_started = False
                await send_json({"type": "stt_complete"})
            else:
                await _stream_tts(websocket, tts_service, control.text or "")
    finally:
        if pipeline is not None:
            await pipeline.close()


async def _stream_tts(websocket: WebSocket, tts_service, text: str) -> None:
    sent_format = False
    await websocket.send_json({"type": "tts_start"})
    async for chunk in tts_service.synthesize_stream(text.strip()):
        if not sent_format:
            await websocket.send_json(
                {
                    "type": "audio_format",
                    "sample_rate": chunk.sample_rate,
                    "format": chunk.format,
                }
            )
            sent_format = True
        await websocket.send_bytes(chunk.bytes)
    await websocket.send_json({"type": "tts_complete"})


def _authorized(websocket: WebSocket, settings: Settings) -> bool:
    expected = settings.speech_service_token
    if not expected:
        return settings.app_env in TOKENLESS_ENVIRONMENTS
    return compare_digest(
        websocket.headers.get("authorization", ""),
        f"Bearer {expected}",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "9000")),
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )
