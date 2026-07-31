from __future__ import annotations

import time
from dataclasses import dataclass, fields

from core.logging import get_logger


logger = get_logger(__name__)


@dataclass
class VoiceLatencyMetrics:
    speech_end_time: float | None = None
    stt_final_time: float | None = None
    evaluation_completed_time: float | None = None
    question_generated_time: float | None = None
    tts_first_audio: float | None = None

    def durations_ms(self) -> dict[str, float]:
        pairs = {
            "speech_to_transcript_ms": (self.speech_end_time, self.stt_final_time),
            "transcript_to_evaluation_ms": (
                self.stt_final_time,
                self.evaluation_completed_time,
            ),
            "evaluation_to_question_ms": (
                self.evaluation_completed_time,
                self.question_generated_time,
            ),
            "question_to_tts_audio_ms": (
                self.question_generated_time,
                self.tts_first_audio,
            ),
            "total_turn_latency_ms": (
                self.speech_end_time,
                self.tts_first_audio,
            ),
        }
        return {
            name: round((end - start) * 1000, 2)
            for name, (start, end) in pairs.items()
            if start is not None and end is not None and end >= start
        }


class VoiceLatencyRegistry:
    """Keeps content-free timing data for active voice sessions only."""

    _MILESTONES = {field.name for field in fields(VoiceLatencyMetrics)}

    def __init__(self, *, clock=time.perf_counter) -> None:
        self._clock = clock
        self._sessions: dict[tuple[str, str], VoiceLatencyMetrics] = {}

    def start_turn(self, session_id: str, user_id: str) -> None:
        self._sessions[(user_id, session_id)] = VoiceLatencyMetrics()

    def mark(self, session_id: str, user_id: str, milestone: str) -> None:
        if milestone not in self._MILESTONES:
            raise ValueError(f"Unknown voice latency milestone: {milestone}")
        metrics = self._sessions.setdefault(
            (user_id, session_id),
            VoiceLatencyMetrics(),
        )
        if getattr(metrics, milestone) is None:
            setattr(metrics, milestone, self._clock())

    def snapshot(
        self, session_id: str, user_id: str
    ) -> VoiceLatencyMetrics | None:
        metrics = self._sessions.get((user_id, session_id))
        if metrics is None:
            return None
        return VoiceLatencyMetrics(**metrics.__dict__)

    def log_summary(self, session_id: str, user_id: str) -> None:
        metrics = self._sessions.get((user_id, session_id))
        if metrics is None:
            return
        durations = metrics.durations_ms()
        if not durations:
            return
        logger.debug(
            "Voice turn latency measured.",
            extra={
                "event": "voice_turn_latency",
                **durations,
            },
        )

    def remove(self, session_id: str, user_id: str) -> None:
        self._sessions.pop((user_id, session_id), None)
