from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


def log_duration(
    logger: logging.Logger,
    event: str,
    started_at: float,
    *,
    status: str = "complete",
    **fields: Any,
) -> None:
    logger.info(
        "Pipeline stage measured.",
        extra={
            "event": event,
            "duration_ms": round((time.perf_counter() - started_at) * 1000, 2),
            "status": status,
            **fields,
        },
    )


@contextmanager
def timed_stage(
    logger: logging.Logger,
    event: str,
    *,
    stage: str | None = None,
    **fields: Any,
) -> Iterator[None]:
    started_at = time.perf_counter()
    status = "complete"
    try:
        yield
    except BaseException:
        status = "failed"
        raise
    finally:
        log_duration(
            logger,
            event,
            started_at,
            status=status,
            stage=stage,
            **fields,
        )
