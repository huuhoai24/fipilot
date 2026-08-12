from __future__ import annotations

import unittest
import asyncio
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from infrastructure.speech.tts.base import AudioChunk, StreamingTTS
from infrastructure.speech.tts.vieneu import VieneuStreamingTTS
from services.voice_session.question_speech import (
    QuestionSentenceChunker,
    QuestionSpeechStreamer,
)


class MockVieneuModel:
    sample_rate = 48000

    def __init__(self) -> None:
        self.texts: list[str] = []

    def infer_stream(self, text: str, **kwargs):
        self.texts.append(text)
        yield np.full(4800, 0.25, dtype=np.float32)


class MockStreamingTTS(StreamingTTS):
    def __init__(self) -> None:
        self.texts: list[str] = []

    async def synthesize_stream(self, text: str):
        self.texts.append(text)
        yield AudioChunk(
            bytes=b"\x01\x00" * 16,
            sample_rate=24000,
        )


class BlockingStreamingTTS(StreamingTTS):
    async def synthesize_stream(self, text: str):
        yield AudioChunk(bytes=b"\x01\x00" * 16, sample_rate=24000)
        await __import__("asyncio").sleep(60)


async def _collect_audio(tts: StreamingTTS, text: str) -> list[AudioChunk]:
    return [chunk async for chunk in tts.synthesize_stream(text)]


class TTSStreamingTests(unittest.IsolatedAsyncioTestCase):
    async def test_vieneu_adapter_streams_resampled_pcm_without_model_download(self):
        model = MockVieneuModel()
        tts = VieneuStreamingTTS(
            model_provider=lambda: model,
            sample_rate=24000,
            frame_duration_ms=100,
        )
        try:
            with patch(
                "builtins.open",
                side_effect=AssertionError("audio must not be persisted"),
            ):
                chunks = [
                    chunk
                    async for chunk in tts.synthesize_stream(
                        "Explain YOLO architecture."
                    )
                ]
        finally:
            tts.close()

        self.assertEqual(model.texts, ["Explain YOLO architecture."])
        self.assertTrue(chunks)
        self.assertTrue(all(chunk.sample_rate == 24000 for chunk in chunks))
        self.assertTrue(all(chunk.format == "pcm" for chunk in chunks))
        self.assertTrue(all(len(chunk.bytes) % 2 == 0 for chunk in chunks))

    async def test_concurrent_prewarm_runs_only_one_internal_warmup(self):
        model = MockVieneuModel()
        tts = VieneuStreamingTTS(model_provider=lambda: model)
        try:
            metrics = await asyncio.gather(
                tts.warm_up(),
                tts.warm_up(),
                tts.warm_up(),
            )
        finally:
            tts.close()

        self.assertEqual(model.texts, ["Xin chao."])
        self.assertEqual(sum(item.performed for item in metrics), 1)
        self.assertTrue(all(item.prewarm_ms >= 0 for item in metrics))

    async def test_concurrent_first_requests_load_one_model_and_remain_serialized(self):
        constructor_calls = 0
        active_syntheses = 0
        max_active_syntheses = 0

        class ConcurrentModel:
            sample_rate = 24000

            def infer_stream(inner_self, text: str, **kwargs):
                nonlocal active_syntheses, max_active_syntheses
                active_syntheses += 1
                max_active_syntheses = max(max_active_syntheses, active_syntheses)
                try:
                    time.sleep(0.01)
                    yield np.full(2400, 0.25, dtype=np.float32)
                finally:
                    active_syntheses -= 1

        def create_model(*, mode: str, device: str):
            nonlocal constructor_calls
            constructor_calls += 1
            return ConcurrentModel()

        fake_vieneu = SimpleNamespace(Vieneu=create_model)
        with patch.dict(sys.modules, {"vieneu": fake_vieneu}):
            tts = VieneuStreamingTTS(mode="v3turbo", device="cpu")
            try:
                await asyncio.gather(
                    _collect_audio(tts, "First interviewer question."),
                    _collect_audio(tts, "Second interviewer question."),
                )
            finally:
                tts.close()

        self.assertEqual(constructor_calls, 1)
        self.assertEqual(max_active_syntheses, 1)
        self.assertIsNotNone(tts.model_load_ms)
        self.assertGreaterEqual(tts.model_load_ms, 0)

    async def test_failed_prewarm_retries_through_normal_lazy_synthesis(self):
        class RecoveringModel(MockVieneuModel):
            def infer_stream(self, text: str, **kwargs):
                self.texts.append(text)
                if len(self.texts) == 1:
                    raise RuntimeError("warmup failed")
                yield np.full(2400, 0.25, dtype=np.float32)

        model = RecoveringModel()
        tts = VieneuStreamingTTS(model_provider=lambda: model)
        try:
            with self.assertRaises(RuntimeError):
                await tts.warm_up()
            chunks = await _collect_audio(tts, "Real interviewer question.")
        finally:
            tts.close()

        self.assertEqual(model.texts, ["Xin chao.", "Real interviewer question."])
        self.assertTrue(chunks)

    def test_sentence_chunker_does_not_cut_partial_words(self):
        chunker = QuestionSentenceChunker(min_words=3, max_chars=80)

        self.assertEqual(chunker.feed("Can you explain"), [])
        self.assertEqual(
            chunker.feed(" YOLO architecture?"),
            ["Can you explain", "YOLO architecture?"],
        )
        self.assertEqual(chunker.flush(), [])

    async def test_question_speech_streams_audio_and_measures_first_chunk(self):
        tts = MockStreamingTTS()
        events: list[tuple[str, object | None]] = []

        async def event(name: str) -> None:
            events.append((name, None))

        async def audio_format(chunk: AudioChunk) -> None:
            events.append(("format", (chunk.sample_rate, chunk.format)))

        async def audio(payload: bytes) -> None:
            events.append(("audio", payload))

        streamer = QuestionSpeechStreamer(
            tts_service=tts,
            chunker=QuestionSentenceChunker(min_words=3, max_chars=80),
            queue_size=4,
            start_publisher=lambda: event("start"),
            format_publisher=audio_format,
            audio_publisher=audio,
            complete_publisher=lambda: event("complete"),
            error_publisher=lambda: event("error"),
        )

        with patch(
            "builtins.open",
            side_effect=AssertionError("audio must not be persisted"),
        ):
            await streamer.feed_text_delta("Can you explain")
            await streamer.feed_text_delta(" YOLO architecture?")
            streamer.mark_question_complete()
            metrics = await streamer.finish()

        self.assertEqual(
            tts.texts,
            ["Can you explain", "YOLO architecture?"],
        )
        self.assertEqual(events[0][0], "start")
        self.assertEqual(
            [name for name, _ in events].count("format"),
            1,
        )
        self.assertEqual(
            [name for name, _ in events].count("audio"),
            2,
        )
        self.assertEqual(events[-1][0], "complete")
        self.assertNotIn("error", [name for name, _ in events])
        self.assertIsNotNone(metrics.question_complete_time_ms)
        self.assertIsNotNone(metrics.tts_first_audio_time_ms)
        self.assertLess(metrics.tts_first_audio_time_ms, 1000)
        self.assertIsNotNone(metrics.tts_queue_ms)
        self.assertIsNotNone(metrics.tts_generation_ms)
        self.assertIsNotNone(metrics.tts_total_ms)
        self.assertGreaterEqual(metrics.tts_queue_ms, 0)
        self.assertGreaterEqual(metrics.tts_generation_ms, 0)
        self.assertGreaterEqual(metrics.tts_total_ms, metrics.tts_generation_ms)

    async def test_question_speech_cancellation_stops_output_without_completion(self):
        events: list[str] = []

        async def event(name: str) -> None:
            events.append(name)

        streamer = QuestionSpeechStreamer(
            tts_service=BlockingStreamingTTS(),
            chunker=QuestionSentenceChunker(min_words=1, max_chars=80),
            queue_size=2,
            start_publisher=lambda: event("start"),
            format_publisher=lambda chunk: event("format"),
            audio_publisher=lambda payload: event("audio"),
            complete_publisher=lambda: event("complete"),
            error_publisher=lambda: event("error"),
        )
        await streamer.feed_text_delta("Interrupt me.")
        for _ in range(20):
            if "audio" in events:
                break
            await __import__("asyncio").sleep(0)
        await streamer.cancel()
        await streamer.feed_text_delta("This must not be synthesized.")
        await streamer.finish()

        self.assertIn("audio", events)
        self.assertNotIn("complete", events)
        self.assertNotIn("error", events)


if __name__ == "__main__":
    unittest.main()
