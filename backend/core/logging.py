from __future__ import annotations

import contextvars
import json
import logging
import re
import sys
import traceback
from datetime import datetime, timezone
from typing import Any

_request_id_context: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)
_email_pattern = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
_bearer_pattern = re.compile(r"Bearer\s+[A-Za-z0-9._~+/-]+=*", re.IGNORECASE)
_structured_fields = (
    "event",
    "stage",
    "model",
    "task_type",
    "operation",
    "output_schema",
    "prompt_chars",
    "response_chars",
    "attempt",
    "retry_max_attempts",
    "temperature",
    "timeout_seconds",
    "thinking_budget",
    "cache_hit",
    "request_id",
    "session_id",
    "duration_ms",
    "status",
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
            payload["exception_message"] = _redact(str(exc_value or ""))
            payload["stacktrace"] = _redact(
                "".join(traceback.format_exception(*record.exc_info))
            )
        return json.dumps(payload, ensure_ascii=True, default=str)


def setup_logging(log_level: str = "INFO") -> None:
    level = getattr(logging, log_level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredJsonFormatter())
    logging.basicConfig(level=level, handlers=[handler], force=True)


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
