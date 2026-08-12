from __future__ import annotations

import json
import unittest

from infrastructure.speech.remote import RemoteAudioPipelineFactory, RemoteStreamingTTS
from services.voice_session.manager import VoiceSessionManager


class FakeSpeechSocket:
    def __init__(self) -> None:
        self.sent: list[str] = []
        self.responses = [
            json.dumps({"type": "tts_start"}),
            json.dumps(
                {
                    "type": "audio_format",
                    "sample_rate": 24000,
                    "format": "pcm",
                }
            ),
            b"\x01\x00" * 4,
            json.dumps({"type": "tts_complete"}),
        ]

    async def send(self, payload: str) -> None:
        self.sent.append(payload)

    async def recv(self):
        return self.responses.pop(0)


class FakeConnectionContext:
    def __init__(self, socket: FakeSpeechSocket) -> None:
        self.socket = socket

    async def __aenter__(self):
        return self.socket

    async def __aexit__(self, exc_type, exc, traceback):
        return None


class FakeSTTSocket(FakeSpeechSocket):
    def __init__(self) -> None:
        super().__init__()
        self.responses = [json.dumps({"type": "stt_started"})]
        self._closed = __import__("asyncio").Event()

    def __aiter__(self):
        return self

    async def __anext__(self):
        await self._closed.wait()
        raise StopAsyncIteration


class RemoteSpeechTests(unittest.IsolatedAsyncioTestCase):
    async def test_remote_factory_accepts_voice_manager_lifecycle_callbacks(self):
        factory = RemoteAudioPipelineFactory(
            service_url="https://speech.internal/",
            service_token="secret",
            queue_size=4,
        )
        manager = VoiceSessionManager(
            max_chunk_bytes=2048,
            max_session_bytes=8192,
            pipeline_factory=factory,
        )

        await manager.connect(
            "session-1",
            "user-1",
            language="vi",
            transcript_publisher=lambda _event: __import__("asyncio").sleep(0),
        )
        await manager.disconnect("session-1", "user-1")

    async def test_remote_stt_sends_session_language_to_private_service(self):
        socket = FakeSTTSocket()

        def connector(_url: str, **_kwargs):
            return FakeConnectionContext(socket)

        factory = RemoteAudioPipelineFactory(
            service_url="https://speech.internal/",
            service_token="secret",
            queue_size=4,
            connector=connector,
        )
        pipeline = factory.create(
            language="vi",
            transcript_publisher=lambda _event: __import__("asyncio").sleep(0),
        )

        await pipeline.start()
        try:
            self.assertEqual(
                json.loads(socket.sent[0]),
                {"type": "stt_start", "language": "vi"},
            )
        finally:
            await pipeline.close()

    async def test_remote_tts_uses_private_boundary_and_streams_pcm(self):
        socket = FakeSpeechSocket()
        connector_calls: list[tuple[str, dict]] = []

        def connector(url: str, **kwargs):
            connector_calls.append((url, kwargs))
            return FakeConnectionContext(socket)

        service = RemoteStreamingTTS(
            service_url="https://speech.internal/",
            service_token="secret",
            connector=connector,
        )
        chunks = [
            chunk
            async for chunk in service.synthesize_stream("Private question")
        ]

        self.assertEqual(
            connector_calls[0][0],
            "wss://speech.internal/internal/v1/inference",
        )
        self.assertEqual(
            connector_calls[0][1]["additional_headers"],
            {"Authorization": "Bearer secret"},
        )
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].sample_rate, 24000)
        request = json.loads(socket.sent[0])
        self.assertEqual(request["type"], "tts_synthesize")


if __name__ == "__main__":
    unittest.main()
