from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from threading import Lock
from typing import Any

from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEventType,
)
from services.voice_session.transcript_service import TranscriptPublisher, TranscriptService


PCM_SAMPLE_RATE = 16_000
PCM_SAMPLE_WIDTH_BYTES = 2
EndpointCallback = Callable[[], Awaitable[None]]
PipelineEventCallback = Callable[[], Awaitable[None]]


class AudioQueueFullError(RuntimeError):
    pass


@dataclass(frozen=True)
class VADFrameResult:
    is_speech: bool
    speech_started: bool = False
    speech_ended: bool = False


class VoiceActivityDetector(ABC):
    @abstractmethod
    async def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        raise NotImplementedError


class VoiceActivityDetectorFactory(ABC):
    @abstractmethod
    def create(self) -> VoiceActivityDetector:
        raise NotImplementedError


class _SileroModelProvider:
    def __init__(self) -> None:
        self._model: Any | None = None
        self._lock = Lock()

    def get_model(self) -> Any:
        if self._model is not None:
            return self._model
        with self._lock:
            if self._model is None:
                try:
                    from silero_vad import load_silero_vad
                except ImportError as error:
                    raise RuntimeError(
                        "Install backend/requirements-speech.txt to enable Silero VAD."
                    ) from error
                self._model = load_silero_vad(onnx=True)
        return self._model


class SileroVoiceActivityDetector(VoiceActivityDetector):
    def __init__(
        self,
        provider: _SileroModelProvider,
        *,
        threshold: float,
        min_silence_ms: int,
        speech_pad_ms: int,
    ) -> None:
        self.provider = provider
        self.threshold = threshold
        self.min_silence_ms = min_silence_ms
        self.speech_pad_ms = speech_pad_ms
        self._iterator: Any | None = None
        self._speaking = False

    async def reset(self) -> None:
        self._iterator = await asyncio.to_thread(self._create_iterator)
        self._speaking = False

    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        if len(audio_bytes) % PCM_SAMPLE_WIDTH_BYTES:
            raise ValueError("PCM16 audio chunk must contain complete samples.")
        if self._iterator is None:
            await self.reset()
        return await asyncio.to_thread(self._process, audio_bytes)

    def _create_iterator(self) -> Any:
        try:
            from silero_vad import VADIterator
        except ImportError as error:
            raise RuntimeError(
                "Install backend/requirements-speech.txt to enable Silero VAD."
            ) from error
        return VADIterator(
            self.provider.get_model(),
            threshold=self.threshold,
            sampling_rate=PCM_SAMPLE_RATE,
            min_silence_duration_ms=self.min_silence_ms,
            speech_pad_ms=self.speech_pad_ms,
        )

    def _process(self, audio_bytes: bytes) -> VADFrameResult:
        try:
            import numpy as np
            import torch
        except ImportError as error:
            raise RuntimeError(
                "Install backend/requirements-speech.txt to enable Silero VAD."
            ) from error

        samples = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        result = self._iterator(torch.from_numpy(samples), return_seconds=False) or {}
        started = "start" in result
        ended = "end" in result
        if started:
            self._speaking = True
        is_speech = self._speaking
        if ended:
            self._speaking = False
        return VADFrameResult(
            is_speech=is_speech,
            speech_started=started,
            speech_ended=ended,
        )


class SileroVADFactory(VoiceActivityDetectorFactory):
    def __init__(
        self,
        *,
        threshold: float,
        min_silence_ms: int,
        speech_pad_ms: int,
    ) -> None:
        self.provider = _SileroModelProvider()
        self.threshold = threshold
        self.min_silence_ms = min_silence_ms
        self.speech_pad_ms = speech_pad_ms

    def create(self) -> VoiceActivityDetector:
        return SileroVoiceActivityDetector(
            self.provider,
            threshold=self.threshold,
            min_silence_ms=self.min_silence_ms,
            speech_pad_ms=self.speech_pad_ms,
        )


class AudioPipeline:
    """Bounded in-memory PCM pipeline. Silence is never forwarded to STT."""

    _STOP = object()

    def __init__(
        self,
        *,
        stt: StreamingSTT,
        vad: VoiceActivityDetector,
        transcript_service: TranscriptService,
        queue_size: int,
        endpoint_callback: EndpointCallback | None = None,
        speech_started_callback: PipelineEventCallback | None = None,
        speech_end_callback: PipelineEventCallback | None = None,
        stt_final_callback: PipelineEventCallback | None = None,
    ) -> None:
        self.stt = stt
        self.vad = vad
        self.transcript_service = transcript_service
        self.queue_size = queue_size
        self.endpoint_callback = endpoint_callback
        self.speech_started_callback = speech_started_callback
        self.speech_end_callback = speech_end_callback
        self.stt_final_callback = stt_final_callback
        self._queue: asyncio.Queue[bytes | object] | None = None
        self._worker: asyncio.Task[None] | None = None
        self._endpoint_detected = False
        self._final_published = False

    async def start(self) -> None:
        if self._worker is not None and not self._worker.done():
            raise RuntimeError("Audio pipeline is already active.")
        self._queue = asyncio.Queue(maxsize=self.queue_size)
        self._endpoint_detected = False
        self._final_published = False
        await self.vad.reset()
        await self.stt.start_session()
        self._worker = asyncio.create_task(self._run())

    def enqueue(self, audio_bytes: bytes) -> None:
        if self._queue is None or self._worker is None or self._worker.done():
            raise RuntimeError("Audio pipeline is not active.")
        try:
            self._queue.put_nowait(audio_bytes)
        except asyncio.QueueFull as error:
            raise AudioQueueFullError("Audio processing queue is full.") from error

    async def finish(self) -> None:
        if self._queue is None or self._worker is None:
            return
        await self._queue.put(self._STOP)
        await self._worker
        if not self._final_published:
            await self._publish_final()
        if not self._endpoint_detected:
            self._endpoint_detected = True
            if self.endpoint_callback is not None:
                await self.endpoint_callback()
        self._queue = None
        self._worker = None

    async def close(self) -> None:
        worker = self._worker
        self._queue = None
        self._worker = None
        if worker is not None and not worker.done():
            worker.cancel()
            try:
                await worker
            except asyncio.CancelledError:
                pass

    async def _run(self) -> None:
        assert self._queue is not None
        while True:
            item = await self._queue.get()
            try:
                if item is self._STOP:
                    return
                if self._endpoint_detected:
                    continue
                audio_bytes = item
                assert isinstance(audio_bytes, bytes)
                vad_result = await self.vad.process_audio_chunk(audio_bytes)
                if (
                    vad_result.speech_started
                    and self.speech_started_callback is not None
                ):
                    await self.speech_started_callback()
                if vad_result.is_speech:
                    partial = await self.stt.process_audio_chunk(audio_bytes)
                    if partial is not None:
                        await self.transcript_service.publish(partial)
                if vad_result.speech_ended:
                    self._endpoint_detected = True
                    if self.speech_end_callback is not None:
                        await self.speech_end_callback()
                    await self._publish_final()
                    if self.endpoint_callback is not None:
                        await self.endpoint_callback()
                    return
            finally:
                self._queue.task_done()

    async def _publish_final(self) -> None:
        final = await self.stt.finish_session()
        self._final_published = True
        if self.stt_final_callback is not None:
            await self.stt_final_callback()
        if final is None:
            return
        if final.type != TranscriptEventType.FINAL:
            final = final.model_copy(update={"type": TranscriptEventType.FINAL})
        await self.transcript_service.publish(final)


class AudioPipelineFactory:
    def __init__(
        self,
        *,
        stt_factory: StreamingSTTFactory,
        vad_factory: VoiceActivityDetectorFactory,
        queue_size: int,
    ) -> None:
        self.stt_factory = stt_factory
        self.vad_factory = vad_factory
        self.queue_size = queue_size

    def create(
        self,
        *,
        transcript_publisher: TranscriptPublisher,
        endpoint_callback: EndpointCallback | None = None,
        speech_started_callback: PipelineEventCallback | None = None,
        speech_end_callback: PipelineEventCallback | None = None,
        stt_final_callback: PipelineEventCallback | None = None,
    ) -> AudioPipeline:
        return AudioPipeline(
            stt=self.stt_factory.create(),
            vad=self.vad_factory.create(),
            transcript_service=TranscriptService(transcript_publisher),
            queue_size=self.queue_size,
            endpoint_callback=endpoint_callback,
            speech_started_callback=speech_started_callback,
            speech_end_callback=speech_end_callback,
            stt_final_callback=stt_final_callback,
        )
