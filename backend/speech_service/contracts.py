from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SpeechControlMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["stt_start", "stt_finish", "tts_synthesize"]
    text: str | None = Field(default=None, max_length=4096)

    @model_validator(mode="after")
    def validate_payload(self) -> "SpeechControlMessage":
        if self.type == "tts_synthesize":
            if self.text is None or not self.text.strip():
                raise ValueError("tts_synthesize requires text")
        elif self.text is not None:
            raise ValueError("text is only valid for tts_synthesize")
        return self
