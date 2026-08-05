from __future__ import annotations

import unittest
from unittest.mock import patch

from services.voice_session.manager import VoiceSessionManager
from services.voice_session.metrics import VoiceLatencyRegistry
from services.voice_session.schemas import VoiceSessionStatus


class VoiceLatencyTests(unittest.TestCase):
    def test_latency_registry_tracks_internal_milestones_without_content(self):
        times = iter([1.0, 1.1, 1.2, 2.0, 2.4, 2.7])
        registry = VoiceLatencyRegistry(
            clock=lambda: next(times),
            benchmark_mode=True,
        )
        registry.start_turn("session-1", "user-1")
        registry.mark("session-1", "user-1", "speech_end_time")
        registry.mark("session-1", "user-1", "stt_started_time")
        registry.mark("session-1", "user-1", "stt_final_time")
        registry.mark("session-1", "user-1", "evaluation_completed_time")
        registry.mark("session-1", "user-1", "question_generated_time")
        registry.mark("session-1", "user-1", "tts_first_audio")

        snapshot = registry.snapshot("session-1", "user-1")

        self.assertIsNotNone(snapshot)
        self.assertEqual(
            snapshot.durations_ms(),
            {
                "speech_to_stt_final_ms": 200.0,
                "audio_queue_drain_ms": 100.0,
                "stt_decode_ms": 100.0,
                "stt_to_evaluation_ms": 800.0,
                "evaluation_to_question_ms": 400.0,
                "question_to_tts_first_audio_ms": 300.0,
                "total_turn_latency_ms": 1700.0,
            },
        )
        with patch("services.voice_session.metrics.logger.info") as log:
            registry.log_summary("session-1", "user-1")
        log.assert_called_once()
        payload = log.call_args.kwargs["extra"]
        self.assertEqual(payload["event"], "speech_latency")
        self.assertEqual(payload["session_id"], "session-1")
        self.assertEqual(payload["status"], "complete")
        output = str(payload)
        self.assertNotIn("audio_bytes", output.lower())
        self.assertNotIn("transcript", output.lower())
        self.assertNotIn("prompt", output.lower())
        self.assertNotIn("candidate_answer", output.lower())

    def test_benchmark_logging_stays_at_debug_when_disabled(self):
        registry = VoiceLatencyRegistry(clock=lambda: 1.0)
        registry.start_turn("session-1", "user-1")
        registry.mark("session-1", "user-1", "speech_end_time")
        registry.mark("session-1", "user-1", "stt_final_time")

        with (
            patch("services.voice_session.metrics.logger.info") as info,
            patch("services.voice_session.metrics.logger.debug") as debug,
        ):
            registry.log_summary("session-1", "user-1")

        info.assert_not_called()
        debug.assert_called_once()
        self.assertEqual(
            debug.call_args.kwargs["extra"]["event"],
            "voice_turn_latency",
        )


class BargeInStateTests(unittest.IsolatedAsyncioTestCase):
    async def test_speech_start_during_ai_output_marks_interruption(self):
        cancelled = 0
        published: list[VoiceSessionStatus] = []

        async def on_barge_in() -> None:
            nonlocal cancelled
            cancelled += 1

        async def publish(state: VoiceSessionStatus) -> None:
            published.append(state)

        manager = VoiceSessionManager(
            max_chunk_bytes=8,
            max_session_bytes=32,
        )
        await manager.connect(
            "session-1",
            "user-1",
            state_publisher=publish,
            barge_in_callback=on_barge_in,
        )
        await manager.start_listening("session-1", "user-1")
        await manager.stop_listening("session-1", "user-1")
        await manager._handle_final_transcript(
            "session-1",
            "user-1",
            "automatic answer",
        )
        await manager.mark_answer_processing("session-1", "user-1")
        await manager.mark_ai_speaking("session-1", "user-1")
        await manager.start_barge_in_monitoring("session-1", "user-1")

        await manager._handle_speech_started("session-1", "user-1")

        self.assertEqual(cancelled, 1)
        self.assertIn(VoiceSessionStatus.INTERRUPTED, published)
        self.assertEqual(published[-1], VoiceSessionStatus.USER_SPEAKING)
        analytics = await manager.analytics_snapshot("session-1", "user-1")
        self.assertEqual(analytics.interruption_count, 1)
        state = await manager.finish_answer_submission(
            "session-1",
            "user-1",
            has_next_question=True,
        )
        self.assertEqual(state.state, VoiceSessionStatus.USER_SPEAKING)

    async def test_conversation_analytics_track_latency_and_speaking_duration(self):
        times = iter([10.0, 10.4, 10.8, 12.0])
        manager = VoiceSessionManager(
            max_chunk_bytes=8,
            max_session_bytes=32,
            clock=lambda: next(times),
        )
        await manager.connect("session-1", "user-1")
        await manager.start_listening("session-1", "user-1")

        await manager._handle_speech_started("session-1", "user-1")
        await manager._handle_speech_end("session-1", "user-1")

        analytics = await manager.analytics_snapshot("session-1", "user-1")
        self.assertAlmostEqual(analytics.response_latencies_ms[0], 400.0)
        self.assertAlmostEqual(analytics.speaking_duration_ms, 400.0)
