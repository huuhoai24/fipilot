from __future__ import annotations

import asyncio
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch

from infrastructure.speech.stt.base import (
    StreamingSTT,
    StreamingSTTFactory,
    TranscriptEvent,
    TranscriptEventType,
)
from infrastructure.speech.stt.faster_whisper import (
    FasterWhisperStreamingSTT,
    _FasterWhisperModelProvider,
)
from infrastructure.speech.stt.vocabulary import vocabulary_hotwords
from services.voice_session.audio_pipeline import (
    AudioPipelineFactory,
    SileroVoiceActivityDetector,
    VADFrameResult,
    VoiceActivityDetector,
    VoiceActivityDetectorFactory,
)
from services.voice_session.manager import VoiceSessionManager
from services.voice_session.schemas import VoiceSessionStatus
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
    async def test_empty_stt_final_returns_to_listening_without_submission(self):
        listening_again = asyncio.Event()
        published_states: list[VoiceSessionStatus] = []
        submitted_answers: list[str] = []

        class EmptyFinalSTT(MockStreamingSTT):
            async def process_audio_chunk(self, audio_bytes: bytes):
                self.received_chunks.append(audio_bytes)
                return None

            async def finish_session(self):
                self.finished = True
                return None

        class EmptyFinalSTTFactory(StreamingSTTFactory):
            def create(self) -> StreamingSTT:
                return EmptyFinalSTT()

        async def publish_state(state: VoiceSessionStatus) -> None:
            published_states.append(state)
            if state == VoiceSessionStatus.WAITING_FOR_USER:
                listening_again.set()

        async def submit_answer(answer: str) -> None:
            submitted_answers.append(answer)

        manager = VoiceSessionManager(
            max_chunk_bytes=2048,
            max_session_bytes=8192,
            pipeline_factory=AudioPipelineFactory(
                stt_factory=EmptyFinalSTTFactory(),
                vad_factory=MockVADFactory(),
                queue_size=4,
            ),
        )
        await manager.connect(
            "session-1",
            "user-1",
            transcript_publisher=lambda _event: asyncio.sleep(0),
            state_publisher=publish_state,
            final_transcript_callback=submit_answer,
        )
        await manager.start_listening("session-1", "user-1")

        for sequence, payload in enumerate(
            (
                b"\x00\x00" * 512,
                b"\x01\x00" * 512,
                b"\x02\x00" * 512,
            )
        ):
            await manager.announce_audio_chunk("session-1", "user-1", sequence)
            await manager.receive_audio_chunk(
                "session-1",
                "user-1",
                payload,
            )

        await manager.stop_listening("session-1", "user-1")
        await manager.finish_transcription("session-1", "user-1")
        await asyncio.wait_for(listening_again.wait(), timeout=1)

        self.assertEqual(published_states, [VoiceSessionStatus.WAITING_FOR_USER])
        self.assertEqual(submitted_answers, [])
        state = await manager.start_listening("session-1", "user-1")
        self.assertEqual(state.state, VoiceSessionStatus.USER_SPEAKING)
        await manager.disconnect("session-1", "user-1")

    async def test_slow_stt_final_keeps_processing_and_completes_once(self):
        final_started = asyncio.Event()
        release_final = asyncio.Event()
        published: list[dict] = []
        speech_end_count = 0
        stt_final_count = 0
        endpoint_count = 0

        class SlowFinalSTT(MockStreamingSTT):
            async def finish_session(self):
                final_started.set()
                await release_final.wait()
                return await super().finish_session()

        class SlowFinalSTTFactory(StreamingSTTFactory):
            def create(self) -> StreamingSTT:
                return SlowFinalSTT()

        async def on_speech_end() -> None:
            nonlocal speech_end_count
            speech_end_count += 1

        async def on_stt_final() -> None:
            nonlocal stt_final_count
            stt_final_count += 1

        async def on_endpoint() -> None:
            nonlocal endpoint_count
            endpoint_count += 1

        async def publish(payload: dict) -> None:
            published.append(payload)

        pipeline = AudioPipelineFactory(
            stt_factory=SlowFinalSTTFactory(),
            vad_factory=MockVADFactory(),
            queue_size=4,
            auto_endpoint=True,
            publish_partials=True,
        ).create(
            transcript_publisher=publish,
            speech_end_callback=on_speech_end,
            stt_final_callback=on_stt_final,
            endpoint_callback=on_endpoint,
        )

        await pipeline.start()
        pipeline.enqueue(b"\x00\x00" * 512)
        pipeline.enqueue(b"\x01\x00" * 512)
        pipeline.enqueue(b"\x02\x00" * 512)
        await asyncio.wait_for(final_started.wait(), timeout=1)

        self.assertEqual(speech_end_count, 1)
        self.assertEqual(stt_final_count, 0)
        self.assertEqual(endpoint_count, 0)
        self.assertNotIn("transcript_final", [event["type"] for event in published])

        finish_task = asyncio.create_task(pipeline.finish())
        release_final.set()
        await asyncio.wait_for(finish_task, timeout=1)

        self.assertEqual(stt_final_count, 1)
        self.assertEqual(endpoint_count, 1)
        self.assertEqual(
            [event["type"] for event in published].count("transcript_final"),
            1,
        )

    async def test_silero_vad_splits_arbitrary_pcm_chunks_into_512_sample_frames(self):
        frame_sizes: list[int] = []

        class FakeIterator:
            def __call__(self, samples, *, return_seconds):
                frame_sizes.append(samples.numel())
                if len(frame_sizes) == 1:
                    return {"start": 0}
                if len(frame_sizes) == 3:
                    return {"end": 1536}
                return {}

        detector = SileroVoiceActivityDetector(
            provider=object(),  # type: ignore[arg-type]
            threshold=0.5,
            min_silence_ms=900,
            speech_pad_ms=120,
        )
        detector._iterator = FakeIterator()

        fake_torch = SimpleNamespace(
            from_numpy=lambda samples: SimpleNamespace(
                numel=lambda: len(samples),
            )
        )
        with patch.dict("sys.modules", {"torch": fake_torch}):
            result = await detector.process_audio_chunk(b"\x01\x00" * 1600)
            await detector.process_audio_chunk(b"\x00\x00" * 448)

        self.assertEqual(frame_sizes, [512, 512, 512, 512])
        self.assertTrue(result.speech_started)
        self.assertTrue(result.speech_ended)
        self.assertTrue(result.is_speech)

    async def test_faster_whisper_session_uses_injected_model_provider(self):
        class MockModelProvider:
            def __init__(self) -> None:
                self.calls = 0

            def transcribe(self, audio, language, hotwords, beam_size=1):
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
            def transcribe(self, audio, language, hotwords, beam_size=1):
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

    def test_faster_whisper_does_not_duplicate_hotwords_as_initial_prompt(self):
        class MockWhisperModel:
            def __init__(self) -> None:
                self.kwargs = {}

            def transcribe(self, _audio, **kwargs):
                self.kwargs = kwargs
                segment = SimpleNamespace(text="FastAPI", avg_logprob=-0.1)
                return iter([segment]), SimpleNamespace(language="vi")

        provider = _FasterWhisperModelProvider(
            model_name="mock",
            device="cpu",
            compute_type="int8",
        )
        model = MockWhisperModel()
        provider._model = model

        provider.transcribe([0.0], "vi", "FastAPI Kubernetes", beam_size=2)

        self.assertEqual(model.kwargs["hotwords"], "FastAPI Kubernetes")
        self.assertNotIn("initial_prompt", model.kwargs)

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
            auto_endpoint=True,
            publish_partials=True,
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
