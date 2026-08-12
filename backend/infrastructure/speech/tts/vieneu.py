from __future__ import annotations

import asyncio
import threading
import time
from collections.abc import AsyncIterator, Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

import numpy as np

from core.logging import get_logger
from infrastructure.speech.tts.base import AudioChunk, StreamingTTS


logger = get_logger(__name__)


class VieneuTTSError(RuntimeError):
    pass


@dataclass(frozen=True)
class VieneuWarmupMetrics:
    model_load_ms: float | None
    prewarm_ms: float
    performed: bool


class _VieneuModelProvider:
    def __init__(self, *, mode: str, device: str) -> None:
        self.mode = mode
        self.device = device
        self._model: Any | None = None
        self._lock = threading.Lock()
        self.model_load_ms: float | None = None

    def get_model(self) -> Any:
        if self._model is not None:
            return self._model
        with self._lock:
            if self._model is None:
                started_at = time.perf_counter()
                try:
                    from vieneu import Vieneu
                except ImportError as error:
                    raise VieneuTTSError(
                        "The vieneu package is required for speech synthesis."
                    ) from error
                self._model = Vieneu(mode=self.mode, device=self.device)
                self.model_load_ms = (time.perf_counter() - started_at) * 1000
                logger.info(
                    "Vieneu model loaded.",
                    extra={
                        "event": "tts_model_loaded",
                        "status": "ready",
                        "tts_model_load_ms": round(self.model_load_ms, 2),
                    },
                )
        return self._model


_END = object()


class VieneuStreamingTTS(StreamingTTS):
    """Lazy VieNeu-TTS adapter that emits 24 kHz PCM16 frames."""

    def __init__(
        self,
        *,
        mode: str = "v3turbo",
        device: str = "auto",
        voice: str | None = None,
        sample_rate: int = 24000,
        frame_duration_ms: int = 100,
        model_provider: Callable[[], Any] | None = None,
    ) -> None:
        if sample_rate <= 0 or frame_duration_ms <= 0:
            raise ValueError("TTS audio settings must be positive.")
        self.voice = voice
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        provider = _VieneuModelProvider(mode=mode, device=device)
        self._model_state = provider if model_provider is None else None
        self._model_provider = model_provider or provider.get_model
        self._executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="vieneu-tts",
        )
        self._synthesis_lock = asyncio.Lock()
        self._warmup_lock = asyncio.Lock()
        self._warmed = False

    async def synthesize_stream(self, text: str) -> AsyncIterator[AudioChunk]:
        normalized_text = text.strip()
        if not normalized_text:
            return

        loop = asyncio.get_running_loop()
        async with self._synthesis_lock:
            iterator = await loop.run_in_executor(
                self._executor,
                self._create_stream,
                normalized_text,
            )
            while True:
                item = await loop.run_in_executor(
                    self._executor,
                    self._next_or_end,
                    iterator,
                )
                if item is _END:
                    break
                for frame in self._pcm_frames(item):
                    yield AudioChunk(
                        bytes=frame,
                        sample_rate=self.sample_rate,
                    )

    async def warm_up(self) -> VieneuWarmupMetrics:
        if self._warmed:
            return VieneuWarmupMetrics(
                model_load_ms=self.model_load_ms,
                prewarm_ms=0.0,
                performed=False,
            )
        async with self._warmup_lock:
            if self._warmed:
                return VieneuWarmupMetrics(
                    model_load_ms=self.model_load_ms,
                    prewarm_ms=0.0,
                    performed=False,
                )
            started_at = time.perf_counter()
            async for _ in self.synthesize_stream("Xin chao."):
                pass
            self._warmed = True
            return VieneuWarmupMetrics(
                model_load_ms=self.model_load_ms,
                prewarm_ms=(time.perf_counter() - started_at) * 1000,
                performed=True,
            )

    def close(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)

    def _create_stream(self, text: str) -> Iterator[np.ndarray]:
        model = self._model_provider()
        kwargs: dict[str, Any] = {"apply_watermark": True}
        if self.voice:
            kwargs["voice"] = self.voice
        return iter(model.infer_stream(text, **kwargs))

    @property
    def model_load_ms(self) -> float | None:
        return self._model_state.model_load_ms if self._model_state else None

    @staticmethod
    def _next_or_end(iterator: Iterator[np.ndarray]) -> np.ndarray | object:
        try:
            return next(iterator)
        except StopIteration:
            return _END

    def _pcm_frames(self, waveform: np.ndarray) -> list[bytes]:
        audio = np.asarray(waveform, dtype=np.float32).reshape(-1)
        if not audio.size:
            return []
        model = self._model_provider()
        source_rate = int(getattr(model, "sample_rate", self.sample_rate))
        if source_rate != self.sample_rate:
            try:
                import soxr
            except ImportError as error:
                raise VieneuTTSError(
                    "The soxr package is required to resample VieNeu audio."
                ) from error
            audio = soxr.resample(
                audio,
                source_rate,
                self.sample_rate,
                quality="HQ",
            )

        pcm = (
            np.clip(audio, -1.0, 1.0) * 32767.0
        ).astype("<i2", copy=False)
        frame_samples = max(
            1,
            self.sample_rate * self.frame_duration_ms // 1000,
        )
        return [
            pcm[offset : offset + frame_samples].tobytes()
            for offset in range(0, pcm.size, frame_samples)
            if pcm[offset : offset + frame_samples].size
        ]
