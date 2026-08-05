from __future__ import annotations

import contextvars
import json
import logging
import re
import sys
import traceback
from datetime import datetime, timezone
from typing import Any

from core.settings import Settings, get_settings


_request_id_context: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)
_email_pattern = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
_bearer_pattern = re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]+=*", re.IGNORECASE)
_structured_fields = (
    "event",
    "request_id",
    "session_id",
    "duration_ms",
    "status",
    "speech_to_stt_final_ms",
    "audio_queue_drain_ms",
    "stt_decode_ms",
    "stt_to_evaluation_ms",
    "evaluation_to_question_ms",
    "question_to_tts_first_audio_ms",
    "total_turn_latency_ms",
    "status_code",
    "method",
    "path",
)


class StructuredJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": record.levelname,
            "logger": record.name,
            "message": _redact(record.getMessage()),
        }
        for field in _structured_fields:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        payload.setdefault("request_id", get_request_id())
        if record.exc_info:
            exc_type, exc_value, _ = record.exc_info
            payload["exception"] = exc_type.__name__ if exc_type else "Exception"
            # Keep the message and stack: recording only the class name made
            # production failures effectively undebuggable.
            payload["exception_message"] = _redact(str(exc_value or ""))
            payload["stacktrace"] = _redact(
                "".join(traceback.format_exception(*record.exc_info))
            )
        return json.dumps(payload, ensure_ascii=True, default=str)


def setup_logging(settings: Settings | None = None) -> None:
    active_settings = settings or get_settings()
    level = getattr(logging, active_settings.log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredJsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)

    for logger_name in ("uvicorn", "uvicorn.error", "fastapi"):
        framework_logger = logging.getLogger(logger_name)
        framework_logger.handlers.clear()
        framework_logger.setLevel(level)
        framework_logger.propagate = True

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    access_logger.disabled = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def set_request_id(request_id: str) -> contextvars.Token:
    return _request_id_context.set(request_id)


def reset_request_id(token: contextvars.Token) -> None:
    _request_id_context.reset(token)


def get_request_id() -> str | None:
    return _request_id_context.get()


def _redact(message: str) -> str:
    message = _email_pattern.sub("[redacted-email]", message)
    return _bearer_pattern.sub("Bearer [redacted]", message)
