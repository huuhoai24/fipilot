"""Logging setup for V2 modules."""

from __future__ import annotations

import logging
import sys

from app.config.settings import Settings, get_settings


def setup_logging(settings: Settings | None = None) -> None:
    """Configure process logging for V2 code.

    This function is side-effect free until explicitly called by a future V2
    entrypoint, so it does not alter existing API behavior in Milestone 1.
    """

    active_settings = settings or get_settings()
    level = getattr(logging, active_settings.log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=False,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

