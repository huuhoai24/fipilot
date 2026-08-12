from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TranscriptEventType(str, Enum):
    PARTIAL = "partial"
    FINAL = "final"


class TranscriptEvent(BaseModel):
    type: TranscriptEventType
    text: str
    language: str
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime


class StreamingSTT(ABC):
    # Implementations whose partial transcription is expensive should set this to
    # True and implement append_audio/partial_due/transcribe_partial. The audio
    # pipeline then runs partials off the consumer path, so buffering audio never
    # waits on inference. Implementations that leave it False keep the simple
    # inline process_audio_chunk contract.
    supports_deferred_partials: bool = False

    @abstractmethod
    async def start_session(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def process_audio_chunk(
        self, audio_bytes: bytes
    ) -> TranscriptEvent | None:
        raise NotImplementedError

    @abstractmethod
    async def finish_session(self) -> TranscriptEvent | None:
        raise NotImplementedError

    async def append_audio(self, audio_bytes: bytes) -> None:
        """Buffer audio without running inference."""
        raise NotImplementedError

    def partial_due(self) -> bool:
        """True when enough new audio has arrived to justify a partial."""
        return False

    async def transcribe_partial(self) -> TranscriptEvent | None:
        """Transcribe the buffer for a partial result."""
        raise NotImplementedError


class StreamingSTTFactory(ABC):
    @abstractmethod
    def create(self) -> StreamingSTT:
        raise NotImplementedError

    def create_for_language(self, language: str | None) -> StreamingSTT:
        """Create a session STT, falling back to the factory configuration."""
        return self.create()
