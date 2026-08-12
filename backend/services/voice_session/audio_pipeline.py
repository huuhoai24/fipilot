from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from contextlib import suppress
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
SILERO_FRAME_SAMPLES = 512
SILERO_FRAME_BYTES = SILERO_FRAME_SAMPLES * PCM_SAMPLE_WIDTH_BYTES
# Drain up to 256 ms from an existing backlog in one thread hop. Live audio is
# still processed immediately when the queue contains only one browser frame.
VAD_BATCH_BYTES = SILERO_FRAME_BYTES * 8
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

    async def process_audio_batch(
        self,
        audio_chunks: list[bytes],
    ) -> list[VADFrameResult]:
        return [
            await self.process_audio_chunk(audio_bytes)
            for audio_bytes in audio_chunks
        ]


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
        self._pending_audio = bytearray()

    async def reset(self) -> None:
        self._iterator = await asyncio.to_thread(self._create_iterator)
        self._speaking = False
        self._pending_audio.clear()

    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        if len(audio_bytes) % PCM_SAMPLE_WIDTH_BYTES:
            raise ValueError("PCM16 audio chunk must contain complete samples.")
        if self._iterator is None:
            await self.reset()
        return await asyncio.to_thread(self._process, audio_bytes)

    async def process_audio_batch(
        self,
        audio_chunks: list[bytes],
    ) -> list[VADFrameResult]:
        if any(len(chunk) % PCM_SAMPLE_WIDTH_BYTES for chunk in audio_chunks):
            raise ValueError("PCM16 audio chunk must contain complete samples.")
        if self._iterator is None:
            await self.reset()
        return await asyncio.to_thread(
            lambda: [self._process(chunk) for chunk in audio_chunks]
        )

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
        self._pending_audio.extend(audio_bytes)
        speech_started = False
        speech_ended = False
        is_speech = False
        processed_frame = False

        while len(self._pending_audio) >= SILERO_FRAME_BYTES:
            frame = bytes(self._pending_audio[:SILERO_FRAME_BYTES])
            del self._pending_audio[:SILERO_FRAME_BYTES]
            result = self._process_frame(frame)
            processed_frame = True
            speech_started = speech_started or result.speech_started
            speech_ended = speech_ended or result.speech_ended
            is_speech = is_speech or result.is_speech

        return VADFrameResult(
            is_speech=is_speech or (not processed_frame and self._speaking),
            speech_started=speech_started,
            speech_ended=speech_ended,
        )

    def _process_frame(self, audio_bytes: bytes) -> VADFrameResult:
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
        stt_started_callback: PipelineEventCallback | None = None,
        stt_final_callback: PipelineEventCallback | None = None,
        auto_endpoint: bool = True,
        publish_partials: bool = True,
    ) -> None:
        self.stt = stt
        self.vad = vad
        self.transcript_service = transcript_service
        self.queue_size = queue_size
        self.endpoint_callback = endpoint_callback
        self.speech_started_callback = speech_started_callback
        self.speech_end_callback = speech_end_callback
        self.stt_started_callback = stt_started_callback
        self.stt_final_callback = stt_final_callback
        self.auto_endpoint = auto_endpoint
        self.publish_partials = publish_partials
        self._queue: asyncio.Queue[bytes | object] | None = None
        self._worker: asyncio.Task[None] | None = None
        self._partial_task: asyncio.Task[None] | None = None
        self._endpoint_detected = False
        self._final_published = False
        self.dropped_chunks = 0

    async def start(self) -> None:
        if self._worker is not None and not self._worker.done():
            raise RuntimeError("Audio pipeline is already active.")
        self._queue = asyncio.Queue(maxsize=self.queue_size)
        self._endpoint_detected = False
        self._final_published = False
        self.dropped_chunks = 0
        await self._cancel_partial()
        await self.vad.reset()
        await self.stt.start_session()
        self._worker = asyncio.create_task(self._run())

    def enqueue(self, audio_bytes: bytes) -> bool:
        """Buffer one PCM frame.

        Returns False when the frame was dropped because the queue is full.
        Dropping a frame degrades one utterance; raising here used to tear down
        the whole WebSocket and end the interview, which is far worse.
        """
        if self._queue is None or self._worker is None or self._worker.done():
            raise RuntimeError("Audio pipeline is not active.")
        try:
            self._queue.put_nowait(audio_bytes)
        except asyncio.QueueFull:
            self.dropped_chunks += 1
            return False
        return True

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
        await self._cancel_partial()
        if worker is not None and not worker.done():
            worker.cancel()
            try:
                await worker
            except asyncio.CancelledError:
                pass

    async def _consume_speech(self, audio_bytes: bytes) -> None:
        """Buffer speech audio and emit partials without stalling the consumer."""
        if not self.stt.supports_deferred_partials:
            partial = await self.stt.process_audio_chunk(audio_bytes)
            if partial is not None:
                await self.transcript_service.publish(partial)
            return

        await self.stt.append_audio(audio_bytes)
        if not self.publish_partials:
            return
        if not self.stt.partial_due():
            return
        if self._partial_task is not None and not self._partial_task.done():
            # Inference is still busy. Skip this partial instead of queueing
            # behind it: a backlog of partials is what used to starve the
            # consumer and overflow the audio queue.
            return
        self._partial_task = asyncio.create_task(self._emit_partial())

    async def _emit_partial(self) -> None:
        try:
            partial = await self.stt.transcribe_partial()
        except Exception:
            return
        if partial is None or self._endpoint_detected or self._final_published:
            return
        await self.transcript_service.publish(partial)

    async def _cancel_partial(self) -> None:
        task = self._partial_task
        self._partial_task = None
        if task is not None and not task.done():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    async def _run(self) -> None:
        # Bind the queue locally: close() clears self._queue while this task may
        # still be inside the loop, so re-reading the attribute in `finally`
        # would raise AttributeError on every shutdown.
        queue = self._queue
        assert queue is not None
        while True:
            item = await queue.get()
            consumed_items = 1
            try:
                if item is self._STOP:
                    return
                if self._endpoint_detected:
                    continue
                assert isinstance(item, bytes)
                batch = [item]
                batch_size = len(item)
                stop_after_batch = False
                while batch_size < VAD_BATCH_BYTES:
                    try:
                        pending = queue.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    consumed_items += 1
                    if pending is self._STOP:
                        stop_after_batch = True
                        break
                    assert isinstance(pending, bytes)
                    batch.append(pending)
                    batch_size += len(pending)

                vad_results = await self.vad.process_audio_batch(batch)
                if len(vad_results) != len(batch):
                    raise RuntimeError("VAD batch result count does not match audio input.")
                for audio_bytes, vad_result in zip(batch, vad_results, strict=True):
                    if (
                        vad_result.speech_started
                        and self.speech_started_callback is not None
                    ):
                        await self.speech_started_callback()
                    if vad_result.is_speech:
                        await self._consume_speech(audio_bytes)
                    if vad_result.speech_ended and self.auto_endpoint:
                        self._endpoint_detected = True
                        if self.speech_end_callback is not None:
                            await self.speech_end_callback()
                        await self._publish_final()
                        if self.endpoint_callback is not None:
                            await self.endpoint_callback()
                        return
                if stop_after_batch:
                    return
            finally:
                for _ in range(consumed_items):
                    queue.task_done()

    async def _publish_final(self) -> None:
        # Stop any in-flight partial first so a stale partial can never be
        # published after the final transcript.
        await self._cancel_partial()
        if self.stt_started_callback is not None:
            await self.stt_started_callback()
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
        auto_endpoint: bool = False,
        publish_partials: bool = False,
    ) -> None:
        self.stt_factory = stt_factory
        self.vad_factory = vad_factory
        self.queue_size = queue_size
        self.auto_endpoint = auto_endpoint
        self.publish_partials = publish_partials

    def create(
        self,
        *,
        language: str | None = None,
        transcript_publisher: TranscriptPublisher,
        endpoint_callback: EndpointCallback | None = None,
        speech_started_callback: PipelineEventCallback | None = None,
        speech_end_callback: PipelineEventCallback | None = None,
        stt_started_callback: PipelineEventCallback | None = None,
        stt_final_callback: PipelineEventCallback | None = None,
    ) -> AudioPipeline:
        return AudioPipeline(
            stt=self.stt_factory.create_for_language(language),
            vad=self.vad_factory.create(),
            transcript_service=TranscriptService(transcript_publisher),
            queue_size=self.queue_size,
            endpoint_callback=endpoint_callback,
            speech_started_callback=speech_started_callback,
            speech_end_callback=speech_end_callback,
            stt_started_callback=stt_started_callback,
            stt_final_callback=stt_final_callback,
            auto_endpoint=self.auto_endpoint,
            publish_partials=self.publish_partials,
        )
