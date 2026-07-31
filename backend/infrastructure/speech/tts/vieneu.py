from __future__ import annotations

import asyncio
import threading
from collections.abc import AsyncIterator, Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import numpy as np

from infrastructure.speech.tts.base import AudioChunk, StreamingTTS


class VieneuTTSError(RuntimeError):
    pass


class _VieneuModelProvider:
    def __init__(self, *, mode: str, device: str) -> None:
        self.mode = mode
        self.device = device
        self._model: Any | None = None
        self._lock = threading.Lock()

    def get_model(self) -> Any:
        if self._model is not None:
            return self._model
        with self._lock:
            if self._model is None:
                try:
                    from vieneu import Vieneu
                except ImportError as error:
                    raise VieneuTTSError(
                        "The vieneu package is required for speech synthesis."
                    ) from error
                self._model = Vieneu(mode=self.mode, device=self.device)
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
        self._model_provider = model_provider or provider.get_model
        self._executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="vieneu-tts",
        )
        self._synthesis_lock = asyncio.Lock()

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

    async def warm_up(self) -> None:
        async for _ in self.synthesize_stream("Xin chao."):
            pass

    def close(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)

    def _create_stream(self, text: str) -> Iterator[np.ndarray]:
        model = self._model_provider()
        kwargs: dict[str, Any] = {"apply_watermark": True}
        if self.voice:
            kwargs["voice"] = self.voice
        return iter(model.infer_stream(text, **kwargs))

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
