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


class StreamingSTTFactory(ABC):
    @abstractmethod
    def create(self) -> StreamingSTT:
        raise NotImplementedError
