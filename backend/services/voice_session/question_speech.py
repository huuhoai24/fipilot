from __future__ import annotations

import asyncio
import re
import time
from contextlib import suppress
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from infrastructure.speech.tts.base import AudioChunk, StreamingTTS


EventPublisher = Callable[[], Awaitable[None]]
FormatPublisher = Callable[[AudioChunk], Awaitable[None]]
AudioPublisher = Callable[[bytes], Awaitable[None]]


class QuestionSentenceChunker:
    """Builds speakable chunks without cutting a partially streamed word."""

    _sentence_boundary = re.compile(r"^(.+?[.!?;:])(?=\s|$)", re.DOTALL)

    def __init__(self, *, min_words: int = 3, max_chars: int = 80) -> None:
        if min_words <= 0 or max_chars <= 0:
            raise ValueError("Question chunk limits must be positive.")
        self.min_words = min_words
        self.max_chars = max_chars
        self._buffer = ""

    def feed(self, delta: str) -> list[str]:
        chunks: list[str] = []
        if delta and delta[0].isspace() and self._word_count(self._buffer) >= self.min_words:
            self._emit_buffer(chunks)
        self._buffer += delta
        self._extract_boundaries(chunks)
        self._extract_oversized(chunks)
        return chunks

    def flush(self) -> list[str]:
        chunks: list[str] = []
        self._emit_buffer(chunks)
        return chunks

    def _extract_boundaries(self, chunks: list[str]) -> None:
        while True:
            match = self._sentence_boundary.match(self._buffer.lstrip())
            if match is None:
                return
            chunk = match.group(1).strip()
            if chunk:
                chunks.append(chunk)
            stripped = self._buffer.lstrip()
            self._buffer = stripped[match.end() :].lstrip()

    def _extract_oversized(self, chunks: list[str]) -> None:
        while len(self._buffer) > self.max_chars:
            split_at = self._buffer.rfind(" ", 0, self.max_chars + 1)
            if split_at <= 0:
                return
            chunk = self._buffer[:split_at].strip()
            if chunk:
                chunks.append(chunk)
            self._buffer = self._buffer[split_at + 1 :]

    def _emit_buffer(self, chunks: list[str]) -> None:
        chunk = self._buffer.strip()
        self._buffer = ""
        if chunk:
            chunks.append(chunk)

    @staticmethod
    def _word_count(text: str) -> int:
        return len(text.split())


@dataclass(frozen=True)
class QuestionSpeechMetrics:
    question_complete_time_ms: float | None
    tts_first_audio_time_ms: float | None


class QuestionSpeechStreamer:
    """Synthesizes queued question chunks while Gemini continues streaming."""

    def __init__(
        self,
        *,
        tts_service: StreamingTTS,
        chunker: QuestionSentenceChunker,
        queue_size: int,
        start_publisher: EventPublisher,
        format_publisher: FormatPublisher,
        audio_publisher: AudioPublisher,
        complete_publisher: EventPublisher,
        error_publisher: EventPublisher,
        first_audio_publisher: EventPublisher | None = None,
    ) -> None:
        if queue_size <= 0:
            raise ValueError("TTS queue size must be positive.")
        self.tts_service = tts_service
        self.chunker = chunker
        self.start_publisher = start_publisher
        self.format_publisher = format_publisher
        self.audio_publisher = audio_publisher
        self.complete_publisher = complete_publisher
        self.error_publisher = error_publisher
        self.first_audio_publisher = first_audio_publisher
        self._queue: asyncio.Queue[str | None] = asyncio.Queue(maxsize=queue_size)
        self._worker = asyncio.create_task(self._run())
        self._started = False
        self._failed = False
        self._audio_format: tuple[int, str] | None = None
        self._question_started_at = time.perf_counter()
        self._question_completed_at: float | None = None
        self._first_text_ready_at: float | None = None
        self._first_audio_at: float | None = None
        self._cancelled = False

    async def feed_text_delta(self, delta: str) -> None:
        if self._cancelled:
            return
        for chunk in self.chunker.feed(delta):
            await self._enqueue(chunk)

    def mark_question_complete(self) -> None:
        if self._question_completed_at is None:
            self._question_completed_at = time.perf_counter()

    async def finish(self) -> QuestionSpeechMetrics:
        if not self._cancelled:
            for chunk in self.chunker.flush():
                await self._enqueue(chunk)
            await self._queue.put(None)
            await self._worker
            if self._started:
                await self.complete_publisher()
        return QuestionSpeechMetrics(
            question_complete_time_ms=(
                (self._question_completed_at - self._question_started_at) * 1000
                if self._question_completed_at is not None
                else None
            ),
            tts_first_audio_time_ms=(
                (self._first_audio_at - self._first_text_ready_at) * 1000
                if (
                    self._first_audio_at is not None
                    and self._first_text_ready_at is not None
                )
                else None
            ),
        )

    async def cancel(self) -> None:
        self._cancelled = True
        if self._worker.done():
            with suppress(asyncio.CancelledError, Exception):
                await self._worker
            return
        self._worker.cancel()
        with suppress(asyncio.CancelledError):
            await self._worker

    async def _enqueue(self, text: str) -> None:
        if not self._started:
            self._started = True
            self._first_text_ready_at = time.perf_counter()
            await self.start_publisher()
        await self._queue.put(text)
        await asyncio.sleep(0)

    async def _run(self) -> None:
        while True:
            text = await self._queue.get()
            if text is None:
                return
            if self._failed:
                continue
            try:
                async for audio_chunk in self.tts_service.synthesize_stream(text):
                    current_format = (
                        audio_chunk.sample_rate,
                        audio_chunk.format,
                    )
                    if self._audio_format is None:
                        self._audio_format = current_format
                        await self.format_publisher(audio_chunk)
                    elif current_format != self._audio_format:
                        raise RuntimeError("TTS audio format changed mid-stream.")
                    if self._first_audio_at is None:
                        self._first_audio_at = time.perf_counter()
                        if self.first_audio_publisher is not None:
                            await self.first_audio_publisher()
                    await self.audio_publisher(audio_chunk.bytes)
            except Exception:
                self._failed = True
                await self.error_publisher()


class QuestionSpeechStreamerFactory:
    def __init__(
        self,
        *,
        tts_service: StreamingTTS,
        queue_size: int,
        chunk_min_words: int,
        chunk_max_chars: int,
    ) -> None:
        self.tts_service = tts_service
        self.queue_size = queue_size
        self.chunk_min_words = chunk_min_words
        self.chunk_max_chars = chunk_max_chars

    def create(
        self,
        *,
        start_publisher: EventPublisher,
        format_publisher: FormatPublisher,
        audio_publisher: AudioPublisher,
        complete_publisher: EventPublisher,
        error_publisher: EventPublisher,
        first_audio_publisher: EventPublisher | None = None,
    ) -> QuestionSpeechStreamer:
        return QuestionSpeechStreamer(
            tts_service=self.tts_service,
            chunker=QuestionSentenceChunker(
                min_words=self.chunk_min_words,
                max_chars=self.chunk_max_chars,
            ),
            queue_size=self.queue_size,
            start_publisher=start_publisher,
            format_publisher=format_publisher,
            audio_publisher=audio_publisher,
            complete_publisher=complete_publisher,
            error_publisher=error_publisher,
            first_audio_publisher=first_audio_publisher,
        )
