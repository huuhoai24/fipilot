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


class AzureOpenAIJsonClient:
    """Live Azure OpenAI / Foundry provider boundary."""

    def __init__(
        self,
        *,
        base_url: str = "https://hoai-openai-test-2026-55ac1.openai.azure.com/openai/v1/",
        api_key: str | None = None,
        max_attempts: int = 10,
        concurrency: int = 2,
    ) -> None:
        import os
        from openai import OpenAI

        resolved_api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        if not resolved_api_key:
            raise ValueError("AZURE_OPENAI_API_KEY is required for Azure OpenAI execution")
        self.client = OpenAI(
            base_url=base_url,
            api_key=resolved_api_key,
            timeout=90.0,
            max_retries=0,
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
    ) -> Any:
        import json
        schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False)
        full_sys_prompt = (
            (system_instruction or "")
            + f"\nYou MUST return ONLY a JSON object matching this schema:\n{schema_json}"
        )
        messages = [
            {"role": "system", "content": full_sys_prompt},
            {"role": "user", "content": prompt},
        ]

        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )

    def _normalize_dict(self, data: dict[str, Any], schema: type[SchemaT]) -> dict[str, Any]:
        schema_name = schema.__name__
        if schema_name == "GeneratedQuestion":
            if "primary_question" in data and "question" not in data:
                data["question"] = data["primary_question"]
            elif "interview_question" in data and "question" not in data:
                data["question"] = data["interview_question"]
            if "language" not in data:
                data["language"] = "vi"
            if "topic" not in data:
                data["topic"] = data.get("category", data.get("domain", data.get("focus_area", "General")))
            diff = str(data.get("difficulty", "medium")).lower()
            if diff not in ("easy", "medium", "hard"):
                diff = "medium"
            data["difficulty"] = diff
            if "expected_answer_points" not in data:
                data["expected_answer_points"] = data.get("key_points", data.get("expected_answers", []))
            if "follow_up_questions" not in data:
                data["follow_up_questions"] = data.get("follow_ups", [])
        elif schema_name == "QualityJudgment":
            for binary_key in ("technical_validity", "role_relevance", "cv_alignment", "answerability", "non_redundancy", "knowledge_false_premise"):
                val = data.get(binary_key)
                if val is True or val == "1" or val == 1:
                    data[binary_key] = 1
                elif val is False or val == "0" or val == 0:
                    data[binary_key] = 0
                else:
                    data[binary_key] = 1
            if "difficulty_label" not in data or data["difficulty_label"] not in ("Intern", "Junior", "Middle", "Senior"):
                data["difficulty_label"] = "Middle"
            if "difficulty_score" not in data:
                data["difficulty_score"] = 3
            if "clarity" not in data:
                data["clarity"] = 5
            if "specificity" not in data:
                data["specificity"] = 1
            if "rag_grounding" not in data:
                data["rag_grounding"] = 1
        return data

    async def generate_json(
        self,
        prompt: str,
        schema: type[SchemaT],
        *,
        model: str,
        temperature: float,
        system_instruction: str,
        thinking_budget: int | None = 0,
        timeout_seconds: float = 90.0,
    ) -> ProviderResult:
        import json
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
                        ),
                        timeout=timeout_seconds,
                    )
                    raw = str(response.choices[0].message.content or "")
                    extracted_str = self._extract_json(raw)
                    raw_dict = json.loads(extracted_str)
                    normalized = self._normalize_dict(raw_dict, schema)
                    parsed = schema.model_validate(normalized)
                    usage = getattr(response, "usage", None)
                    return ProviderResult(
                        parsed=parsed.model_dump(mode="json"),
                        raw_provider_output=raw,
                        usage={
                            "availability": (
                                "provider_reported" if usage else "unavailable"
                            ),
                            "input_tokens": getattr(usage, "prompt_tokens", None),
                            "output_tokens": getattr(usage, "completion_tokens", None),
                            "total_tokens": getattr(usage, "total_tokens", None),
                        },
                        latency_ms=(time.perf_counter() - started) * 1000,
                        model=model,
                    )
                except Exception as error:
                    last_error = error
                    if attempt == self.max_attempts:
                        break
                    is_rate_limit = "429" in str(error) or "rate_limit" in str(error).lower()
                    backoff = (
                        min(45.0, 5.0 + 3.0 * (1.5 ** (attempt - 1))) + random.uniform(1.0, 3.0)
                        if is_rate_limit
                        else min(10.0, 1.0 * (2 ** (attempt - 1))) + random.random() * 0.2
                    )
                    if is_rate_limit:
                        print(f"[RateLimit 429] Waiting {backoff:.1f}s before attempt {attempt + 1}/{self.max_attempts}...", flush=True)
                    await asyncio.sleep(backoff)
        raise RuntimeError(
            f"Provider call failed after {self.max_attempts} attempts"
        ) from last_error

