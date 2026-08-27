import io
import wave

from fastapi.testclient import TestClient

from core.dependencies import (
    get_current_user,
    get_streaming_tts_service,
    get_uploaded_audio_transcriber,
)
from gateway.main import app
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from shared.schemas import CurrentUser


class FakeStreamingTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        assert text == "Xin chào"
        yield AudioChunk(bytes=b"\x01\x00" * 240, sample_rate=24000)


class FakeUploadedAudioTranscriber:
    locale = "vi-VN"

    def transcribe(self, audio: bytes) -> str:
        assert audio == b"audio-bytes"
        return "Xin chào"


def test_legacy_speech_endpoint_is_available():
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-1")
    app.dependency_overrides[get_streaming_tts_service] = FakeStreamingTTS
    try:
        client = TestClient(app)
        response = client.post("/api/v1/speech", json={"text": "Xin chào"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("audio/wav")
    with wave.open(io.BytesIO(response.content), "rb") as audio:
        assert audio.getframerate() == 24000
        assert audio.getnchannels() == 1
        assert audio.getsampwidth() == 2


def test_legacy_speech_recognition_endpoint_is_available():
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="user-1")
    app.dependency_overrides[get_uploaded_audio_transcriber] = (
        FakeUploadedAudioTranscriber
    )
    try:
        client = TestClient(app)
        response = client.post(
            "/api/v1/speech/recognize",
            files={"audio": ("answer.webm", b"audio-bytes", "audio/webm")},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"text": "Xin chào", "locale": "vi-VN"}
