from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


DecisionAction = Literal["follow_up", "next_question", "increase_difficulty", "finish"]


class InterviewDecision(BaseModel):
    action: DecisionAction
    reason: str
    next_topic: str | None = None
    difficulty_change: str | None = None
