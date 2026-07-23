from __future__ import annotations

import re
import time
from uuid import uuid4

from fastapi import Request

from core.logging import get_logger, reset_request_id, set_request_id


logger = get_logger(__name__)
_request_id_pattern = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
_session_path_pattern = re.compile(r"/api/v2/interview/([^/]+)")


async def request_correlation_middleware(request: Request, call_next):
    supplied_request_id = request.headers.get("X-Request-ID", "")
    request_id = (
        supplied_request_id
        if _request_id_pattern.fullmatch(supplied_request_id)
        else str(uuid4())
    )
    context_token = set_request_id(request_id)
    request.state.request_id = request_id
    started_at = time.perf_counter()
    session_match = _session_path_pattern.search(request.url.path)
    session_id = session_match.group(1) if session_match else None
    try:
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "HTTP request completed",
            extra={
                "event": "http_request_completed",
                "request_id": request_id,
                "session_id": session_id,
                "duration_ms": duration_ms,
                "status_code": response.status_code,
                "method": request.method,
                "path": request.url.path,
            },
        )
        return response
    except Exception:
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.exception(
            "HTTP request failed",
            extra={
                "event": "http_request_failed",
                "request_id": request_id,
                "session_id": session_id,
                "duration_ms": duration_ms,
                "status_code": 500,
                "method": request.method,
                "path": request.url.path,
            },
        )
        raise
    finally:
        reset_request_id(context_token)
