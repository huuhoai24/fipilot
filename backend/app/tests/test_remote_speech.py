from __future__ import annotations

import json
import unittest

from infrastructure.speech.remote import RemoteStreamingTTS


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


class RemoteSpeechTests(unittest.IsolatedAsyncioTestCase):
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
