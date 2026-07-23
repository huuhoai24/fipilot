from __future__ import annotations

import asyncio
import math
from datetime import datetime, timezone
from threading import Lock
from typing import Any

from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)


PCM_SAMPLE_RATE = 16_000
PCM_SAMPLE_WIDTH_BYTES = 2


class _FasterWhisperModelProvider:
    """Lazy shared model loader; no model is initialized per voice session."""

    def __init__(self, *, model_name: str, device: str, compute_type: str) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model: Any | None = None
        self._load_lock = Lock()
        self._inference_lock = Lock()

    def transcribe(
        self,
        audio: Any,
        language: str | None,
        hotwords: str | None = None,
    ) -> tuple[str, str, float]:
        model = self._get_model()
        with self._inference_lock:
            segments, info = model.transcribe(
                audio,
                language=language,
                beam_size=1,
                vad_filter=False,
                condition_on_previous_text=False,
                word_timestamps=False,
                hotwords=hotwords,
                initial_prompt=hotwords,
            )
            materialized = list(segments)

        text = " ".join(segment.text.strip() for segment in materialized).strip()
        detected_language = getattr(info, "language", None) or language or "unknown"
        if not materialized:
            return text, detected_language, 0.0
        average_log_probability = sum(
            float(getattr(segment, "avg_logprob", -5.0)) for segment in materialized
        ) / len(materialized)
        confidence = max(0.0, min(1.0, math.exp(average_log_probability)))
        return text, detected_language, confidence

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model
        with self._load_lock:
            if self._model is None:
                try:
                    from faster_whisper import WhisperModel
                except ImportError as error:
                    raise RuntimeError(
                        "Install backend/requirements-speech.txt to enable streaming STT."
                    ) from error
                self._model = WhisperModel(
                    self.model_name,
                    device=self.device,
                    compute_type=self.compute_type,
                )
        return self._model


class FasterWhisperStreamingSTT(StreamingSTT):
    def __init__(
        self,
        provider: _FasterWhisperModelProvider,
        *,
        language: str,
        partial_interval_ms: int,
        hotwords: str | None = None,
    ) -> None:
        self.provider = provider
        self.language = None if language.lower() == "auto" else language
        self.partial_interval_bytes = max(
            PCM_SAMPLE_WIDTH_BYTES,
            int(PCM_SAMPLE_RATE * PCM_SAMPLE_WIDTH_BYTES * partial_interval_ms / 1000),
        )
        self._audio = bytearray()
        self._last_partial_size = 0
        self.hotwords = hotwords

    async def start_session(self) -> None:
        self._audio.clear()
        self._last_partial_size = 0

    async def process_audio_chunk(
        self, audio_bytes: bytes
    ) -> TranscriptEvent | None:
        self._audio.extend(audio_bytes)
        if len(self._audio) - self._last_partial_size < self.partial_interval_bytes:
            return None
        self._last_partial_size = len(self._audio)
        return await self._transcribe(TranscriptEventType.PARTIAL)

    async def finish_session(self) -> TranscriptEvent | None:
        if not self._audio:
            return None
        try:
            return await self._transcribe(TranscriptEventType.FINAL)
        finally:
            self._audio.clear()
            self._last_partial_size = 0

    async def _transcribe(
        self, event_type: TranscriptEventType
    ) -> TranscriptEvent | None:
        try:
            import numpy as np
        except ImportError as error:
            raise RuntimeError(
                "Install backend/requirements-speech.txt to enable streaming STT."
            ) from error

        pcm = np.frombuffer(bytes(self._audio), dtype=np.int16)
        audio = pcm.astype(np.float32) / 32768.0
        text, language, confidence = await asyncio.to_thread(
            self.provider.transcribe,
            audio,
            self.language,
            self.hotwords,
        )
        if not text:
            return None
        return TranscriptEvent(
            type=event_type,
            text=text,
            language=language,
            confidence=confidence,
            timestamp=datetime.now(timezone.utc),
        )


class FasterWhisperSTTFactory(StreamingSTTFactory):
    def __init__(
        self,
        *,
        model_name: str,
        device: str,
        compute_type: str,
        language: str,
        partial_interval_ms: int,
        vocabulary_profile: str = "auto",
        custom_hotwords: list[str] | None = None,
    ) -> None:
        self.provider = _FasterWhisperModelProvider(
            model_name=model_name,
            device=device,
            compute_type=compute_type,
        )
        self.language = language
        self.partial_interval_ms = partial_interval_ms
        from infrastructure.speech.stt.vocabulary import vocabulary_hotwords

        self.hotwords = vocabulary_hotwords(
            vocabulary_profile,
            custom_hotwords,
        ) or None

    def create(self) -> StreamingSTT:
        return FasterWhisperStreamingSTT(
            self.provider,
            language=self.language,
            partial_interval_ms=self.partial_interval_ms,
            hotwords=self.hotwords,
        )
