from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.settings import get_settings
from infrastructure.llm.vertex_gemini import RetryConfig, VertexGeminiService
from pydantic import BaseModel


RAW_RESPONSE_LIMITATION = (
    "Unavailable: BaseLLMService.generate_json returns only the validated model; "
    "the provider raw response is not exposed."
)


def read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as input_file:
        payload = json.load(input_file)
    if not isinstance(payload, dict):
        raise ValueError("AI Lab input must be a JSON object")
    return payload


def create_llm_service(*, resume_route: bool = False) -> VertexGeminiService:
    settings = get_settings()
    if not resume_route:
        return VertexGeminiService(settings=settings)

    resume_settings = settings.model_copy(
        update={
            "google_cloud": settings.google_cloud.model_copy(
                update={"location": settings.gemini_resume_location}
            ),
            "llm_routing": settings.llm_routing.model_copy(
                update={"simple_model": settings.gemini_resume_model}
            ),
        }
    )
    return VertexGeminiService(
        settings=resume_settings,
        retry_config=RetryConfig(max_attempts=1),
    )


def utc_timestamp() -> datetime:
    return datetime.now(timezone.utc)


def create_run_directory(root: str | Path, timestamp: datetime) -> Path:
    run_directory = Path(root) / timestamp.strftime("%Y%m%dT%H%M%S.%fZ")
    run_directory.mkdir(parents=True, exist_ok=False)
    return run_directory


def write_artifacts(
    run_directory: Path,
    *,
    input_payload: dict[str, Any],
    prompt: str,
    output: BaseModel | None,
    ai: str,
    model: str,
    task_type: str,
    temperature: float,
    timestamp: datetime,
    success: bool,
    error: str | None = None,
) -> None:
    output_payload = output.model_dump(mode="json") if output is not None else None
    metadata = {
        "ai": ai,
        "model": model,
        "task_type": task_type,
        "temperature": temperature,
        "timestamp": timestamp.isoformat(),
        "success": success,
        "raw_response_captured": False,
    }
    if error is not None:
        metadata["error"] = error

    _write_json(run_directory / "input.json", input_payload)
    (run_directory / "prompt.txt").write_text(prompt, encoding="utf-8")
    (run_directory / "raw_response.txt").write_text(
        RAW_RESPONSE_LIMITATION,
        encoding="utf-8",
    )
    _write_json(run_directory / "output.json", output_payload)
    _write_json(run_directory / "metadata.json", metadata)


def print_output(output: BaseModel) -> None:
    print(json.dumps(output.model_dump(mode="json"), ensure_ascii=False, indent=2))


def validate_temperature(value: float) -> float:
    if not 0.0 <= value <= 2.0:
        raise ValueError("temperature must be between 0.0 and 2.0")
    return value


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
