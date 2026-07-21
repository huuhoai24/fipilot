from __future__ import annotations

import asyncio
import json
import random
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from app.config.logging import get_logger
from app.config.settings import Settings, get_settings
from app.services.base_llm_service import BaseLLMService, LLMTaskType


SchemaT = TypeVar("SchemaT", bound=BaseModel)


class LLMServiceError(RuntimeError):
    """Base error for V2 LLM service failures."""


class LLMConfigurationError(LLMServiceError):
    """Raised when required provider configuration is missing."""


class LLMTimeoutError(LLMServiceError):
    """Raised when an LLM call exceeds its timeout."""


class LLMResponseValidationError(LLMServiceError):
    """Raised when JSON output cannot be validated."""


@dataclass(frozen=True)
class RetryConfig:
    max_attempts: int = 3
    initial_backoff_seconds: float = 0.5
    max_backoff_seconds: float = 4.0
    jitter_seconds: float = 0.1


class VertexGeminiService(BaseLLMService):
    """Gemini implementation backed by Vertex AI and Google ADC.

    Authentication is delegated to Google Application Default Credentials.
    For local development, run `gcloud auth application-default login`.
    On Cloud Run, attach a service account with Vertex AI permissions.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        *,
        client: Any | None = None,
        client_factory: Callable[[Settings], Any] | None = None,
        retry_config: RetryConfig | None = None,
        default_timeout_seconds: float = 60.0,
    ) -> None:
        self.settings = settings or get_settings()
        self._client = client
        self._client_factory = client_factory or self._create_default_client
        self.retry_config = retry_config or RetryConfig()
        self.default_timeout_seconds = default_timeout_seconds
        self.logger = get_logger(__name__)

    def route_model(self, task_type: LLMTaskType = "simple", model: str | None = None) -> str:
        if model:
            return model
        if task_type == "complex":
            return self.settings.llm_routing.complex_model
        return self.settings.llm_routing.simple_model

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
        response = await self._call_with_retry(
            selected_model,
            prompt,
            system_instruction=system_instruction,
            temperature=temperature,
            response_mime_type=None,
            timeout_seconds=timeout_seconds,
        )
        text = self._extract_text(response).strip()
        if not text:
            raise LLMServiceError("Gemini returned an empty text response")
        return text

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
    ) -> SchemaT:
        selected_model = self.route_model(task_type=task_type, model=model)
        schema_prompt = self._build_json_prompt(prompt, output_schema)
        last_error: Exception | None = None

        for attempt in range(1, self.retry_config.max_attempts + 1):
            try:
                response = await self._call_once_with_timeout(
                    selected_model,
                    schema_prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    response_mime_type="application/json",
                    timeout_seconds=timeout_seconds,
                )
                return self._validate_json_response(response, output_schema)
            except (ValidationError, ValueError, json.JSONDecodeError) as error:
                last_error = error
                if attempt >= self.retry_config.max_attempts:
                    break
                await self._sleep_before_retry(attempt)
            except Exception as error:
                last_error = error
                if attempt >= self.retry_config.max_attempts or not self._is_retryable_error(error):
                    break
                await self._sleep_before_retry(attempt)

        raise LLMResponseValidationError(f"Could not produce valid {output_schema.__name__} JSON") from last_error

    def _create_default_client(self, settings: Settings) -> Any:
        if not settings.google_cloud.project:
            raise LLMConfigurationError("GOOGLE_CLOUD_PROJECT is required for Vertex AI Gemini")

        try:
            from google import genai
        except ImportError as error:  # pragma: no cover - exercised through dependency installation
            raise LLMConfigurationError("google-genai is required for Vertex AI Gemini") from error

        return genai.Client(
            vertexai=True,
            project=settings.google_cloud.project,
            location=settings.google_cloud.location,
        )

    @property
    def client(self) -> Any:
        if self._client is None:
            self._client = self._client_factory(self.settings)
        return self._client

    async def _call_with_retry(
        self,
        model: str,
        prompt: str,
        *,
        system_instruction: str | None,
        temperature: float,
        response_mime_type: str | None,
        timeout_seconds: float | None,
    ) -> Any:
        last_error: Exception | None = None
        for attempt in range(1, self.retry_config.max_attempts + 1):
            try:
                return await self._call_once_with_timeout(
                    model,
                    prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    response_mime_type=response_mime_type,
                    timeout_seconds=timeout_seconds,
                )
            except Exception as error:
                last_error = error
                if attempt >= self.retry_config.max_attempts or not self._is_retryable_error(error):
                    break
                await self._sleep_before_retry(attempt)
        if isinstance(last_error, LLMTimeoutError):
            raise last_error
        raise LLMServiceError(f"Gemini call failed after {self.retry_config.max_attempts} attempts") from last_error

    async def _call_once_with_timeout(
        self,
        model: str,
        prompt: str,
        *,
        system_instruction: str | None,
        temperature: float,
        response_mime_type: str | None,
        timeout_seconds: float | None,
    ) -> Any:
        timeout = timeout_seconds or self.default_timeout_seconds
        try:
            return await asyncio.wait_for(
                asyncio.to_thread(
                    self._sync_generate_content,
                    model,
                    prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    response_mime_type=response_mime_type,
                ),
                timeout=timeout,
            )
        except TimeoutError as error:
            raise LLMTimeoutError(f"Gemini call exceeded {timeout:.1f}s timeout") from error

    def _sync_generate_content(
        self,
        model: str,
        prompt: str,
        *,
        system_instruction: str | None,
        temperature: float,
        response_mime_type: str | None,
    ) -> Any:
        config = self._build_generation_config(
            system_instruction=system_instruction,
            temperature=temperature,
            response_mime_type=response_mime_type,
        )
        kwargs = {"model": model, "contents": prompt}
        if config is not None:
            kwargs["config"] = config
        return self.client.models.generate_content(**kwargs)

    def _build_generation_config(
        self,
        *,
        system_instruction: str | None,
        temperature: float,
        response_mime_type: str | None,
    ) -> Any:
        config_values = {"temperature": temperature}
        if system_instruction:
            config_values["system_instruction"] = system_instruction
        if response_mime_type:
            config_values["response_mime_type"] = response_mime_type

        try:
            from google.genai import types

            return types.GenerateContentConfig(**config_values)
        except Exception:
            return config_values

    def _build_json_prompt(self, prompt: str, output_schema: type[BaseModel]) -> str:
        json_schema = output_schema.model_json_schema()
        return (
            f"{prompt.strip()}\n\n"
            "Return only one valid JSON object matching this JSON Schema. "
            "Do not include markdown, comments, or trailing text.\n\n"
            f"{json.dumps(json_schema, ensure_ascii=False)}"
        )

    def _validate_json_response(self, response: Any, output_schema: type[SchemaT]) -> SchemaT:
        text = self._extract_text(response)
        json_text = self._extract_json_object(text)
        return output_schema.model_validate_json(json_text)

    def _extract_text(self, response: Any) -> str:
        text = getattr(response, "text", None)
        if isinstance(text, str) and text:
            return text
        candidates = getattr(response, "candidates", None)
        if candidates:
            parts = []
            for candidate in candidates:
                content = getattr(candidate, "content", None)
                for part in getattr(content, "parts", []) or []:
                    part_text = getattr(part, "text", None)
                    if part_text:
                        parts.append(part_text)
            if parts:
                return "\n".join(parts)
        if isinstance(response, str):
            return response
        return str(response or "")

    def _extract_json_object(self, text: str) -> str:
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

    def _is_retryable_error(self, error: Exception) -> bool:
        if isinstance(error, LLMTimeoutError):
            return True
        status_code = getattr(error, "status_code", None) or getattr(error, "code", None)
        if status_code in {408, 409, 429, 500, 502, 503, 504}:
            return True
        text = str(error).lower()
        return any(marker in text for marker in ["timeout", "temporarily", "rate limit", "unavailable", "deadline"])

    async def _sleep_before_retry(self, attempt: int) -> None:
        base = min(
            self.retry_config.initial_backoff_seconds * (2 ** max(attempt - 1, 0)),
            self.retry_config.max_backoff_seconds,
        )
        jitter = random.uniform(0, self.retry_config.jitter_seconds) if self.retry_config.jitter_seconds else 0
        await asyncio.sleep(base + jitter)
