"""Compatibility HTTP adapter for the legacy browser speech player."""

from __future__ import annotations

import io
import wave
import asyncio

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from pydantic import BaseModel, Field

from core.dependencies import (
    get_app_settings,
    get_current_user,
    get_streaming_tts_service,
    get_uploaded_audio_transcriber,
)
from core.settings import Settings
from core.logging import get_logger
from infrastructure.speech.tts.base import StreamingTTS
from shared.schemas import CurrentUser


router = APIRouter(tags=["legacy-speech"])
logger = get_logger(__name__)


class LegacySpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4096)


class UploadedAudioTranscriber:
    locale: str

    def transcribe(self, audio: bytes) -> str:
        raise NotImplementedError


def _pcm_wav(audio: bytes, sample_rate: int) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(audio)
    return buffer.getvalue()


@router.post("/api/v1/speech", response_class=Response)
async def synthesize_legacy_speech(
    request: LegacySpeechRequest,
    _current_user: CurrentUser = Depends(get_current_user),
    tts_service: StreamingTTS = Depends(get_streaming_tts_service),
) -> Response:
    """Return Azure-backed PCM as WAV for the existing V1 audio element."""
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="Speech text must not be blank.")

    try:
        sample_rate: int | None = None
        pcm = bytearray()
        async for chunk in tts_service.synthesize_stream(text):
            if chunk.format != "pcm":
                raise RuntimeError("TTS returned an unsupported audio format.")
            if sample_rate is None:
                sample_rate = chunk.sample_rate
            elif chunk.sample_rate != sample_rate:
                raise RuntimeError("TTS changed sample rate during synthesis.")
            pcm.extend(chunk.bytes)
        if sample_rate is None or not pcm:
            raise RuntimeError("TTS returned no audio.")
        return Response(content=_pcm_wav(bytes(pcm), sample_rate), media_type="audio/wav")
    except Exception as error:
        logger.exception("Legacy speech synthesis failed")
        raise HTTPException(status_code=502, detail="Speech synthesis failed.") from error


@router.post("/api/v1/speech/recognize")
async def recognize_legacy_speech(
    audio: UploadFile = File(...),
    _current_user: CurrentUser = Depends(get_current_user),
    settings: Settings = Depends(get_app_settings),
    transcriber: UploadedAudioTranscriber = Depends(get_uploaded_audio_transcriber),
) -> dict[str, str]:
    """Transcribe V1 browser media with the configured Azure STT provider."""
    content = await audio.read()
    if not content:
        raise HTTPException(status_code=400, detail="The recording is empty.")
    if len(content) > settings.max_voice_session_bytes:
        raise HTTPException(status_code=413, detail="The recording is too large.")
    try:
        text = await asyncio.to_thread(transcriber.transcribe, content)
    except Exception as error:
        logger.exception("Legacy speech recognition failed")
        raise HTTPException(status_code=502, detail="Speech recognition failed.") from error
    if not text:
        raise HTTPException(status_code=422, detail="Không nhận diện được giọng nói. Hãy nói rõ hơn.")
    return {"text": text, "locale": transcriber.locale}
