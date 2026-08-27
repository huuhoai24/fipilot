from __future__ import annotations

import json
import os
import re
from collections.abc import AsyncIterator
from typing import Any

from pydantic import BaseModel, ValidationError

from core.logging import get_logger
from core.settings import Settings, get_settings
from infrastructure.llm.base import BaseLLMService, LLMTaskType
from infrastructure.llm.vertex_gemini import (
    LLMConfigurationError,
    LLMResponseValidationError,
    LLMServiceError,
)


class AzureOpenAIService(BaseLLMService):
    """OpenAI-compatible LLM backend (Azure OpenAI, or any /openai/v1 endpoint).

    Backed by the `openai` SDK pointed at ``AZURE_OPENAI_BASE_URL``. Authentication
    uses ``AZURE_OPENAI_API_KEY``. Enable it via ``LLM_PROVIDER=azure`` (or by
    setting ``AZURE_OPENAI_BASE_URL``). This keeps the pipeline provider-agnostic
    so local development can run without Google Vertex AI credentials.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        *,
        default_timeout_seconds: float = 60.0,
    ) -> None:
        self.settings = settings or get_settings()
        self.default_timeout_seconds = default_timeout_seconds
        self.logger = get_logger(__name__)
        self._client: Any | None = None

    @property
    def client(self) -> Any:
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> Any:
        from openai import AsyncOpenAI

        base_url = os.environ.get("AZURE_OPENAI_BASE_URL")
        api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        if not base_url or not api_key:
            raise LLMConfigurationError(
                "AZURE_OPENAI_BASE_URL and AZURE_OPENAI_API_KEY are required "
                "for the Azure OpenAI LLM provider"
            )
        return AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=self.default_timeout_seconds,
        )

    def route_model(self, task_type: LLMTaskType = "simple", model: str | None = None) -> str:
        if model:
            return model
        if task_type == "complex":
            return (
                os.environ.get("AZURE_OPENAI_COMPLEX_DEPLOYMENT")
                or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
                or "gpt41mini"
            )
        return (
            os.environ.get("AZURE_OPENAI_SIMPLE_DEPLOYMENT")
            or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
            or "gpt41mini"
        )

    async def generate_text(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        task_type: LLMTaskType = "simple",
        model: str | None = None,
        temperature: float = 0.2,
        timeout_seconds: float | None = None,
    ) -> str:
        selected_model = self.route_model(task_type=task_type, model=model)
        messages = self._build_messages(prompt, system_instruction)
        try:
            response = await self.client.chat.completions.create(
                model=selected_model,
                messages=messages,
                temperature=temperature,
            )
        except LLMServiceError:
            raise
        except Exception as error:  # noqa: BLE001 - normalize provider failures
            raise LLMServiceError(f"Azure OpenAI request failed: {error}") from error
        text = (response.choices[0].message.content or "").strip()
        if not text:
            raise LLMServiceError("Azure OpenAI returned an empty text response")
        return text

    async def stream_text(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        task_type: LLMTaskType = "simple",
        model: str | None = None,
        temperature: float = 0.2,
        timeout_seconds: float | None = None,
        output_schema: type[BaseModel] | None = None,
    ) -> AsyncIterator[str]:
        selected_model = self.route_model(task_type=task_type, model=model)
        user_prompt = prompt
        if output_schema is not None:
            user_prompt = (
                f"{prompt}\n\nReturn only a valid JSON object matching "
                f"{output_schema.__name__}."
            )
        messages = self._build_messages(user_prompt, system_instruction)
        try:
            stream = await self.client.chat.completions.create(
                model=selected_model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )
            emitted = False
            async for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    emitted = True
                    yield delta
            if not emitted:
                raise LLMServiceError("Azure OpenAI returned an empty text stream")
        except LLMServiceError:
            raise
        except Exception as error:  # noqa: BLE001 - normalize provider failures
            raise LLMServiceError(f"Azure OpenAI stream failed: {error}") from error

    async def generate_json(
        self,
        prompt: str,
        output_schema: type[SchemaT],
        *,
        system_instruction: str | None = None,
        task_type: LLMTaskType = "complex",
        model: str | None = None,
        temperature: float = 0.1,
        timeout_seconds: float | None = None,
        thinking_budget: int | None = None,
        operation: str | None = None,
    ) -> SchemaT:
        selected_model = self.route_model(task_type=task_type, model=model)
        schema_hint = self._schema_hint(output_schema)
        user_prompt = (
            f"{prompt.strip()}\n\n"
            "Respond with exactly one JSON object and no other text. Match the "
            "following JSON Schema exactly: use the listed enum values verbatim, "
            "include every required property, do NOT wrap the object in an outer "
            "key, and do NOT add properties that are not in the schema.\n"
            f"{schema_hint}"
        )
        messages = self._build_messages(user_prompt, system_instruction)
        last_error: Exception | None = None
        for _ in range(2):
            try:
                response = await self.client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                )
                text = response.choices[0].message.content or ""
                json_text = self._extract_json_object(text)
                return self._validate_schema(json_text, output_schema)
            except ValidationError as error:
                last_error = error
                self.logger.warning(
                    "Azure OpenAI JSON validation failed; retrying with raw response.",
                    extra={
                        "event": "llm.azure_json_validation_failed",
                        "output_schema": output_schema.__name__,
                        "validation_error": str(error)[:500],
                        "raw_response": text[:500],
                    },
                )
            except Exception as error:  # noqa: BLE001 - normalize provider failures
                raise LLMServiceError(
                    f"Azure OpenAI JSON request failed: {error}"
                ) from error
        raise LLMResponseValidationError(
            f"Could not produce valid {output_schema.__name__} JSON (schema_validation)"
        ) from last_error

    @staticmethod
    def _schema_hint(output_schema: type[BaseModel]) -> str:
        try:
            return json.dumps(output_schema.model_json_schema(), ensure_ascii=False)
        except Exception:
            return ""

    @staticmethod
    def _validate_schema(json_text: str, output_schema: type[SchemaT]) -> SchemaT:
        data = json.loads(json_text)
        try:
            return output_schema.model_validate(data)
        except ValidationError:
            # Some models wrap the object under a single outer key; unwrap it.
            if isinstance(data, dict) and len(data) == 1:
                only = next(iter(data.values()))
                if isinstance(only, dict):
                    return output_schema.model_validate(only)
            raise

    @staticmethod
    def _build_messages(prompt: str, system_instruction: str | None) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        return messages

    @staticmethod
    def _extract_json_object(text: str) -> str:
        content = (text or "").strip()
        content = re.sub(r"^```(?:json)?\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"\s*```$", "", content)
        start = content.find("{")
        if start < 0:
            raise ValueError("LLM response does not contain a JSON object")
        depth = 0
        in_string = False
        escape = False
        for index in range(start, len(content)):
            char = content[index]
            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return content[start : index + 1]
        raise ValueError("LLM response contains incomplete JSON")
