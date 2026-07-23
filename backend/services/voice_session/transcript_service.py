from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from infrastructure.speech.stt.base import TranscriptEvent, TranscriptEventType


TranscriptPublisher = Callable[[dict[str, Any]], Awaitable[None]]


class TranscriptService:
    """Maps STT results to safe WebSocket events without logging or persistence."""

    def __init__(self, publisher: TranscriptPublisher) -> None:
        self.publisher = publisher

    async def publish(self, event: TranscriptEvent) -> bool:
        text = event.text.strip()
        if not text:
            return False
        event_type = (
            "transcript_partial"
            if event.type == TranscriptEventType.PARTIAL
            else "transcript_final"
        )
        await self.publisher(
            {
                "type": event_type,
                "text": text,
                "language": event.language,
                "confidence": event.confidence,
                "timestamp": event.timestamp.isoformat(),
            }
        )
        return True
