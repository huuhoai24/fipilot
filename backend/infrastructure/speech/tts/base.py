from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class AudioChunk:
    bytes: bytes
    sample_rate: int
    format: Literal["pcm"] = "pcm"


class StreamingTTS(ABC):
    @abstractmethod
    def synthesize_stream(self, text: str) -> AsyncIterator[AudioChunk]:
        """Stream mono PCM16 little-endian audio for one text chunk."""
