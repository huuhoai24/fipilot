from __future__ import annotations

import asyncio
import hashlib
import json
import time
from collections import OrderedDict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from core.logging import get_logger
from core.performance import log_duration
from shared.schemas import InterviewConfig, InterviewPlan, PersistedCandidateProfile


PreparationFactory = Callable[[], Awaitable[InterviewPlan]]
logger = get_logger(__name__)
INTERVIEW_BLUEPRINT_VERSION = "interview-blueprint-v2"


@dataclass(frozen=True)
class _PreparedEntry:
    plan: InterviewPlan
    expires_at: float


class InterviewPreparationCache:
    """Deduplicates stable blueprints; generated questions are never cached."""

    def __init__(self, *, ttl_seconds: float = 300.0, max_entries: int = 128) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._ready: OrderedDict[str, _PreparedEntry] = OrderedDict()
        self._inflight: dict[str, asyncio.Task[InterviewPlan]] = {}

    def key_for(
        self,
        user_id: str,
        candidate_profile: PersistedCandidateProfile,
        interview_config: InterviewConfig,
    ) -> str:
        config_json = json.dumps(
            interview_config.model_dump(mode="json"),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
        fingerprint = hashlib.sha256(config_json.encode("utf-8")).hexdigest()
        key_material = ":".join(
            (
                INTERVIEW_BLUEPRINT_VERSION,
                user_id,
                candidate_profile.candidate_id,
                str(candidate_profile.profile_version),
                fingerprint,
            )
        )
        return hashlib.sha256(key_material.encode("utf-8")).hexdigest()

    async def get_or_create(
        self,
        key: str,
        factory: PreparationFactory,
    ) -> InterviewPlan:
        started_at = time.perf_counter()
        self._remove_expired()
        cached = self._ready.get(key)
        if cached is not None:
            self._ready.move_to_end(key)
            log_duration(
                logger,
                "interview.preparation_cache",
                started_at,
                status="ready_hit",
                stage="interview_blueprint",
                cache_hit=True,
            )
            return cached.plan.model_copy(deep=True)

        task = self._inflight.get(key)
        cache_status = "inflight_hit" if task is not None else "miss"
        if task is None:
            task = asyncio.create_task(factory())
            self._inflight[key] = task
            task.add_done_callback(
                lambda completed, preparation_key=key: self._store_completed(
                    preparation_key,
                    completed,
                )
            )

        state = await asyncio.shield(task)
        log_duration(
            logger,
            "interview.preparation_cache",
            started_at,
            status=cache_status,
            stage="interview_blueprint",
            cache_hit=cache_status != "miss",
        )
        return state.model_copy(deep=True)

    def clear(self) -> None:
        for task in self._inflight.values():
            task.cancel()
        self._inflight.clear()
        self._ready.clear()

    def _store_completed(
        self,
        key: str,
        task: asyncio.Task[InterviewPlan],
    ) -> None:
        if self._inflight.get(key) is not task:
            return
        self._inflight.pop(key, None)
        if task.cancelled():
            return
        try:
            state = task.result()
        except BaseException:
            return

        self._ready[key] = _PreparedEntry(
            plan=state.model_copy(deep=True),
            expires_at=time.monotonic() + self.ttl_seconds,
        )
        self._ready.move_to_end(key)
        while len(self._ready) > self.max_entries:
            self._ready.popitem(last=False)

    def _remove_expired(self) -> None:
        now = time.monotonic()
        expired = [
            key
            for key, entry in self._ready.items()
            if entry.expires_at <= now
        ]
        for key in expired:
            self._ready.pop(key, None)
