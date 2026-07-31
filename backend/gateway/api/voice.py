from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from contextlib import suppress
from typing import Coroutine

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from core.dependencies import (
    get_app_settings,
    get_auth_service,
    get_interview_repository,
    get_question_speech_streamer_factory,
    get_question_streaming_service,
    get_voice_answer_submission_service,
    get_voice_session_manager,
)
from core.exceptions import AuthenticationError
from core.logging import get_logger
from core.settings import Settings
from infrastructure.repositories.base import InterviewRepository
from services.voice_session.events import (
    ClientVoiceEvent,
    audio_format_event,
    audio_ack_event,
    completed_event,
    connected_event,
    error_event,
    processing_event,
    question_complete_event,
    question_delta_event,
    question_start_event,
    state_event,
    tts_complete_event,
    tts_cancelled_event,
    tts_start_event,
)
from services.voice_session.question_speech import (
    QuestionSpeechStreamer,
    QuestionSpeechStreamerFactory,
)
from services.question_generator.streaming_service import QuestionStreamingService
from services.voice_session.answer_service import (
    VoiceAnswerSubmissionError,
    VoiceAnswerSubmissionService,
)
from services.voice_session.manager import (
    AudioChunkError,
    VoiceSessionConflictError,
    VoiceSessionManager,
    VoiceSessionProtocolError,
)
from shared.schemas import CurrentUser, InterviewSessionState


router = APIRouter(tags=["v2-voice"])
AUTH_SUBPROTOCOL = "firebase-auth"
logger = get_logger(__name__)


class _VoiceConnectionRuntime:
    def __init__(self, websocket: WebSocket) -> None:
        self.websocket = websocket
        self.send_lock = asyncio.Lock()
        self.answer_task: asyncio.Task[None] | None = None
        self.question_speech: QuestionSpeechStreamer | None = None
        self.tts_cancelled = False

    async def send_json(self, payload: dict) -> None:
        async with self.send_lock:
            await self.websocket.send_json(payload)

    async def send_audio(self, payload: bytes) -> None:
        async with self.send_lock:
            await self.websocket.send_bytes(payload)

    def start_answer(self, coroutine: Coroutine[None, None, None]) -> bool:
        if self.answer_task is not None and not self.answer_task.done():
            coroutine.close()
            return False
        task = asyncio.create_task(coroutine)
        self.answer_task = task
        task.add_done_callback(self._answer_finished)
        return True

    def bind_speech(self, speech: QuestionSpeechStreamer) -> None:
        self.question_speech = speech
        self.tts_cancelled = False

    async def wait_for_answer_idle(self) -> None:
        task = self.answer_task
        if task is None or task.done():
            return
        with suppress(asyncio.CancelledError, Exception):
            await task

    async def cancel_tts(self) -> None:
        speech = self.question_speech
        if speech is None or self.tts_cancelled:
            return
        self.tts_cancelled = True
        await speech.cancel()
        await self.send_json(tts_cancelled_event())

    async def close(self) -> None:
        if self.question_speech is not None:
            await self.question_speech.cancel()
        task = self.answer_task
        if task is not None and not task.done():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    def _answer_finished(self, task: asyncio.Task[None]) -> None:
        if self.answer_task is task:
            self.answer_task = None
        with suppress(asyncio.CancelledError, Exception):
            task.result()


def _offered_protocols(websocket: WebSocket) -> list[str]:
    header = websocket.headers.get("sec-websocket-protocol", "")
    return [item.strip() for item in header.split(",") if item.strip()]


def _firebase_token(websocket: WebSocket) -> str | None:
    protocols = _offered_protocols(websocket)
    if len(protocols) != 2 or protocols[0] != AUTH_SUBPROTOCOL:
        return None
    return protocols[1]


def _origin_is_allowed(websocket: WebSocket, settings: Settings) -> bool:
    if not settings.cors_allowed_origins:
        return True
    origin = websocket.headers.get("origin")
    return bool(origin and origin in settings.cors_allowed_origins)


async def _reject(websocket: WebSocket, code: int, reason: str) -> None:
    await websocket.close(code=code, reason=reason)


@router.websocket("/api/v2/voice/interview/{session_id}")
async def voice_interview(
    websocket: WebSocket,
    session_id: str,
    settings: Settings = Depends(get_app_settings),
    auth_service=Depends(get_auth_service),
    repository: InterviewRepository = Depends(get_interview_repository),
    manager: VoiceSessionManager = Depends(get_voice_session_manager),
    answer_service: VoiceAnswerSubmissionService = Depends(
        get_voice_answer_submission_service
    ),
    question_streaming_service: QuestionStreamingService = Depends(
        get_question_streaming_service
    ),
    question_speech_factory: QuestionSpeechStreamerFactory = Depends(
        get_question_speech_streamer_factory
    ),
) -> None:
    if not _origin_is_allowed(websocket, settings):
        await _reject(websocket, 4403, "Origin is not allowed.")
        return

    if not settings.auth_enabled:
        # Mirror core.dependencies.get_current_user: with authentication off the
        # REST routes fall back to the development identity, so the voice socket
        # has to as well or local development cannot use voice at all.
        current_user = CurrentUser(
            uid=settings.auth_dev_user_id,
            name="Local Development User",
            email_verified=False,
            claims={"auth_provider": "development"},
        )
    else:
        token = _firebase_token(websocket)
        if token is None:
            await _reject(websocket, 4401, "Authentication is required.")
            return
        try:
            current_user = auth_service.verify_id_token(token)
        except AuthenticationError:
            await _reject(websocket, 4401, "Authentication failed.")
            return
        except Exception:
            await _reject(websocket, 1011, "Authentication service unavailable.")
            return

    session = repository.get_session(session_id, user_id=current_user.uid)
    if session is None:
        await _reject(websocket, 4404, "Interview session not found.")
        return
    if session.state_payload.get("interview_config", {}).get("mode") != "voice":
        await _reject(websocket, 4409, "Interview session is not configured for voice.")
        return

    runtime = _VoiceConnectionRuntime(websocket)
    try:
        persisted_state = InterviewSessionState.model_validate(session.state_payload)
    except ValidationError:
        await _reject(websocket, 4409, "Interview session is unavailable.")
        return

    async def submit_final_transcript(text: str) -> None:
        await runtime.wait_for_answer_idle()
        started = runtime.start_answer(
            _handle_confirm_answer(
                session_id,
                current_user.uid,
                text,
                manager,
                answer_service,
                question_streaming_service,
                question_speech_factory,
                runtime,
                automatic=True,
            )
        )
        if not started:
            await runtime.send_json(
                error_event(
                    "An answer is already being processed.",
                    "answer_processing",
                )
            )

    try:
        state = await manager.connect(
            session_id,
            current_user.uid,
            transcript_publisher=runtime.send_json,
            state_publisher=lambda value: runtime.send_json(state_event(value)),
            barge_in_callback=runtime.cancel_tts,
            final_transcript_callback=submit_final_transcript,
            initial_analytics=persisted_state.voice_analytics,
        )
    except VoiceSessionConflictError:
        await _reject(websocket, 4429, "Voice session is already connected.")
        return

    try:
        # Only echo the subprotocol the client actually offered. With auth disabled a
        # dev client may connect without one, and echoing an unoffered subprotocol
        # makes browsers drop the connection.
        await websocket.accept(
            subprotocol=(
                AUTH_SUBPROTOCOL
                if AUTH_SUBPROTOCOL in _offered_protocols(websocket)
                else None
            )
        )
        await runtime.send_json(connected_event(session_id))
        await runtime.send_json(state_event(state.state))

        async def speak_current_question() -> None:
            # Re-read the session so a reconnect mid-interview speaks the question
            # the candidate is actually on, not the one from connect time.
            record = repository.get_session(session_id, user_id=current_user.uid)
            latest = persisted_state
            if record is not None and record.state_payload:
                try:
                    latest = InterviewSessionState.model_validate(record.state_payload)
                except ValidationError:
                    latest = persisted_state
            await _speak_pending_question(
                latest,
                manager,
                session_id,
                current_user.uid,
                question_speech_factory,
                runtime,
            )

        try:
            while True:
                message = await websocket.receive()
                if message["type"] == "websocket.disconnect":
                    break
                if message.get("text") is not None:
                    should_continue = await _handle_text_message(
                        websocket,
                        message["text"],
                        session_id,
                        current_user.uid,
                        manager,
                        answer_service,
                        question_streaming_service,
                        question_speech_factory,
                        runtime,
                        settings.max_voice_message_chars,
                        speak_current_question,
                    )
                    if not should_continue:
                        break
                elif message.get("bytes") is not None:
                    should_continue = await _handle_binary_message(
                        websocket,
                        message["bytes"],
                        session_id,
                        current_user.uid,
                        manager,
                        runtime,
                    )
                    if not should_continue:
                        break
        except WebSocketDisconnect:
            pass
    finally:
        await runtime.close()
        await manager.disconnect(session_id, current_user.uid)


async def _speak_pending_question(
    state: InterviewSessionState,
    manager: VoiceSessionManager,
    session_id: str,
    user_id: str,
    question_speech_factory: QuestionSpeechStreamerFactory,
    runtime: _VoiceConnectionRuntime,
) -> None:
    """Read the already-generated current question aloud.

    The first question comes from the REST /start call, so nothing on the socket
    ever synthesised it: candidates saw question 1 as text but heard silence,
    while every later question was spoken. This also covers reconnects.
    """
    turn = state.current_turn
    if turn is None:
        return
    question = turn.question
    question_text = question if isinstance(question, str) else question.question
    if not question_text.strip():
        return

    send_json = runtime.send_json
    speech = question_speech_factory.create(
        start_publisher=lambda: _start_tts(manager, session_id, user_id, send_json),
        format_publisher=lambda chunk: send_json(
            audio_format_event(chunk.sample_rate, chunk.format)
        ),
        audio_publisher=runtime.send_audio,
        complete_publisher=lambda: send_json(tts_complete_event()),
        error_publisher=lambda: send_json(
            error_event("Question audio could not be generated.", "tts_failed")
        ),
        first_audio_publisher=lambda: _mark_tts_first_audio(
            manager, session_id, user_id
        ),
    )
    runtime.bind_speech(speech)
    try:
        # mark_ai_speaking (driven by the TTS start publisher) only accepts
        # EVALUATING / AI_THINKING / AI_SPEAKING, and a fresh connection sits in
        # WAITING_FOR_USER, so move through AI_THINKING first.
        await manager.mark_ai_thinking(session_id, user_id)
        await send_json(question_start_event())
        await send_json(question_delta_event(question_text))
        await speech.feed_text_delta(question_text)
        speech.mark_question_complete()
        await send_json(question_complete_event(question_text))
        await speech.finish()
    except Exception:
        await speech.cancel()
        logger.exception(
            "Could not speak the pending interview question.",
            extra={"event": "voice_pending_question_failed", "session_id": session_id},
        )


async def _handle_text_message(
    websocket: WebSocket,
    raw_message: str,
    session_id: str,
    user_id: str,
    manager: VoiceSessionManager,
    answer_service: VoiceAnswerSubmissionService,
    question_streaming_service: QuestionStreamingService,
    question_speech_factory: QuestionSpeechStreamerFactory,
    runtime: _VoiceConnectionRuntime,
    max_message_chars: int,
    speak_current_question: Callable[[], Awaitable[None]] | None = None,
) -> bool:
    if len(raw_message) > max_message_chars:
        await runtime.send_json(error_event("Control message is too large.", "message_too_large"))
        await websocket.close(code=1009, reason="Control message is too large.")
        return False

    try:
        event = ClientVoiceEvent.model_validate(json.loads(raw_message))
        if event.type == "start_listening":
            state = await manager.start_listening(session_id, user_id)
            await runtime.send_json(state_event(state.state))
        elif event.type == "stop_listening":
            state = await manager.stop_listening(session_id, user_id)
            await runtime.send_json(state_event(state.state))
            await manager.finish_transcription(session_id, user_id)
        elif event.type == "audio_chunk":
            await manager.announce_audio_chunk(
                session_id,
                user_id,
                event.sequence if event.sequence is not None else -1,
            )
        elif event.type == "start_barge_in":
            await manager.start_barge_in_monitoring(session_id, user_id)
        elif event.type == "playback_complete":
            state = await manager.complete_playback(session_id, user_id)
            runtime.question_speech = None
            await runtime.send_json(state_event(state.state))
        elif event.type == "speak_question":
            if speak_current_question is not None:
                await speak_current_question()
        else:
            started = runtime.start_answer(_handle_confirm_answer(
                session_id,
                user_id,
                event.text or "",
                manager,
                answer_service,
                question_streaming_service,
                question_speech_factory,
                runtime,
                automatic=False,
            ))
            if not started:
                await runtime.send_json(
                    error_event(
                        "An answer is already being processed.",
                        "answer_processing",
                    )
                )
    except (json.JSONDecodeError, ValidationError, VoiceSessionProtocolError):
        await runtime.send_json(error_event("Invalid voice control message."))
    return True


async def _handle_confirm_answer(
    session_id: str,
    user_id: str,
    answer: str,
    manager: VoiceSessionManager,
    answer_service: VoiceAnswerSubmissionService,
    question_streaming_service: QuestionStreamingService,
    question_speech_factory: QuestionSpeechStreamerFactory,
    runtime: _VoiceConnectionRuntime,
    *,
    automatic: bool,
) -> None:
    if not automatic:
        try:
            await manager.begin_answer_submission(session_id, user_id)
        except VoiceSessionProtocolError:
            await runtime.send_json(
                error_event(
                    "Answer can only be submitted after transcription.",
                    "answer_not_ready",
                )
            )
            return

    await manager.mark_answer_processing(session_id, user_id)
    await runtime.send_json(processing_event("evaluation"))
    question_stream_started = False
    question_speech: QuestionSpeechStreamer | None = None
    send_json = runtime.send_json
    send_audio = runtime.send_audio

    def get_question_speech() -> QuestionSpeechStreamer:
        nonlocal question_speech
        if question_speech is None:
            question_speech = question_speech_factory.create(
                start_publisher=lambda: _start_tts(
                    manager,
                    session_id,
                    user_id,
                    send_json,
                ),
                format_publisher=lambda chunk: send_json(
                    audio_format_event(
                        chunk.sample_rate,
                        chunk.format,
                    )
                ),
                audio_publisher=send_audio,
                complete_publisher=lambda: send_json(tts_complete_event()),
                error_publisher=lambda: send_json(
                    error_event(
                        "Question audio could not be generated.",
                        "tts_failed",
                    )
                ),
                first_audio_publisher=lambda: _mark_tts_first_audio(
                    manager,
                    session_id,
                    user_id,
                ),
            )
            runtime.bind_speech(question_speech)
        return question_speech

    async def stream_question(
        candidate_profile,
        interview_round,
        interview_config,
    ):
        nonlocal question_stream_started
        question_stream_started = True
        manager.latency_registry.mark(
            session_id,
            user_id,
            "evaluation_completed_time",
        )
        await manager.mark_ai_thinking(session_id, user_id)
        speech = get_question_speech()
        await send_json(question_start_event())

        async def publish_delta(text: str) -> None:
            manager.latency_registry.mark(
                session_id,
                user_id,
                "question_generated_time",
            )
            await send_json(question_delta_event(text))
            await speech.feed_text_delta(text)

        return await question_streaming_service.generate_question(
            candidate_profile,
            interview_round,
            interview_config,
            delta_publisher=publish_delta,
        )

    try:
        updated_state = await answer_service.submit_answer(
            session_id,
            user_id,
            answer,
            question_provider=stream_question,
            voice_analytics=await manager.analytics_snapshot(
                session_id,
                user_id,
            ),
        )
    except VoiceAnswerSubmissionError as error:
        if question_speech is not None:
            await question_speech.cancel()
        await manager.recover_answer_submission(session_id, user_id)
        await send_json(error_event(str(error), error.code))
        return
    except Exception:
        if question_speech is not None:
            await question_speech.cancel()
        await manager.recover_answer_submission(session_id, user_id)
        await send_json(
            error_event(
                "The answer could not be evaluated. Please try again.",
                "answer_evaluation_failed",
            )
        )
        return

    manager.latency_registry.mark(
        session_id,
        user_id,
        "evaluation_completed_time",
    )
    has_next_question = updated_state.current_turn is not None
    if not has_next_question:
        if question_speech is not None:
            await question_speech.cancel()
        await manager.finish_answer_submission(
            session_id,
            user_id,
            has_next_question=False,
        )
        manager.latency_registry.log_summary(session_id, user_id)
        await send_json(completed_event())
        return

    question = updated_state.current_turn.question
    question_text = question if isinstance(question, str) else question.question
    speech = get_question_speech()
    if not question_stream_started:
        manager.latency_registry.mark(
            session_id,
            user_id,
            "question_generated_time",
        )
        await send_json(question_start_event())
        await send_json(question_delta_event(question_text))
        await speech.feed_text_delta(question_text)
    speech.mark_question_complete()
    await send_json(question_complete_event(question_text))
    metrics = await speech.finish()
    await manager.finish_answer_submission(
        session_id,
        user_id,
        has_next_question=True,
    )
    _log_question_speech_metrics(session_id, metrics)


async def _start_tts(
    manager: VoiceSessionManager,
    session_id: str,
    user_id: str,
    publisher,
) -> None:
    await manager.mark_ai_speaking(session_id, user_id)
    await publisher(tts_start_event())


async def _mark_tts_first_audio(
    manager: VoiceSessionManager,
    session_id: str,
    user_id: str,
) -> None:
    manager.latency_registry.mark(session_id, user_id, "tts_first_audio")
    manager.latency_registry.log_summary(session_id, user_id)


def _log_question_speech_metrics(session_id: str, metrics) -> None:
    if metrics.question_complete_time_ms is not None:
        logger.info(
            "Voice question generation completed.",
            extra={
                "event": "voice_question_complete",
                "session_id": session_id,
                "duration_ms": round(metrics.question_complete_time_ms, 2),
            },
        )
    if metrics.tts_first_audio_time_ms is not None:
        logger.info(
            "Voice TTS produced first audio.",
            extra={
                "event": "voice_tts_first_audio",
                "session_id": session_id,
                "duration_ms": round(metrics.tts_first_audio_time_ms, 2),
            },
        )


async def _handle_binary_message(
    websocket: WebSocket,
    payload: bytes,
    session_id: str,
    user_id: str,
    manager: VoiceSessionManager,
    runtime: _VoiceConnectionRuntime,
) -> bool:
    try:
        accepted = await manager.receive_audio_chunk(session_id, user_id, payload)
        if accepted is None:
            # Frame arrived after the session stopped listening. Expected while
            # the client drains its capture buffer; acknowledging or erroring on
            # each one only produced noise.
            return True
        sequence, chunk_size = accepted
        await runtime.send_json(audio_ack_event(sequence, chunk_size))
        return True
    except AudioChunkError as error:
        await runtime.send_json(error_event(str(error), error.code))
        await websocket.close(code=1009, reason="Audio payload rejected.")
        return False
    except VoiceSessionProtocolError:
        await runtime.send_json(error_event("Unexpected binary audio payload."))
        return True
