from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class VoiceSessionStatus(str, Enum):
    IDLE = "IDLE"
    AI_THINKING = "AI_THINKING"
    AI_SPEAKING = "AI_SPEAKING"
    WAITING_FOR_USER = "WAITING_FOR_USER"
    USER_SPEAKING = "USER_SPEAKING"
    TRANSCRIBING = "TRANSCRIBING"
    EVALUATING = "EVALUATING"
    INTERRUPTED = "INTERRUPTED"


class VoiceSessionState(BaseModel):
    session_id: str
    user_id: str
    connected_at: datetime
    state: VoiceSessionStatus = VoiceSessionStatus.WAITING_FOR_USER
