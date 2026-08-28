from __future__ import annotations

import hashlib
import time
from collections import OrderedDict
from dataclasses import dataclass

from shared.schemas import CandidateProfile


RESUME_EXTRACTION_VERSION = "resume-extraction-v2"


@dataclass(frozen=True)
class _ProcessedResumeEntry:
    profile: CandidateProfile
    expires_at: float


class ProcessedResumeCache:
    """Bounded cache of extracted profiles for unchanged owned Resume content."""

    def __init__(self, *, ttl_seconds: float = 3600.0, max_entries: int = 256) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._entries: OrderedDict[str, _ProcessedResumeEntry] = OrderedDict()

    def get(
        self,
        user_id: str,
        content_hash: str,
        extraction_version: str = RESUME_EXTRACTION_VERSION,
    ) -> CandidateProfile | None:
        key = self.key_for(user_id, content_hash, extraction_version)
        entry = self._entries.get(key)
        if entry is None:
            return None
        if entry.expires_at <= time.monotonic():
            self._entries.pop(key, None)
            return None
        self._entries.move_to_end(key)
        return entry.profile.model_copy(deep=True)

    def store(
        self,
        user_id: str,
        content_hash: str,
        profile: CandidateProfile,
        extraction_version: str = RESUME_EXTRACTION_VERSION,
    ) -> None:
        key = self.key_for(user_id, content_hash, extraction_version)
        self._entries[key] = _ProcessedResumeEntry(
            profile=profile.model_copy(deep=True),
            expires_at=time.monotonic() + self.ttl_seconds,
        )
        self._entries.move_to_end(key)
        while len(self._entries) > self.max_entries:
            self._entries.popitem(last=False)

    @staticmethod
    def key_for(user_id: str, content_hash: str, extraction_version: str) -> str:
        key_material = f"{extraction_version}:{user_id}:{content_hash}"
        return hashlib.sha256(key_material.encode("utf-8")).hexdigest()
