from __future__ import annotations

import asyncio
import threading
import time
from datetime import datetime, timezone
from typing import Any, Callable

from core.logging import get_logger
from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)


logger = get_logger(__name__)

# The pipeline hands over 16 kHz mono PCM16 frames (see events.py Literal[16000]).
_SAMPLE_RATE = 16_000
_BITS_PER_SAMPLE = 16
_CHANNELS = 1
_FINAL_TIMEOUT_S = 10.0

_LANGUAGE_TAGS = {"vi": "vi-VN", "en": "en-US"}
_FALLBACK_TAG = "en-US"


def _language_tag(language: str | None) -> str:
    return _LANGUAGE_TAGS.get((language or "").lower()[:2], _FALLBACK_TAG)


class AzureStreamingSTT(StreamingSTT):
    """Azure Speech adapter behind the streaming STT seam.

    Reuses the flow the minimal deployment proved: push raw PCM into Azure,
    accumulate recognized segments, and join them into one final transcript.
    Partials come from Azure's ``recognizing`` events through the deferred
    partial contract so inference never blocks the audio consumer.
    """

    supports_deferred_partials = True

    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        language: str = "vi",
        partial_interval_ms: int = 2500,
        sdk_provider: Callable[[], Any] | None = None,
    ) -> None:
        if not speech_key or not speech_region:
            raise ValueError("Azure Speech key and region are required.")
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._language_tag = _language_tag(language)
        self._partial_interval_s = max(0.0, partial_interval_ms / 1000)
        self._sdk_provider = sdk_provider
        self._lock = threading.Lock()
        self._recognizer: Any | None = None
        self._push_stream: Any | None = None
        self._final_segments: list[str] = []
        self._pending_partial: str | None = None
        self._partial_dirty = False
        self._last_partial_at = 0.0
        self._session_finished = threading.Event()
        self._cancellation_error: str | None = None

    async def start_session(self) -> None:
        await asyncio.to_thread(self._start_session)

    def _start_session(self) -> None:
        speechsdk = self._sdk()
        config = speechsdk.SpeechConfig(
            subscription=self._speech_key,
            region=self._speech_region,
        )
        config.speech_recognition_language = self._language_tag
        stream_format = speechsdk.audio.AudioStreamFormat(
            samples_per_second=_SAMPLE_RATE,
            bits_per_sample=_BITS_PER_SAMPLE,
            channels=_CHANNELS,
        )
        push_stream = speechsdk.audio.PushAudioInputStream(stream_format=stream_format)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=config,
            audio_config=speechsdk.audio.AudioConfig(stream=push_stream),
        )

        def on_recognizing(event: Any) -> None:
            text = (event.result.text or "").strip()
            if not text:
                return
            with self._lock:
                self._pending_partial = text
                self._partial_dirty = True

        def on_recognized(event: Any) -> None:
            reason = getattr(event.result, "reason", None)
            recognized_speech = getattr(
                speechsdk, "ResultReason", None
            )
            expected = getattr(recognized_speech, "RecognizedSpeech", None)
            if expected is not None and reason != expected:
                return
            text = (event.result.text or "").strip()
            if not text:
                return
            with self._lock:
                self._final_segments.append(text)
                self._pending_partial = None
                self._partial_dirty = False

        def on_canceled(event: Any) -> None:
            details = getattr(getattr(event, "result", None), "cancellation_details", None)
            error_details = getattr(details, "error_details", None)
            with self._lock:
                self._cancellation_error = error_details or "Azure recognition canceled"
            self._session_finished.set()

        recognizer.recognizing.connect(on_recognizing)
        recognizer.recognized.connect(on_recognized)
        recognizer.canceled.connect(on_canceled)
        recognizer.session_stopped.connect(lambda _event: self._session_finished.set())

        recognizer.start_continuous_recognition_async().get()
        self._push_stream = push_stream
        self._recognizer = recognizer

    async def append_audio(self, audio_bytes: bytes) -> None:
        stream = self._push_stream
        if stream is None:
            return
        await asyncio.to_thread(stream.write, audio_bytes)

    async def process_audio_chunk(self, audio_bytes: bytes) -> TranscriptEvent | None:
        # Deferred-partials contract: buffer only; partials are emitted through
        # transcribe_partial() so SDK callbacks never stall the audio consumer.
        await self.append_audio(audio_bytes)
        return None

    def partial_due(self) -> bool:
        if not self._partial_dirty:
            return False
        return time.monotonic() - self._last_partial_at >= self._partial_interval_s

    async def transcribe_partial(self) -> TranscriptEvent | None:
        with self._lock:
            text = self._composed_text_locked()
            self._last_partial_at = time.monotonic()
        if not text:
            return None
        return TranscriptEvent(
            type=TranscriptEventType.PARTIAL,
            text=text,
            language=self._language_tag,
            confidence=1.0,
            timestamp=datetime.now(timezone.utc),
        )

    async def finish_session(self) -> TranscriptEvent | None:
        await asyncio.to_thread(self._finish_session)
        with self._lock:
            text = " ".join(self._final_segments).strip()
            cancellation_error = self._cancellation_error
        if not text:
            if cancellation_error and self._pending_partial is None:
                logger.warning(
                    "Azure recognition canceled without a transcript.",
                    extra={"event": "azure_stt_canceled"},
                )
            return None
        return TranscriptEvent(
            type=TranscriptEventType.FINAL,
            text=text,
            language=self._language_tag,
            confidence=1.0,
            timestamp=datetime.now(timezone.utc),
        )

    def _finish_session(self) -> None:
        stream = self._push_stream
        recognizer = self._recognizer
        if stream is None or recognizer is None:
            return
        stream.close()
        try:
            recognizer.stop_continuous_recognition_async().get(timeout=_FINAL_TIMEOUT_S)
        except Exception as error:  # noqa: BLE001 - surfaced via empty transcript
            logger.warning(
                "Azure stop_continuous_recognition failed.",
                extra={"event": "azure_stt_stop_failed", "error": str(error)},
            )
        self._session_finished.wait(timeout=_FINAL_TIMEOUT_S)

    def _composed_text_locked(self) -> str:
        parts = [*self._final_segments]
        if self._pending_partial:
            parts.append(self._pending_partial)
        return " ".join(parts).strip()

    def _sdk(self) -> Any:
        if self._sdk_provider is not None:
            return self._sdk_provider()
        import azure.cognitiveservices.speech as speechsdk

        return speechsdk


class AzureStreamingSTTFactory(StreamingSTTFactory):
    def __init__(
        self,
        *,
        speech_key: str,
        speech_region: str,
        language: str = "vi",
        partial_interval_ms: int = 2500,
        sdk_provider: Callable[[], Any] | None = None,
    ) -> None:
        self._speech_key = speech_key
        self._speech_region = speech_region
        self._language = language
        self._partial_interval_ms = partial_interval_ms
        self._sdk_provider = sdk_provider

    def create(self) -> AzureStreamingSTT:
        return self.create_for_language(None)

    def create_for_language(self, language: str | None) -> AzureStreamingSTT:
        return AzureStreamingSTT(
            speech_key=self._speech_key,
            speech_region=self._speech_region,
            language=language or self._language,
            partial_interval_ms=self._partial_interval_ms,
            sdk_provider=self._sdk_provider,
        )
