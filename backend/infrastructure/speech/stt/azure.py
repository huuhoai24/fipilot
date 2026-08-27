from __future__ import annotations

import asyncio
import json
import subprocess
import threading
from datetime import datetime, timezone

from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:  # pragma: no cover - imported only when provider is selected
    speechsdk = None


_LANGUAGE_MAP = {"vi": "vi-VN", "en": "en-US"}


def _resolve_stt_locale(
    session_language: str | None, default_locale: str | None
) -> str:
    normalized = (session_language or "").strip().lower()
    if normalized in _LANGUAGE_MAP:
        return _LANGUAGE_MAP[normalized]
    return default_locale or "vi-VN"


def _parse_confidence(result) -> float:
    try:
        payload = json.loads(result.json)
        confidence = payload.get("Confidence")
        if isinstance(confidence, (int, float)):
            return max(0.0, min(1.0, float(confidence)))
    except Exception:
        pass
    return 0.0


class AzureSTTError(RuntimeError):
    pass


def _wait_for_recognizer_operation(recognizer, operation: str) -> None:
    """Use the SDK's completion-aware method, with a sync fallback for tests."""
    asynchronous = getattr(recognizer, f"{operation}_async", None)
    if asynchronous is not None:
        asynchronous().get()
        return
    getattr(recognizer, operation)()


class AzureUploadedAudioTranscriber:
    """Transcribe browser-recorded media with Azure without persisting audio."""

    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        speech_endpoint: str | None = None,
        recognition_locale: str = "vi-VN",
        sample_rate: int = 16000,
    ) -> None:
        if not speech_key or not (speech_region or speech_endpoint):
            raise AzureSTTError(
                "Azure Speech STT requires AZURE_SPEECH_KEY and "
                "AZURE_SPEECH_REGION (or AZURE_SPEECH_ENDPOINT)."
            )
        if speechsdk is None:
            raise AzureSTTError(
                "Install azure-cognitiveservices-speech to use Azure STT."
            )
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._speech_endpoint = speech_endpoint
        self.locale = recognition_locale
        self._sample_rate = sample_rate

    def transcribe(self, audio: bytes) -> str:
        pcm = self._decode_to_pcm(audio)
        if not pcm:
            return ""
        return self._recognize_pcm(pcm)

    def _decode_to_pcm(self, audio: bytes) -> bytes:
        conversion = subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-i",
                "-",
                "-f",
                "s16le",
                "-ac",
                "1",
                "-ar",
                str(self._sample_rate),
                "-",
            ],
            input=audio,
            capture_output=True,
            check=False,
        )
        if conversion.returncode != 0:
            details = conversion.stderr.decode("utf-8", errors="replace").strip()
            raise AzureSTTError(f"Could not decode uploaded audio: {details}")
        return conversion.stdout

    def _recognize_pcm(self, pcm: bytes) -> str:
        if self._speech_endpoint:
            config = speechsdk.SpeechConfig(
                endpoint=self._speech_endpoint,
                subscription=self._speech_key,
            )
        else:
            config = speechsdk.SpeechConfig(
                subscription=self._speech_key,
                region=self._speech_region,
            )
        config.speech_recognition_language = self.locale
        audio_format = speechsdk.audio.AudioStreamFormat(
            samples_per_second=self._sample_rate,
            bits_per_sample=16,
            channels=1,
        )
        stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=config,
            audio_config=speechsdk.audio.AudioConfig(stream=stream),
        )
        completed = threading.Event()
        transcript: list[str] = []
        cancellation_error: list[str] = []

        def recognized(event) -> None:
            if event.result.reason != speechsdk.ResultReason.RecognizedSpeech:
                return
            text = (event.result.text or "").strip()
            if text:
                transcript.append(text)

        def cancelled(event) -> None:
            details = getattr(event.result, "cancellation_details", None)
            message = getattr(details, "error_details", "") if details else ""
            if message:
                cancellation_error.append(message)
            completed.set()

        recognizer.recognized.connect(recognized)
        recognizer.session_stopped.connect(lambda _: completed.set())
        recognizer.canceled.connect(cancelled)
        recognizer.start_continuous_recognition_async().get()
        try:
            stream.write(pcm)
            stream.close()
            duration_seconds = len(pcm) / (self._sample_rate * 2)
            if not completed.wait(timeout=max(30.0, duration_seconds + 20.0)):
                raise AzureSTTError("Azure Speech recognition timed out.")
        finally:
            recognizer.stop_continuous_recognition_async().get()

        if cancellation_error and not transcript:
            raise AzureSTTError(cancellation_error[0])
        return " ".join(transcript).strip()


class AzureStreamingSTT(StreamingSTT):
    """Streaming STT backed by Azure Speech-to-Text.

    Accepts the same raw PCM16 mono @ 16 kHz frames the local faster-whisper
    adapter does, so Silero VAD keeps producing the existing speech-start/end
    and endpoint events in the pipeline. Partial and final transcripts are
    emitted directly from ``process_audio_chunk`` (no deferred partials).
    """

    supports_deferred_partials = False

    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        speech_endpoint: str | None = None,
        recognition_locale: str = "vi-VN",
    ) -> None:
        if not speech_key or not (speech_region or speech_endpoint):
            raise AzureSTTError(
                "Azure Speech STT requires AZURE_SPEECH_KEY and "
                "AZURE_SPEECH_REGION (or AZURE_SPEECH_ENDPOINT)."
            )
        if speechsdk is None:
            raise AzureSTTError(
                "Install azure-cognitiveservices-speech to use Azure STT."
            )
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._speech_endpoint = speech_endpoint
        self._recognition_locale = recognition_locale
        self._event_lock = threading.Lock()
        self._latest_partial: TranscriptEvent | None = None
        self._final: TranscriptEvent | None = None
        self._recognizer = None
        self._push_stream = None
        self._language = recognition_locale

    async def start_session(self) -> None:
        await asyncio.to_thread(self._start)

    def _start(self) -> None:
        if self._speech_endpoint:
            config = speechsdk.SpeechConfig(
                endpoint=self._speech_endpoint,
                subscription=self._speech_key,
            )
        else:
            config = speechsdk.SpeechConfig(
                subscription=self._speech_key,
                region=self._speech_region,
            )
        config.speech_recognition_language = self._recognition_locale
        self._language = self._recognition_locale
        audio_format = speechsdk.audio.AudioStreamFormat(
            samples_per_second=16000,
            bits_per_sample=16,
            channels=1,
        )
        self._push_stream = speechsdk.audio.PushAudioInputStream(
            stream_format=audio_format
        )
        audio_config = speechsdk.audio.AudioConfig(stream=self._push_stream)
        self._recognizer = speechsdk.SpeechRecognizer(
            speech_config=config,
            audio_config=audio_config,
        )
        self._recognizer.recognizing.connect(self._on_recognizing)
        self._recognizer.recognized.connect(self._on_recognized)
        _wait_for_recognizer_operation(
            self._recognizer, "start_continuous_recognition"
        )

    def _on_recognizing(self, evt) -> None:
        self._emit(evt, TranscriptEventType.PARTIAL)

    def _on_recognized(self, evt) -> None:
        self._emit(evt, TranscriptEventType.FINAL)

    def _emit(self, evt, event_type: TranscriptEventType) -> None:
        try:
            text = evt.result.text or ""
        except Exception:
            text = ""
        if not text:
            return
        transcript = TranscriptEvent(
            type=event_type,
            text=text,
            language=self._language,
            confidence=_parse_confidence(evt.result),
            timestamp=datetime.now(timezone.utc),
        )
        # Azure can finalize an utterance before VAD observes the matching
        # silence. Hold that final result until finish_session so the voice
        # pipeline submits exactly one answer per endpoint.
        with self._event_lock:
            if event_type == TranscriptEventType.FINAL:
                self._final = transcript
            else:
                self._latest_partial = transcript

    async def process_audio_chunk(
        self, audio_bytes: bytes
    ) -> TranscriptEvent | None:
        if not audio_bytes:
            return None
        self._push_stream.write(audio_bytes)
        with self._event_lock:
            partial = self._latest_partial
            self._latest_partial = None
        return partial

    async def finish_session(self) -> TranscriptEvent | None:
        if self._recognizer is not None:
            await asyncio.to_thread(
                _wait_for_recognizer_operation,
                self._recognizer,
                "stop_continuous_recognition",
            )
        if self._push_stream is not None:
            try:
                self._push_stream.close()
            except Exception:
                pass
            self._push_stream = None
        with self._event_lock:
            final = self._final or self._latest_partial
            self._latest_partial = None
            self._final = None
        return final


class AzureSTTFactory(StreamingSTTFactory):
    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        speech_endpoint: str | None = None,
        default_locale: str = "vi-VN",
    ) -> None:
        self.speech_key = speech_key
        self.speech_region = speech_region
        self.speech_endpoint = speech_endpoint
        self.default_locale = default_locale

    def create(self) -> StreamingSTT:
        return self.create_for_language(None)

    def create_for_language(self, language: str | None) -> StreamingSTT:
        locale = _resolve_stt_locale(language, self.default_locale)
        return AzureStreamingSTT(
            speech_key=self.speech_key,
            speech_region=self.speech_region,
            speech_endpoint=self.speech_endpoint,
            recognition_locale=locale,
        )
