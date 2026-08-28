from __future__ import annotations

import json
import os
import re
from typing import Any

from pydantic import BaseModel, ValidationError

from core.logging import get_logger
from infrastructure.llm.base import BaseLLMService, LLMTaskType, SchemaT
from infrastructure.llm.exceptions import (
    LLMConfigurationError,
    LLMResponseValidationError,
    LLMServiceError,
)


class AzureOpenAIService(BaseLLMService):
    """OpenAI-compatible LLM backend (Azure OpenAI, OpenAI, or local endpoints)."""

    def __init__(
        self,
        *,
        default_timeout_seconds: float = 60.0,
    ) -> None:
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

        base_url = (
            os.environ.get("AZURE_OPENAI_BASE_URL")
            or os.environ.get("AZURE_FOUNDRY_ENDPOINT")
            or os.environ.get("OPENAI_BASE_URL")
        )
        api_key = (
            os.environ.get("AZURE_OPENAI_API_KEY")
            or os.environ.get("AZURE_FOUNDRY_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )
        if not api_key:
            raise LLMConfigurationError(
                "AZURE_OPENAI_API_KEY or OPENAI_API_KEY is required for the LLM provider"
            )
        kwargs: dict[str, Any] = {
            "api_key": api_key,
            "timeout": self.default_timeout_seconds,
        }
        if base_url:
            kwargs["base_url"] = base_url
        return AsyncOpenAI(**kwargs)

    def route_model(self, task_type: LLMTaskType = "simple", model: str | None = None) -> str:
        if model:
            return model
        if task_type == "complex":
            return (
                os.environ.get("AZURE_OPENAI_COMPLEX_DEPLOYMENT")
                or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
                or os.environ.get("AZURE_MODEL_NAME")
                or os.environ.get("OPENAI_MODEL")
                or "gpt-4o-mini"
            )
        return (
            os.environ.get("AZURE_OPENAI_SIMPLE_DEPLOYMENT")
            or os.environ.get("AZURE_OPENAI_DEPLOYMENT")
            or os.environ.get("AZURE_MODEL_NAME")
            or os.environ.get("OPENAI_MODEL")
            or "gpt-4o-mini"
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
        except Exception as error:
            raise LLMServiceError(f"OpenAI request failed: {error}") from error
        text = (response.choices[0].message.content or "").strip()
        if not text:
            raise LLMServiceError("OpenAI returned an empty text response")
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
                    "OpenAI JSON validation failed; retrying with raw response."
                )
            except Exception as error:
                raise LLMServiceError(
                    f"OpenAI JSON request failed: {error}"
                ) from error
        raise LLMResponseValidationError(
            f"Could not produce valid {output_schema.__name__} JSON"
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

    async def generate_embedding(self, text: str, model: str | None = None) -> list[float]:
        selected_model = model or os.environ.get("AZURE_EMBEDDING_MODEL") or "text-embedding-3-small"
        
        # Try to use a dedicated embedding client if AZURE_FOUNDRY_ENDPOINT is set
        # This handles the case where GPT models are on one Azure resource 
        # but Embedding models are on another (e.g. Foundry).
        embedding_client = self.client
        foundry_endpoint = os.environ.get("AZURE_FOUNDRY_ENDPOINT")
        foundry_key = os.environ.get("AZURE_FOUNDRY_API_KEY")
        
        if foundry_endpoint and foundry_key:
            from openai import AsyncOpenAI
            # Replace .services.ai.azure.com with .openai.azure.com/openai/v1/ if needed for standard API
            base_url = foundry_endpoint
            if "services.ai.azure.com" in base_url and "openai/v1" not in base_url:
                base_url = base_url.replace("services.ai.azure.com", "openai.azure.com/openai/v1/")
                
            embedding_client = AsyncOpenAI(
                api_key=foundry_key,
                base_url=base_url,
                timeout=self.default_timeout_seconds,
            )

        try:
            response = await embedding_client.embeddings.create(
                input=text,
                model=selected_model,
                timeout=self.default_timeout_seconds,
            )
            return response.data[0].embedding
        except Exception as e:
            self.logger.error("Failed to generate embedding: %s", e, exc_info=True)
            raise
