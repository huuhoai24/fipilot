from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from shared.language import normalize_language


VIETNAMESE_INTERVIEW_INSTRUCTION = """
The interview language is Vietnamese.

Rules:
- Ask questions in Vietnamese.
- Provide feedback in Vietnamese.
- Keep technical terms such as YOLO, PyTorch, TensorRT, FastAPI in English.
- Do not translate programming concepts.
""".strip()


ENGLISH_INTERVIEW_INSTRUCTION = """
The interview language is English.

Rules:
- Ask questions in English.
- Provide feedback in English.
- Keep technical terms unchanged.
""".strip()


def get_language_instruction(language: str) -> str:
    normalized = normalize_language(language)
    if normalized == "vi":
        return VIETNAMESE_INTERVIEW_INSTRUCTION
    return ENGLISH_INTERVIEW_INSTRUCTION


def build_agent_prompt(
    *,
    task: str,
    language: str,
    context: BaseModel | dict[str, Any] | str,
    system_instruction: str = "",
    agent_task: str = "",
) -> str:
    context_text = _format_context(context)
    sections = [
        ("System instruction", system_instruction.strip()),
        ("Language instruction", get_language_instruction(language)),
        ("Task", task),
        ("Agent task", agent_task.strip()),
        ("Context", context_text),
    ]
    return "\n\n".join(f"{title}:\n{body}" for title, body in sections if body)


def _format_context(context: BaseModel | dict[str, Any] | str) -> str:
    if isinstance(context, BaseModel):
        return context.model_dump_json()
    if isinstance(context, dict):
        import json

        return json.dumps(context, ensure_ascii=False)
    return str(context)

