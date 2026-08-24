from __future__ import annotations

import asyncio
import random
import re
import time
from dataclasses import dataclass
from typing import Any, TypeVar

from pydantic import BaseModel


SchemaT = TypeVar("SchemaT", bound=BaseModel)


@dataclass(frozen=True)
class ProviderResult:
    parsed: dict[str, Any]
    raw_provider_output: str
    usage: dict[str, int | str | None]
    latency_ms: float
    model: str


class VertexJsonClient:
    """Narrow live provider boundary; tests replace the whole boundary."""

    def __init__(
        self,
        *,
        project: str,
        location: str = "global",
        max_attempts: int = 3,
        concurrency: int = 6,
    ) -> None:
        if not project:
            raise ValueError("GOOGLE_CLOUD_PROJECT is required for paid execution")
        from google import genai

        self.client = genai.Client(
            vertexai=True, project=project, location=location
        )
        self.max_attempts = max_attempts
        self.semaphore = asyncio.Semaphore(concurrency)

    @staticmethod
    def _extract_json(text: str) -> str:
        content = re.sub(
            r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE
        )
        start = content.find("{")
        if start < 0:
            raise ValueError("Provider output contains no JSON object")
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
            elif char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return content[start : index + 1]
        raise ValueError("Provider output contains incomplete JSON")

    def _call(
        self,
        prompt: str,
        schema: type[SchemaT],
        *,
        model: str,
        temperature: float,
        system_instruction: str,
        thinking_budget: int | None,
    ) -> Any:
        from google.genai import types

        config_values: dict[str, Any] = {
            "temperature": temperature,
            "system_instruction": system_instruction,
            "response_mime_type": "application/json",
            "response_json_schema": schema.model_json_schema(),
        }
        if thinking_budget is not None:
            config_values["thinking_config"] = types.ThinkingConfig(
                thinking_budget=thinking_budget
            )
        return self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_values),
        )

    async def generate_json(
        self,
        prompt: str,
        schema: type[SchemaT],
        *,
        model: str,
        temperature: float,
        system_instruction: str,
        thinking_budget: int | None = 0,
        timeout_seconds: float = 60.0,
    ) -> ProviderResult:
        last_error: Exception | None = None
        async with self.semaphore:
            for attempt in range(1, self.max_attempts + 1):
                started = time.perf_counter()
                try:
                    response = await asyncio.wait_for(
                        asyncio.to_thread(
                            self._call,
                            prompt,
                            schema,
                            model=model,
                            temperature=temperature,
                            system_instruction=system_instruction,
                            thinking_budget=thinking_budget,
                        ),
                        timeout=timeout_seconds,
                    )
                    raw = str(getattr(response, "text", "") or "")
                    parsed = schema.model_validate_json(self._extract_json(raw))
                    usage = getattr(response, "usage_metadata", None)
                    return ProviderResult(
                        parsed=parsed.model_dump(mode="json"),
                        raw_provider_output=raw,
                        usage={
                            "availability": (
                                "provider_reported" if usage else "unavailable"
                            ),
                            "input_tokens": getattr(
                                usage, "prompt_token_count", None
                            ),
                            "output_tokens": getattr(
                                usage, "candidates_token_count", None
                            ),
                            "total_tokens": getattr(usage, "total_token_count", None),
                        },
                        latency_ms=(time.perf_counter() - started) * 1000,
                        model=model,
                    )
                except Exception as error:
                    last_error = error
                    if attempt == self.max_attempts:
                        break
                    await asyncio.sleep(
                        min(4.0, 0.5 * (2 ** (attempt - 1)))
                        + random.random() * 0.1
                    )
        raise RuntimeError(
            f"Provider call failed after {self.max_attempts} attempts"
        ) from last_error

