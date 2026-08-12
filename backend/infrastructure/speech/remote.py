from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import Any
from urllib.parse import urlparse, urlunparse

from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from services.voice_session.audio_pipeline import AudioQueueFullError


JsonPublisher = Callable[[dict[str, Any]], Awaitable[None]]
EventCallback = Callable[[], Awaitable[None]]


def _inference_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    scheme = {"http": "ws", "https": "wss"}.get(parsed.scheme, parsed.scheme)
    path = parsed.path.rstrip("/") + "/internal/v1/inference"
    return urlunparse(parsed._replace(scheme=scheme, path=path))


def _headers(token: str | None) -> dict[str, str] | None:
    return {"Authorization": f"Bearer {token}"} if token else None


class RemoteStreamingTTS(StreamingTTS):
    def __init__(
        self,
        *,
        service_url: str,
        service_token: str | None,
        connector=None,
    ) -> None:
        self.url = _inference_url(service_url)
        self.service_token = service_token
        self.connector = connector

    async def synthesize_stream(self, text: str):
        connector = self.connector
        if connector is None:
            from websockets.asyncio.client import connect

            connector = connect
        async with connector(
            self.url,
            additional_headers=_headers(self.service_token),
            max_size=None,
        ) as websocket:
            await websocket.send(
                json.dumps({"type": "tts_synthesize", "text": text})
            )
            sample_rate: int | None = None
            audio_format: str | None = None
            while True:
                message = await websocket.recv()
                if isinstance(message, bytes):
                    if sample_rate is None or audio_format != "pcm":
                        raise RuntimeError(
                            "Speech service sent audio before its format."
                        )
                    yield AudioChunk(
                        bytes=message,
                        sample_rate=sample_rate,
                        format="pcm",
                    )
                    continue
                event = json.loads(message)
                if event.get("type") == "audio_format":
                    sample_rate = int(event["sample_rate"])
                    audio_format = event["format"]
                elif event.get("type") == "tts_complete":
                    return
                elif event.get("type") == "error":
                    raise RuntimeError("Remote speech synthesis failed.")


class RemoteAudioPipeline:
    _STOP = object()

    def __init__(
        self,
        *,
        service_url: str,
        service_token: str | None,
        queue_size: int,
        language: str | None,
        transcript_publisher: JsonPublisher,
        endpoint_callback: EventCallback | None,
        speech_started_callback: EventCallback | None,
        speech_end_callback: EventCallback | None,
        stt_final_callback: EventCallback | None,
        stt_started_callback: EventCallback | None = None,
        connector=None,
    ) -> None:
        self.url = _inference_url(service_url)
        self.service_token = service_token
        self.queue_size = queue_size
        self.language = language
        self.transcript_publisher = transcript_publisher
        self.endpoint_callback = endpoint_callback
        self.speech_started_callback = speech_started_callback
        self.speech_end_callback = speech_end_callback
        self.stt_started_callback = stt_started_callback
        self.stt_final_callback = stt_final_callback
        self.connector = connector
        self._connection_context = None
        self._websocket = None
        self._queue: asyncio.Queue[bytes | object] | None = None
        self._sender: asyncio.Task[None] | None = None
        self._reader: asyncio.Task[None] | None = None
        self._complete = asyncio.Event()
        self.dropped_chunks = 0

    async def start(self) -> None:
        if self._websocket is not None:
            raise RuntimeError("Remote audio pipeline is already active.")
        connector = self.connector
        if connector is None:
            from websockets.asyncio.client import connect

            connector = connect
        self._connection_context = connector(
            self.url,
            additional_headers=_headers(self.service_token),
            max_size=None,
        )
        self._websocket = await self._connection_context.__aenter__()
        start_event = {"type": "stt_start"}
        if self.language:
            start_event["language"] = self.language
        await self._websocket.send(json.dumps(start_event))
        started = json.loads(await self._websocket.recv())
        if started.get("type") != "stt_started":
            await self.close()
            raise RuntimeError("Remote speech recognition could not start.")
        queue: asyncio.Queue[bytes | object] = asyncio.Queue(
            maxsize=self.queue_size
        )
        websocket = self._websocket
        self._queue = queue
        self._complete.clear()
        self._sender = asyncio.create_task(self._send_audio(queue, websocket))
        self._reader = asyncio.create_task(self._read_events(websocket))

    def enqueue(self, audio_bytes: bytes) -> bool:
        """Buffer one PCM frame; returns False when it was dropped."""
        if self._queue is None:
            raise RuntimeError("Remote audio pipeline is not active.")
        try:
            self._queue.put_nowait(audio_bytes)
        except asyncio.QueueFull:
            self.dropped_chunks += 1
            return False
        return True

    async def finish(self) -> None:
        if self._queue is None or self._websocket is None:
            return
        await self._queue.join()
        if self.stt_started_callback:
            await self.stt_started_callback()
        await self._websocket.send(json.dumps({"type": "stt_finish"}))
        await self._complete.wait()
        await self.close()

    async def close(self) -> None:
        queue = self._queue
        sender = self._sender
        reader = self._reader
        self._queue = None
        self._sender = None
        self._reader = None
        if queue is not None and sender is not None and not sender.done():
            await queue.put(self._STOP)
            with suppress(asyncio.CancelledError):
                await sender
        if reader is not None and not reader.done():
            reader.cancel()
            with suppress(asyncio.CancelledError):
                await reader
        context = self._connection_context
        self._connection_context = None
        self._websocket = None
        if context is not None:
            await context.__aexit__(None, None, None)

    async def _send_audio(
        self,
        queue: asyncio.Queue[bytes | object],
        websocket,
    ) -> None:
        while True:
            item = await queue.get()
            try:
                if item is self._STOP:
                    return
                assert isinstance(item, bytes)
                await websocket.send(item)
            finally:
                queue.task_done()

    async def _read_events(self, websocket) -> None:
        async for message in websocket:
            if isinstance(message, bytes):
                continue
            event = json.loads(message)
            event_type = event.get("type")
            if event_type in {"transcript_partial", "transcript_final"}:
                await self.transcript_publisher(event)
            elif event_type == "speech_started" and self.speech_started_callback:
                await self.speech_started_callback()
            elif event_type == "speech_end" and self.speech_end_callback:
                await self.speech_end_callback()
            elif event_type == "stt_final" and self.stt_final_callback:
                await self.stt_final_callback()
            elif event_type == "endpoint" and self.endpoint_callback:
                await self.endpoint_callback()
            elif event_type == "stt_complete":
                self._complete.set()
                return


class RemoteAudioPipelineFactory:
    def __init__(
        self,
        *,
        service_url: str,
        service_token: str | None,
        queue_size: int,
        connector=None,
    ) -> None:
        self.service_url = service_url
        self.service_token = service_token
        self.queue_size = queue_size
        self.connector = connector

    def create(
        self,
        *,
        language: str | None = None,
        transcript_publisher: JsonPublisher,
        endpoint_callback: EventCallback | None = None,
        speech_started_callback: EventCallback | None = None,
        speech_end_callback: EventCallback | None = None,
        stt_started_callback: EventCallback | None = None,
        stt_final_callback: EventCallback | None = None,
    ) -> RemoteAudioPipeline:
        return RemoteAudioPipeline(
            service_url=self.service_url,
            service_token=self.service_token,
            queue_size=self.queue_size,
            language=language,
            transcript_publisher=transcript_publisher,
            endpoint_callback=endpoint_callback,
            speech_started_callback=speech_started_callback,
            speech_end_callback=speech_end_callback,
            stt_started_callback=stt_started_callback,
            stt_final_callback=stt_final_callback,
            connector=self.connector,
        )
