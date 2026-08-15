from __future__ import annotations

import math
import time
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel


VERTEX_STANDARD_PRICING_USD_PER_MILLION = {
    "gemini-2.5-flash": {"input": 0.30, "output": 2.50},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
}
PRICING_SOURCE = "https://cloud.google.com/vertex-ai/generative-ai/pricing"
PRICING_ACCESSED_AT = "2026-08-15"


def _estimated_tokens(characters: int) -> int:
    return math.ceil(max(characters, 0) / 4)


def estimate_visible_token_cost_usd(calls: list[dict[str, Any]]) -> float:
    total = 0.0
    for call in calls:
        if call.get("status") != "completed":
            continue
        prices = VERTEX_STANDARD_PRICING_USD_PER_MILLION.get(str(call.get("model")))
        if not prices:
            continue
        total += call.get("estimated_input_tokens", 0) / 1_000_000 * prices["input"]
        total += call.get("estimated_output_tokens", 0) / 1_000_000 * prices["output"]
    return total


class TrackingLLM:
    """Evaluation-only wrapper that records aggregate-safe logical call metadata."""

    def __init__(self, delegate: Any) -> None:
        self.delegate = delegate
        self.calls: list[dict[str, Any]] = []

    def route_model(self, task_type: str = "simple", model: str | None = None) -> str:
        return self.delegate.route_model(task_type=task_type, model=model)

    async def generate_json(
        self,
        prompt: str,
        output_schema: type[BaseModel],
        **kwargs: Any,
    ) -> BaseModel:
        started = time.perf_counter()
        task_type = kwargs.get("task_type", "complex")
        model = self.route_model(task_type=task_type, model=kwargs.get("model"))
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": kwargs.get("operation") or output_schema.__name__,
            "model": model,
            "task_type": task_type,
            "temperature": kwargs.get("temperature", 0.1),
            "prompt_chars": len(prompt),
            "estimated_input_tokens": _estimated_tokens(len(prompt)),
            "status": "failed",
        }
        try:
            result = await self.delegate.generate_json(prompt, output_schema, **kwargs)
            output_text = result.model_dump_json() if isinstance(result, BaseModel) else str(result)
            record.update(
                {
                    "status": "completed",
                    "output_chars": len(output_text),
                    "estimated_output_tokens": _estimated_tokens(len(output_text)),
                }
            )
            return result
        except Exception as exc:
            record["error_type"] = type(exc).__name__
            record["output_chars"] = 0
            record["estimated_output_tokens"] = 0
            raise
        finally:
            record["latency_ms"] = (time.perf_counter() - started) * 1000
            self.calls.append(record)

    async def generate_text(self, prompt: str, **kwargs: Any) -> str:
        return await self.delegate.generate_text(prompt, **kwargs)

    def stream_text(self, prompt: str, **kwargs: Any) -> Any:
        return self.delegate.stream_text(prompt, **kwargs)
