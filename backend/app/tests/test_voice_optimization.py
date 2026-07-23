from __future__ import annotations

import unittest

from services.voice_session.manager import VoiceSessionManager
from services.voice_session.metrics import VoiceLatencyRegistry
from services.voice_session.schemas import VoiceSessionStatus


class VoiceLatencyTests(unittest.TestCase):
    def test_latency_registry_tracks_internal_milestones_without_content(self):
        times = iter([1.0, 1.2, 2.0, 2.4, 2.7])
        registry = VoiceLatencyRegistry(clock=lambda: next(times))
        registry.start_turn("session-1", "user-1")
        registry.mark("session-1", "user-1", "speech_end_time")
        registry.mark("session-1", "user-1", "stt_final_time")
        registry.mark("session-1", "user-1", "evaluation_start")
        registry.mark("session-1", "user-1", "question_first_token")
        registry.mark("session-1", "user-1", "tts_first_audio")

        snapshot = registry.snapshot("session-1", "user-1")

        self.assertIsNotNone(snapshot)
        self.assertEqual(
            snapshot.durations_ms(),
            {
                "speech_to_stt_final_ms": 200.0,
                "stt_to_evaluation_start_ms": 800.0,
                "evaluation_to_question_first_token_ms": 400.0,
                "question_to_tts_first_audio_ms": 300.0,
                "speech_to_tts_first_audio_ms": 1700.0,
            },
        )
        with self.assertLogs(
            "services.voice_session.metrics", level="INFO"
        ) as logs:
            registry.log_summary("session-1", "user-1")
        output = " ".join(logs.output)
        self.assertNotIn("audio", output.lower())
        self.assertNotIn("transcript", output.lower())
        self.assertNotIn("prompt", output.lower())


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
        self.assertAlmostEqual(analytics.speaking_duration_ms, 1200.0)
