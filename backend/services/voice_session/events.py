from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from services.voice_session.schemas import VoiceSessionStatus


class ClientVoiceEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "start_listening",
        "stop_listening",
        "audio_chunk",
        "confirm_answer",
        "start_barge_in",
        "playback_complete",
        # Ask the server to read the current question aloud. The first question
        # is produced by the REST /start call, so without this the candidate saw
        # question 1 as text and heard nothing. Also used after a reconnect.
        "speak_question",
        "speak_interviewer",
        "stop_playback",
    ]
    sequence: int | None = Field(default=None, ge=0)
    encoding: Literal["pcm_s16le"] | None = None
    sample_rate: Literal[16000] | None = None
    text: str | None = Field(default=None, max_length=12000)
    turn_id: str | None = Field(default=None, min_length=1, max_length=128)
    message_kind: Literal["closing"] | None = None

    @model_validator(mode="after")
    def validate_payload(self) -> "ClientVoiceEvent":
        if self.type == "audio_chunk" and self.sequence is None:
            raise ValueError("audio_chunk requires sequence")
        if self.type != "audio_chunk" and self.sequence is not None:
            raise ValueError("sequence is only valid for audio_chunk")
        if self.type != "audio_chunk" and (
            self.encoding is not None or self.sample_rate is not None
        ):
            raise ValueError("audio format is only valid for audio_chunk")
        if self.type == "confirm_answer":
            if self.text is None or not self.text.strip():
                raise ValueError("confirm_answer requires non-empty text")
            if self.turn_id is None:
                raise ValueError("confirm_answer requires turn_id")
        elif self.text is not None:
            raise ValueError("text is only valid for confirm_answer")
        if self.type == "speak_interviewer":
            has_turn = self.turn_id is not None
            has_kind = self.message_kind is not None
            if has_turn == has_kind:
                raise ValueError(
                    "speak_interviewer requires exactly one dialogue selector"
                )
        elif self.type != "confirm_answer" and (
            self.turn_id is not None or self.message_kind is not None
        ):
            raise ValueError(
                "dialogue selectors are only valid for speak_interviewer"
            )
        return self


def connected_event(session_id: str) -> dict[str, Any]:
    return {"type": "connected", "session_id": session_id}


def state_event(value: VoiceSessionStatus) -> dict[str, Any]:
    return {"type": "state", "value": value.value}


def audio_ack_event(sequence: int, bytes_received: int) -> dict[str, Any]:
    return {
        "type": "audio_ack",
        "sequence": sequence,
        "bytes_received": bytes_received,
    }


def processing_event(stage: Literal["evaluation"]) -> dict[str, Any]:
    return {"type": "processing", "stage": stage}


def question_start_event() -> dict[str, Any]:
    return {"type": "question_start"}


def question_delta_event(text: str) -> dict[str, Any]:
    return {"type": "question_delta", "text": text}


def question_complete_event(text: str) -> dict[str, Any]:
    return {"type": "question_complete", "text": text}


def tts_start_event() -> dict[str, Any]:
    return {"type": "tts_start"}


def audio_format_event(
    sample_rate: int,
    audio_format: Literal["pcm"],
) -> dict[str, Any]:
    return {
        "type": "audio_format",
        "sample_rate": sample_rate,
        "format": audio_format,
    }


def tts_complete_event() -> dict[str, Any]:
    return {"type": "tts_complete"}


def tts_cancelled_event() -> dict[str, Any]:
    return {"type": "tts_cancelled"}


def question_event(text: str) -> dict[str, Any]:
    return {"type": "question", "text": text}


def completed_event() -> dict[str, Any]:
    return {"type": "completed"}


def error_event(message: str, code: str = "invalid_message") -> dict[str, Any]:
    return {"type": "error", "code": code, "message": message}
