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


def _preload_torch_cuda() -> None:
    """Bind PyTorch's cuDNN before CTranslate2 binds its own.

    faster-whisper (CTranslate2) and VieNeu-TTS (PyTorch) each ship a copy of
    cuDNN. When CTranslate2 initialises CUDA first, loading PyTorch afterwards
    aborts the whole process with

        Could not load symbol cudnnGetLibConfig. Error code 127

    which killed the speech service mid-interview. Touching torch's CUDA context
    first makes both libraries share the symbols that are already resident.
    Verified on an RTX 3050 Ti: CTranslate2-first crashes, torch-first survives
    whisper -> TTS -> whisper.
    """
    try:
        import torch
    except ImportError:  # CPU-only install; nothing to reconcile.
        return
    try:
        if torch.cuda.is_available():
            torch.zeros(1, device="cuda")
    except Exception:  # pragma: no cover - depends on local CUDA runtime
        return


class _FasterWhisperModelProvider:
    """Lazy shared model loader; no model is initialized per voice session."""

    def __init__(self, *, model_name: str, device: str, compute_type: str) -> None:
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self._model: Any | None = None
        self._load_lock = Lock()
        self._inference_lock = Lock()

    def warm_up(self, language: str | None) -> None:
        """Load the model and run one tiny inference.

        Both the weight load and the first CUDA kernel launch are slow. Doing
        them here means the first real utterance is not competing with them
        while audio is arriving.
        """
        import numpy as np

        self.transcribe(
            np.zeros(PCM_SAMPLE_RATE // 2, dtype="float32"),
            language,
            None,
            beam_size=1,
        )

    def transcribe(
        self,
        audio: Any,
        language: str | None,
        hotwords: str | None = None,
        beam_size: int = 1,
    ) -> tuple[str, str, float]:
        model = self._get_model()
        with self._inference_lock:
            segments, info = model.transcribe(
                audio,
                language=language,
                beam_size=beam_size,
                vad_filter=False,
                condition_on_previous_text=False,
                word_timestamps=False,
                hotwords=hotwords,
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
                if "cuda" in self.device or self.device == "auto":
                    _preload_torch_cuda()
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
    supports_deferred_partials = True

    def __init__(
        self,
        provider: _FasterWhisperModelProvider,
        *,
        language: str,
        partial_interval_ms: int,
        hotwords: str | None = None,
        partial_max_audio_ms: int = 20_000,
        final_beam_size: int = 5,
    ) -> None:
        self.provider = provider
        self.language = None if language.lower() == "auto" else language
        self.partial_interval_bytes = max(
            PCM_SAMPLE_WIDTH_BYTES,
            int(PCM_SAMPLE_RATE * PCM_SAMPLE_WIDTH_BYTES * partial_interval_ms / 1000),
        )
        # Every partial re-transcribes the whole utterance, so its cost grows with
        # utterance length. Past this much buffered speech, stop spending GPU on
        # partials and save it for the final transcript.
        self.partial_max_audio_bytes = max(
            self.partial_interval_bytes,
            int(PCM_SAMPLE_RATE * PCM_SAMPLE_WIDTH_BYTES * partial_max_audio_ms / 1000),
        )
        self.final_beam_size = max(1, final_beam_size)
        self._audio = bytearray()
        self._last_partial_size = 0
        self.hotwords = hotwords

    async def start_session(self) -> None:
        self._audio.clear()
        self._last_partial_size = 0

    async def append_audio(self, audio_bytes: bytes) -> None:
        self._audio.extend(audio_bytes)

    def partial_due(self) -> bool:
        if len(self._audio) > self.partial_max_audio_bytes:
            return False
        return len(self._audio) - self._last_partial_size >= self.partial_interval_bytes

    async def transcribe_partial(self) -> TranscriptEvent | None:
        # Claim the interval up front so concurrent callers cannot pile up.
        self._last_partial_size = len(self._audio)
        return await self._transcribe(TranscriptEventType.PARTIAL)

    async def process_audio_chunk(
        self, audio_bytes: bytes
    ) -> TranscriptEvent | None:
        await self.append_audio(audio_bytes)
        if not self.partial_due():
            return None
        return await self.transcribe_partial()

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
        # Partials are throwaway previews, so keep them greedy and cheap. The
        # final transcript is what gets scored, so give it a real beam search.
        beam_size = (
            self.final_beam_size
            if event_type == TranscriptEventType.FINAL
            else 1
        )
        text, language, confidence = await asyncio.to_thread(
            self.provider.transcribe,
            audio,
            self.language,
            self.hotwords,
            beam_size,
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
        partial_max_audio_ms: int = 20_000,
        final_beam_size: int = 5,
    ) -> None:
        self.provider = _FasterWhisperModelProvider(
            model_name=model_name,
            device=device,
            compute_type=compute_type,
        )
        self.language = language
        self.partial_interval_ms = partial_interval_ms
        self.partial_max_audio_ms = partial_max_audio_ms
        self.final_beam_size = final_beam_size
        from infrastructure.speech.stt.vocabulary import vocabulary_hotwords

        self.hotwords = vocabulary_hotwords(
            vocabulary_profile,
            custom_hotwords,
        ) or None

    def warm_up(self) -> None:
        self.provider.warm_up(None if self.language.lower() == "auto" else self.language)

    def create(self) -> StreamingSTT:
        return FasterWhisperStreamingSTT(
            self.provider,
            language=self.language,
            partial_interval_ms=self.partial_interval_ms,
            hotwords=self.hotwords,
            partial_max_audio_ms=self.partial_max_audio_ms,
            final_beam_size=self.final_beam_size,
        )
