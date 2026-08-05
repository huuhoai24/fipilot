from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from services.voice_session.audio_pipeline import (
    AudioPipeline,
    AudioPipelineFactory,
    AudioQueueFullError,
)
from services.voice_session.schemas import VoiceSessionState, VoiceSessionStatus
from services.voice_session.metrics import VoiceLatencyRegistry
from shared.schemas import VoiceAnalytics


class VoiceSessionProtocolError(ValueError):
    pass


class AudioChunkError(VoiceSessionProtocolError):
    def __init__(self, message: str, *, code: str = "invalid_audio_chunk") -> None:
        super().__init__(message)
        self.code = code


class VoiceSessionConflictError(VoiceSessionProtocolError):
    pass


TranscriptPublisher = Callable[[dict[str, Any]], Awaitable[None]]
StatePublisher = Callable[[VoiceSessionStatus], Awaitable[None]]
BargeInCallback = Callable[[], Awaitable[None]]
FinalTranscriptCallback = Callable[[str], Awaitable[None]]


@dataclass
class _ManagedVoiceSession:
    state: VoiceSessionState
    pipeline: AudioPipeline | None = None
    state_publisher: StatePublisher | None = None
    pending_sequence: int | None = None
    last_sequence: int = -1
    bytes_received: int = 0
    barge_in_monitoring: bool = False
    barge_in_callback: BargeInCallback | None = None
    final_transcript_callback: FinalTranscriptCallback | None = None
    analytics: VoiceAnalytics = field(default_factory=VoiceAnalytics)
    waiting_for_user_at: float | None = None
    user_speech_started_at: float | None = None
    dropped_chunks: int = 0
    late_chunks: int = 0


class VoiceSessionManager:
    """Owns bounded, ephemeral audio pipelines for active WebSocket sessions."""

    def __init__(
        self,
        *,
        max_chunk_bytes: int,
        max_session_bytes: int,
        pipeline_factory: AudioPipelineFactory | None = None,
        latency_registry: VoiceLatencyRegistry | None = None,
        clock=time.perf_counter,
    ) -> None:
        if max_chunk_bytes <= 0 or max_session_bytes < max_chunk_bytes:
            raise ValueError("Voice audio limits are invalid")
        self.max_chunk_bytes = max_chunk_bytes
        self.max_session_bytes = max_session_bytes
        self.pipeline_factory = pipeline_factory
        self.latency_registry = latency_registry or VoiceLatencyRegistry()
        self.clock = clock
        self._sessions: dict[tuple[str, str], _ManagedVoiceSession] = {}
        self._lock = asyncio.Lock()

    async def connect(
        self,
        session_id: str,
        user_id: str,
        *,
        transcript_publisher: TranscriptPublisher | None = None,
        state_publisher: StatePublisher | None = None,
        barge_in_callback: BargeInCallback | None = None,
        final_transcript_callback: FinalTranscriptCallback | None = None,
        initial_analytics: VoiceAnalytics | None = None,
    ) -> VoiceSessionState:
        key = (user_id, session_id)
        async with self._lock:
            if key in self._sessions:
                raise VoiceSessionConflictError("Voice session is already connected.")
            state = VoiceSessionState(
                session_id=session_id,
                user_id=user_id,
                connected_at=datetime.now(timezone.utc),
            )
            managed = _ManagedVoiceSession(
                state=state,
                state_publisher=state_publisher,
                barge_in_callback=barge_in_callback,
                final_transcript_callback=final_transcript_callback,
                analytics=(initial_analytics or VoiceAnalytics()).model_copy(deep=True),
                waiting_for_user_at=self.clock(),
            )
            self._sessions[key] = managed

            if self.pipeline_factory is not None and transcript_publisher is not None:
                async def publish_transcript(payload: dict[str, Any]) -> None:
                    await transcript_publisher(payload)
                    if (
                        payload.get("type") == "transcript_final"
                        and isinstance(payload.get("text"), str)
                        and payload["text"].strip()
                    ):
                        await self._handle_final_transcript(
                            session_id,
                            user_id,
                            payload["text"].strip(),
                        )

                managed.pipeline = self.pipeline_factory.create(
                    transcript_publisher=publish_transcript,
                    endpoint_callback=lambda: self._handle_endpoint(
                        session_id, user_id
                    ),
                    speech_started_callback=lambda: self._handle_speech_started(
                        session_id, user_id
                    ),
                    speech_end_callback=lambda: self._handle_speech_end(
                        session_id, user_id
                    ),
                    stt_started_callback=lambda: self._mark_latency(
                        session_id, user_id, "stt_started_time"
                    ),
                    stt_final_callback=lambda: self._mark_latency(
                        session_id, user_id, "stt_final_time"
                    ),
                )
            return state.model_copy(deep=True)

    async def disconnect(self, session_id: str, user_id: str) -> None:
        async with self._lock:
            managed = self._sessions.pop((user_id, session_id), None)
        if managed is not None and managed.pipeline is not None:
            await managed.pipeline.close()
        self.latency_registry.remove(session_id, user_id)

    async def start_listening(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state not in {
                VoiceSessionStatus.IDLE,
                VoiceSessionStatus.WAITING_FOR_USER,
            }:
                raise VoiceSessionProtocolError("Voice session is not ready to listen.")
            managed.pending_sequence = None
            managed.last_sequence = -1
            now = self.clock()
            if managed.waiting_for_user_at is not None:
                response_latency_ms = max(
                    0.0,
                    (now - managed.waiting_for_user_at) * 1000,
                )
                managed.analytics.response_latencies_ms = [
                    *managed.analytics.response_latencies_ms[-99:],
                    response_latency_ms,
                ]
            managed.state.state = VoiceSessionStatus.USER_SPEAKING
            managed.barge_in_monitoring = False
            managed.user_speech_started_at = now
            managed.waiting_for_user_at = None
            pipeline = managed.pipeline
            state = managed.state.model_copy(deep=True)

        if pipeline is not None:
            try:
                await pipeline.start()
            except Exception as error:
                await self._set_state(
                    session_id, user_id, VoiceSessionStatus.IDLE, publish=False
                )
                raise VoiceSessionProtocolError(
                    "Speech recognition could not start."
                ) from error
        return state

    async def stop_listening(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state != VoiceSessionStatus.USER_SPEAKING:
                raise VoiceSessionProtocolError("Voice session is not listening.")
            if managed.pending_sequence is not None:
                raise VoiceSessionProtocolError(
                    "An announced audio chunk is missing its binary payload."
                )
            managed.state.state = VoiceSessionStatus.TRANSCRIBING
            self.latency_registry.start_turn(session_id, user_id)
            self._record_speech_end(managed, session_id, user_id)
            return managed.state.model_copy(deep=True)

    async def start_barge_in_monitoring(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state != VoiceSessionStatus.AI_SPEAKING:
                raise VoiceSessionProtocolError(
                    "Barge-in monitoring requires active AI speech."
                )
            if managed.barge_in_monitoring:
                return managed.state.model_copy(deep=True)
            managed.pending_sequence = None
            managed.last_sequence = -1
            managed.barge_in_monitoring = True
            pipeline = managed.pipeline
            snapshot = managed.state.model_copy(deep=True)
        if pipeline is not None:
            try:
                await pipeline.start()
            except Exception as error:
                async with self._lock:
                    self._get(session_id, user_id).barge_in_monitoring = False
                raise VoiceSessionProtocolError(
                    "Barge-in detection could not start."
                ) from error
        return snapshot

    async def complete_playback(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state == VoiceSessionStatus.USER_SPEAKING:
                return managed.state.model_copy(deep=True)
            if managed.state.state != VoiceSessionStatus.AI_SPEAKING:
                raise VoiceSessionProtocolError("AI playback is not active.")
            managed.barge_in_monitoring = False
            managed.state.state = VoiceSessionStatus.WAITING_FOR_USER
            managed.waiting_for_user_at = self.clock()
            pipeline = managed.pipeline
            snapshot = managed.state.model_copy(deep=True)
        if pipeline is not None:
            await pipeline.close()
        return snapshot

    async def finish_transcription(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state != VoiceSessionStatus.TRANSCRIBING:
                return managed.state.model_copy(deep=True)
            pipeline = managed.pipeline

        if pipeline is not None:
            await pipeline.finish()
        else:
            await self._handle_endpoint(session_id, user_id)

        async with self._lock:
            return self._get(session_id, user_id).state.model_copy(deep=True)

    async def begin_answer_submission(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state not in {
                VoiceSessionStatus.TRANSCRIBING,
            }:
                raise VoiceSessionProtocolError(
                    "An answer can only be confirmed after transcription."
                )
            managed.state.state = VoiceSessionStatus.EVALUATING
            return managed.state.model_copy(deep=True)

    async def mark_answer_processing(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state not in {
                VoiceSessionStatus.EVALUATING,
            }:
                raise VoiceSessionProtocolError("Answer submission is not active.")
            managed.state.state = VoiceSessionStatus.EVALUATING
            return managed.state.model_copy(deep=True)

    async def mark_ai_thinking(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        return await self._set_state(
            session_id,
            user_id,
            VoiceSessionStatus.AI_THINKING,
            publish=True,
        )

    async def mark_ai_speaking(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state not in {
                VoiceSessionStatus.EVALUATING,
                VoiceSessionStatus.AI_THINKING,
                VoiceSessionStatus.AI_SPEAKING,
            }:
                raise VoiceSessionProtocolError(
                    "AI speech is not available in the current state."
                )
            managed.state.state = VoiceSessionStatus.AI_SPEAKING
            snapshot = managed.state.model_copy(deep=True)
            publisher = managed.state_publisher
        if publisher is not None:
            await publisher(VoiceSessionStatus.AI_SPEAKING)
        return snapshot

    async def finish_answer_submission(
        self,
        session_id: str,
        user_id: str,
        *,
        has_next_question: bool,
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if (
                has_next_question
                and managed.state.state
                in {
                    VoiceSessionStatus.AI_SPEAKING,
                    VoiceSessionStatus.USER_SPEAKING,
                    VoiceSessionStatus.TRANSCRIBING,
                    VoiceSessionStatus.EVALUATING,
                    VoiceSessionStatus.INTERRUPTED,
                }
            ):
                return managed.state.model_copy(deep=True)
        return await self._set_state(
            session_id,
            user_id,
            (
                VoiceSessionStatus.WAITING_FOR_USER
                if has_next_question
                else VoiceSessionStatus.IDLE
            ),
            publish=False,
        )

    async def recover_answer_submission(
        self, session_id: str, user_id: str
    ) -> VoiceSessionState:
        return await self._set_state(
            session_id,
            user_id,
            VoiceSessionStatus.WAITING_FOR_USER,
            publish=True,
        )

    async def announce_audio_chunk(
        self, session_id: str, user_id: str, sequence: int
    ) -> bool:
        """Register the metadata for the next binary frame.

        Returns False when the session has already stopped listening. A small
        burst of frames can already be in flight when the user presses Stop, so
        late frames are ignored instead of reported as protocol errors.
        """
        async with self._lock:
            managed = self._get(session_id, user_id)
            if (
                managed.state.state
                not in {
                    VoiceSessionStatus.WAITING_FOR_USER,
                    VoiceSessionStatus.USER_SPEAKING,
                }
                and not (
                    managed.state.state == VoiceSessionStatus.AI_SPEAKING
                    and managed.barge_in_monitoring
                )
            ):
                managed.pending_sequence = None
                managed.late_chunks += 1
                return False
            if managed.pending_sequence is not None:
                raise VoiceSessionProtocolError(
                    "The previous audio chunk has no binary payload."
                )
            if sequence <= managed.last_sequence:
                raise VoiceSessionProtocolError("Audio chunk sequence is out of order.")
            managed.pending_sequence = sequence
            return True

    async def receive_audio_chunk(
        self, session_id: str, user_id: str, payload: bytes
    ) -> tuple[int, int] | None:
        """Accept one binary PCM frame.

        Returns None when the frame arrived after the session stopped listening;
        those are expected in-flight frames, not protocol errors.
        """
        async with self._lock:
            managed = self._get(session_id, user_id)
            sequence = managed.pending_sequence
            if sequence is None:
                if managed.state.state not in {
                    VoiceSessionStatus.WAITING_FOR_USER,
                    VoiceSessionStatus.USER_SPEAKING,
                }:
                    managed.late_chunks += 1
                    return None
                raise VoiceSessionProtocolError(
                    "Binary audio requires audio_chunk metadata."
                )
            managed.pending_sequence = None

            chunk_size = len(payload)
            if chunk_size == 0:
                raise AudioChunkError("Audio chunk must not be empty.")
            if chunk_size > self.max_chunk_bytes:
                raise AudioChunkError(
                    "Audio chunk exceeds the allowed size.",
                    code="audio_chunk_too_large",
                )
            if managed.bytes_received + chunk_size > self.max_session_bytes:
                raise AudioChunkError(
                    "Voice session audio limit exceeded.",
                    code="voice_session_limit_exceeded",
                )
            if chunk_size % 2:
                raise AudioChunkError("PCM16 audio chunk has an invalid byte length.")

            pipeline = managed.pipeline
            managed.last_sequence = sequence
            managed.bytes_received += chunk_size

        if pipeline is not None:
            try:
                accepted = pipeline.enqueue(payload)
            except AudioQueueFullError:
                # Older pipelines still raise. Treat it the same as a drop:
                # tearing down the socket would end the interview outright.
                accepted = False
            except RuntimeError as error:
                raise VoiceSessionProtocolError(
                    "Audio pipeline is not available."
                ) from error
            if accepted is False:
                async with self._lock:
                    managed = self._sessions.get((user_id, session_id))
                    if managed is not None:
                        managed.dropped_chunks += 1
        return sequence, chunk_size

    async def dropped_chunk_count(self, session_id: str, user_id: str) -> int:
        async with self._lock:
            return self._get(session_id, user_id).dropped_chunks

    async def active_session_count(self) -> int:
        async with self._lock:
            return len(self._sessions)

    async def analytics_snapshot(
        self, session_id: str, user_id: str
    ) -> VoiceAnalytics:
        async with self._lock:
            return self._get(session_id, user_id).analytics.model_copy(deep=True)

    async def _handle_endpoint(self, session_id: str, user_id: str) -> None:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state != VoiceSessionStatus.TRANSCRIBING:
                return
            managed.state.state = VoiceSessionStatus.WAITING_FOR_USER
            managed.waiting_for_user_at = self.clock()
            publisher = managed.state_publisher
        if publisher is not None:
            await publisher(VoiceSessionStatus.WAITING_FOR_USER)

    async def _handle_final_transcript(
        self,
        session_id: str,
        user_id: str,
        transcript: str,
    ) -> None:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state != VoiceSessionStatus.TRANSCRIBING:
                return
            managed.state.state = VoiceSessionStatus.EVALUATING
            publisher = managed.state_publisher
            callback = managed.final_transcript_callback
        if publisher is not None:
            await publisher(VoiceSessionStatus.EVALUATING)
        if callback is not None:
            await callback(transcript)

    async def _handle_speech_started(
        self, session_id: str, user_id: str
    ) -> None:
        async with self._lock:
            managed = self._get(session_id, user_id)
            previous_state = managed.state.state
            is_interruption = (
                previous_state == VoiceSessionStatus.AI_SPEAKING
                and managed.barge_in_monitoring
            )
            if previous_state not in {
                VoiceSessionStatus.WAITING_FOR_USER,
                VoiceSessionStatus.AI_SPEAKING,
            }:
                return
            if previous_state == VoiceSessionStatus.AI_SPEAKING and not is_interruption:
                return
            now = self.clock()
            if managed.waiting_for_user_at is not None and not is_interruption:
                latency_ms = max(0.0, (now - managed.waiting_for_user_at) * 1000)
                managed.analytics.response_latencies_ms = [
                    *managed.analytics.response_latencies_ms[-99:],
                    latency_ms,
                ]
            if is_interruption:
                managed.analytics.interruption_count += 1
                managed.state.state = VoiceSessionStatus.INTERRUPTED
            managed.user_speech_started_at = now
            managed.waiting_for_user_at = None
            managed.barge_in_monitoring = False
            state_publisher = managed.state_publisher
            barge_in_callback = managed.barge_in_callback if is_interruption else None
        if is_interruption:
            if state_publisher is not None:
                await state_publisher(VoiceSessionStatus.INTERRUPTED)
            if barge_in_callback is not None:
                await barge_in_callback()
            self.latency_registry.log_summary(session_id, user_id)
            self.latency_registry.start_turn(session_id, user_id)
        async with self._lock:
            managed = self._get(session_id, user_id)
            managed.state.state = VoiceSessionStatus.USER_SPEAKING
        if state_publisher is not None:
            await state_publisher(VoiceSessionStatus.USER_SPEAKING)

    async def _handle_speech_end(
        self, session_id: str, user_id: str
    ) -> None:
        async with self._lock:
            managed = self._get(session_id, user_id)
            if managed.state.state not in {
                VoiceSessionStatus.USER_SPEAKING,
            }:
                return
            managed.state.state = VoiceSessionStatus.TRANSCRIBING
            self._record_speech_end(managed, session_id, user_id)
            publisher = managed.state_publisher
        if publisher is not None:
            await publisher(VoiceSessionStatus.TRANSCRIBING)

    def _record_speech_end(
        self,
        managed: _ManagedVoiceSession,
        session_id: str,
        user_id: str,
    ) -> None:
        now = self.clock()
        if managed.user_speech_started_at is not None:
            managed.analytics.speaking_duration_ms += max(
                0.0,
                (now - managed.user_speech_started_at) * 1000,
            )
            managed.user_speech_started_at = None
        self.latency_registry.mark(session_id, user_id, "speech_end_time")

    async def _mark_latency(
        self,
        session_id: str,
        user_id: str,
        milestone: str,
    ) -> None:
        self.latency_registry.mark(session_id, user_id, milestone)

    async def _set_state(
        self,
        session_id: str,
        user_id: str,
        state: VoiceSessionStatus,
        *,
        publish: bool,
    ) -> VoiceSessionState:
        async with self._lock:
            managed = self._get(session_id, user_id)
            managed.state.state = state
            snapshot = managed.state.model_copy(deep=True)
            publisher = managed.state_publisher
        if publish and publisher is not None:
            await publisher(state)
        return snapshot

    def _get(self, session_id: str, user_id: str) -> _ManagedVoiceSession:
        managed = self._sessions.get((user_id, session_id))
        if managed is None:
            raise VoiceSessionProtocolError("Voice session is not connected.")
        return managed
