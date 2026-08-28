from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Literal, TypeVar

from pydantic import BaseModel


LLMTaskType = Literal["simple", "complex"]
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class BaseLLMService(ABC):
    """Interface used by agents to call an LLM provider."""

    @abstractmethod
    def route_model(self, task_type: LLMTaskType = "simple", model: str | None = None) -> str:
        """Return the provider model name for a task."""

    @abstractmethod
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
        """Generate plain text from a prompt."""

    @abstractmethod
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
        """Generate JSON and validate it with a Pydantic schema."""

    @abstractmethod
    async def generate_embedding(self, text: str, model: str | None = None) -> list[float]:
        """Generate a vector embedding for the given text."""
