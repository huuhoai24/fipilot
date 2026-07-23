from __future__ import annotations

import asyncio
import json
import os

from fastapi import Depends, FastAPI, WebSocket
from pydantic import ValidationError

from core.settings import Settings, get_settings
from speech_service.contracts import SpeechControlMessage
from speech_service.dependencies import get_speech_runtime


app = FastAPI(title="AI Interview Speech Inference Service")


@app.get("/health")
@app.get("/internal/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "speech-inference"}


@app.get("/ready")
def ready(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    return {
        "status": "ready",
        "service": "speech-inference",
        "stt_model": settings.stt_model,
        "stt_device": settings.stt_device,
    }


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

    pipeline = pipeline_factory.create(
        transcript_publisher=send_json,
        endpoint_callback=lambda: send_json({"type": "endpoint"}),
        speech_started_callback=lambda: send_json({"type": "speech_started"}),
        speech_end_callback=lambda: send_json({"type": "speech_end"}),
        stt_final_callback=lambda: send_json({"type": "stt_final"}),
    )
    pipeline_started = False
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
                pipeline.enqueue(payload)
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
        return settings.app_env != "production"
    return websocket.headers.get("authorization") == f"Bearer {expected}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "9000")),
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )
