from __future__ import annotations

import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)
from infrastructure.speech.stt.faster_whisper import FasterWhisperStreamingSTT
from infrastructure.speech.stt.vocabulary import vocabulary_hotwords
from services.voice_session.audio_pipeline import (
    AudioPipelineFactory,
    VADFrameResult,
    VoiceActivityDetector,
    VoiceActivityDetectorFactory,
)
from services.voice_session.transcript_service import TranscriptService


def transcript(event_type: TranscriptEventType, text: str) -> TranscriptEvent:
    return TranscriptEvent(
        type=event_type,
        text=text,
        language="en",
        confidence=0.9,
        timestamp=datetime.now(timezone.utc),
    )


class MockStreamingSTT(StreamingSTT):
    def __init__(self) -> None:
        self.started = False
        self.received_chunks: list[bytes] = []
        self.finished = False

    async def start_session(self) -> None:
        self.started = True
        self.received_chunks.clear()
        self.finished = False

    async def process_audio_chunk(self, audio_bytes: bytes):
        self.received_chunks.append(audio_bytes)
        return transcript(TranscriptEventType.PARTIAL, "I worked with YOLO")

    async def finish_session(self):
        self.finished = True
        if not self.received_chunks:
            return None
        return transcript(
            TranscriptEventType.FINAL,
            "I worked with YOLOv8 on a detection service.",
        )


class MockSTTFactory(StreamingSTTFactory):
    def __init__(self) -> None:
        self.instances: list[MockStreamingSTT] = []

    def create(self) -> StreamingSTT:
        instance = MockStreamingSTT()
        self.instances.append(instance)
        return instance


class MockVAD(VoiceActivityDetector):
    def __init__(self) -> None:
        self.calls = 0
        self.reset_called = False

    async def reset(self) -> None:
        self.calls = 0
        self.reset_called = True

    async def process_audio_chunk(self, audio_bytes: bytes) -> VADFrameResult:
        self.calls += 1
        if self.calls == 1:
            return VADFrameResult(is_speech=False)
        if self.calls == 2:
            return VADFrameResult(is_speech=True, speech_started=True)
        return VADFrameResult(is_speech=True, speech_ended=True)


class MockVADFactory(VoiceActivityDetectorFactory):
    def __init__(self) -> None:
        self.instances: list[MockVAD] = []

    def create(self) -> VoiceActivityDetector:
        instance = MockVAD()
        self.instances.append(instance)
        return instance


class VoiceAudioPipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_faster_whisper_session_uses_injected_model_provider(self):
        class MockModelProvider:
            def __init__(self) -> None:
                self.calls = 0

            def transcribe(self, audio, language, hotwords):
                self.calls += 1
                self.assert_audio_size = len(audio)
                self.hotwords = hotwords
                return "mocked transcript", language or "en", 0.88

        provider = MockModelProvider()
        stt = FasterWhisperStreamingSTT(
            provider,  # type: ignore[arg-type]
            language="en",
            partial_interval_ms=1,
        )
        await stt.start_session()
        partial = await stt.process_audio_chunk(b"\x01\x00" * 32)
        final = await stt.finish_session()

        self.assertIsNotNone(partial)
        self.assertEqual(partial.type, TranscriptEventType.PARTIAL)
        self.assertIsNotNone(final)
        self.assertEqual(final.type, TranscriptEventType.FINAL)
        self.assertEqual(final.text, "mocked transcript")
        self.assertEqual(provider.calls, 2)
        self.assertIsNone(provider.hotwords)

    async def test_faster_whisper_receives_technical_vocabulary_hotwords(self):
        class MockModelProvider:
            def transcribe(self, audio, language, hotwords):
                self.hotwords = hotwords
                return "FastAPI on Kubernetes", "en", 0.9

        hotwords = vocabulary_hotwords("backend", ["Kubernetes"])
        provider = MockModelProvider()
        stt = FasterWhisperStreamingSTT(
            provider,  # type: ignore[arg-type]
            language="en",
            partial_interval_ms=1,
            hotwords=hotwords,
        )
        await stt.start_session()
        await stt.process_audio_chunk(b"\x01\x00" * 32)

        self.assertIn("Backend", provider.hotwords)
        self.assertIn("FastAPI", provider.hotwords)
        self.assertIn("Kubernetes", provider.hotwords)

    def test_vocabulary_profiles_cover_supported_technical_roles(self):
        combined = vocabulary_hotwords("auto")

        for term in (
            "AI Engineer",
            "Backend",
            "Frontend",
            "Data Engineer",
            "DevOps",
        ):
            self.assertIn(term, combined)

    async def test_vad_removes_silence_and_publishes_partial_and_final_transcripts(self):
        stt_factory = MockSTTFactory()
        vad_factory = MockVADFactory()
        published: list[dict] = []
        endpoint_count = 0

        async def publisher(event: dict) -> None:
            published.append(event)

        async def endpoint() -> None:
            nonlocal endpoint_count
            endpoint_count += 1

        pipeline = AudioPipelineFactory(
            stt_factory=stt_factory,
            vad_factory=vad_factory,
            queue_size=4,
        ).create(
            transcript_publisher=publisher,
            endpoint_callback=endpoint,
        )

        silence = b"\x00\x00" * 512
        speech_start = b"\x01\x00" * 512
        speech_end = b"\x02\x00" * 512
        with patch("builtins.open", side_effect=AssertionError("audio must not be persisted")):
            await pipeline.start()
            pipeline.enqueue(silence)
            pipeline.enqueue(speech_start)
            pipeline.enqueue(speech_end)
            await pipeline.finish()

        stt = stt_factory.instances[0]
        self.assertTrue(vad_factory.instances[0].reset_called)
        self.assertEqual(stt.received_chunks, [speech_start, speech_end])
        self.assertNotIn(silence, stt.received_chunks)
        self.assertTrue(stt.finished)
        self.assertEqual(endpoint_count, 1)
        self.assertIn("transcript_partial", [event["type"] for event in published])
        self.assertEqual(published[-1]["type"], "transcript_final")
        self.assertEqual(
            published[-1]["text"],
            "I worked with YOLOv8 on a detection service.",
        )

    async def test_transcript_publisher_does_not_log_transcript_content(self):
        published: list[dict] = []

        async def publisher(event: dict) -> None:
            published.append(event)

        service = TranscriptService(publisher)
        with self.assertNoLogs(level="INFO"):
            result = await service.publish(
                transcript(TranscriptEventType.FINAL, "private candidate answer")
            )
        self.assertTrue(result)
        self.assertEqual(published[0]["type"], "transcript_final")

    async def test_empty_transcript_is_not_published(self):
        published: list[dict] = []

        async def publisher(event: dict) -> None:
            published.append(event)

        service = TranscriptService(publisher)
        result = await service.publish(transcript(TranscriptEventType.FINAL, "   "))
        self.assertFalse(result)
        self.assertEqual(published, [])


if __name__ == "__main__":
    unittest.main()
