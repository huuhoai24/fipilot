from __future__ import annotations

import json
import re
from collections.abc import Awaitable, Callable

from infrastructure.llm.base import BaseLLMService
from services.question_generator.prompts import (
    QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
    build_streaming_question_generator_prompt,
)
from shared.schemas import (
    CandidateProfile,
    InterviewConfig,
    InterviewQuestion,
    InterviewRound,
)


QuestionDeltaPublisher = Callable[[str], Awaitable[None]]


class QuestionStreamingError(RuntimeError):
    pass


class _QuestionFieldDecoder:
    _field_pattern = re.compile(r'"question"\s*:\s*"')
    _escape_map = {
        '"': '"',
        "\\": "\\",
        "/": "/",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }

    def __init__(self) -> None:
        self.buffer = ""
        self.index = 0
        self.started = False
        self.complete = False
        self.escaped = False
        self.unicode_digits: str | None = None
        self.text = ""

    def feed(self, chunk: str) -> str:
        if self.complete or not chunk:
            return ""
        self.buffer += chunk

        if not self.started:
            match = self._field_pattern.search(self.buffer)
            if match is None:
                return ""
            self.started = True
            self.index = match.end()

        delta_start = len(self.text)
        while self.index < len(self.buffer) and not self.complete:
            character = self.buffer[self.index]
            self.index += 1

            if self.unicode_digits is not None:
                self.unicode_digits += character
                if len(self.unicode_digits) == 4:
                    try:
                        self.text += chr(int(self.unicode_digits, 16))
                    except ValueError as error:
                        raise QuestionStreamingError(
                            "Gemini streamed an invalid Unicode escape."
                        ) from error
                    self.unicode_digits = None
                continue

            if self.escaped:
                self.escaped = False
                if character == "u":
                    self.unicode_digits = ""
                    continue
                decoded = self._escape_map.get(character)
                if decoded is None:
                    raise QuestionStreamingError(
                        "Gemini streamed an invalid JSON escape."
                    )
                self.text += decoded
                continue

            if character == "\\":
                self.escaped = True
            elif character == '"':
                self.complete = True
            else:
                self.text += character

        return self.text[delta_start:]


class QuestionStreamingService:
    def __init__(self, llm_service: BaseLLMService) -> None:
        self.llm_service = llm_service

    async def generate_question(
        self,
        candidate_profile: CandidateProfile,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
        *,
        delta_publisher: QuestionDeltaPublisher,
    ) -> InterviewQuestion:
        prompt = build_streaming_question_generator_prompt(
            candidate_profile,
            interview_round,
            interview_config,
        )
        decoder = _QuestionFieldDecoder()
        raw_response = ""

        async for raw_delta in self.llm_service.stream_text(
            prompt,
            system_instruction=QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
            task_type="complex",
            temperature=0.2,
            output_schema=InterviewQuestion,
        ):
            raw_response += raw_delta
            question_delta = decoder.feed(raw_delta)
            if question_delta:
                await delta_publisher(question_delta)

        if not decoder.complete or not decoder.text.strip():
            raise QuestionStreamingError(
                "Gemini did not stream a complete interview question."
            )

        try:
            payload, _ = json.JSONDecoder().raw_decode(
                self._json_object_content(raw_response)
            )
            question = InterviewQuestion.model_validate(payload)
        except (json.JSONDecodeError, ValueError) as error:
            raise QuestionStreamingError(
                "Gemini returned an invalid interview question."
            ) from error

        if question.question != decoder.text:
            raise QuestionStreamingError(
                "Streamed question does not match the validated response."
            )
        return question

    @staticmethod
    def _json_object_content(raw_response: str) -> str:
        content = raw_response.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
        start = content.find("{")
        if start < 0:
            raise ValueError("Response does not contain a JSON object")
        return content[start:]
