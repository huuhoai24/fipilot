from __future__ import annotations

import json
import re
from collections.abc import Awaitable, Callable

from pydantic import ValidationError

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
    """Streams the question text so speech synthesis can start on the first token.

    Two deliberate differences from the non-streaming generator:

    * No ``output_schema``. Asking Gemini for schema-constrained output makes it
      buffer the whole structured response and emit it as a single chunk, which
      removed every bit of the latency benefit this class exists for. The prompt
      already pins the JSON shape and puts ``question`` first, and the response is
      still validated against InterviewQuestion below.
    * ``task_type="simple"``. This runs while the candidate waits in silence, so
      the faster model is the right trade; the non-streaming path still uses the
      stronger model.
    * ``thinking_budget=0``. Gemini 2.5 thinks before emitting any token. Measured
      on this prompt: ~14.6 s to first token with thinking, ~4.1 s without. That
      delay is dead air in a spoken interview.
    """

    def __init__(
        self,
        llm_service: BaseLLMService,
        *,
        task_type: str = "simple",
        thinking_budget: int | None = 0,
    ) -> None:
        self.llm_service = llm_service
        self.task_type = task_type
        self.thinking_budget = thinking_budget

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

        stream_kwargs: dict = {
            "system_instruction": QUESTION_GENERATOR_SYSTEM_INSTRUCTION,
            "task_type": self.task_type,
            "temperature": 0.6,
        }
        if self.thinking_budget is not None:
            stream_kwargs["thinking_budget"] = self.thinking_budget

        async for raw_delta in self.llm_service.stream_text(prompt, **stream_kwargs):
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
        except (json.JSONDecodeError, ValidationError, ValueError):
            # The candidate has already heard this question read aloud, so
            # failing the turn here would be worse than rebuilding the metadata
            # from the round we asked about.
            return self._question_from_stream(
                decoder.text,
                interview_round,
                interview_config,
            )

        if question.question != decoder.text:
            # Trust what was spoken; the tail of the JSON is only metadata.
            question = question.model_copy(update={"question": decoder.text})
        return question

    @staticmethod
    def _question_from_stream(
        text: str,
        interview_round: InterviewRound,
        interview_config: InterviewConfig,
    ) -> InterviewQuestion:
        return InterviewQuestion(
            question=text.strip(),
            language=interview_config.language,
            topic=interview_round.topic,
            difficulty=interview_round.difficulty,
            reasoning="Rebuilt from the streamed question text.",
            expected_answer_points=list(interview_round.recommended_question_areas),
            follow_up_questions=[],
        )

    @staticmethod
    def _json_object_content(raw_response: str) -> str:
        content = raw_response.strip()
        content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
        start = content.find("{")
        if start < 0:
            raise ValueError("Response does not contain a JSON object")
        return content[start:]
