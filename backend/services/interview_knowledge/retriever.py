from __future__ import annotations

from typing import Protocol

from shared.schemas import CandidateProfile, InterviewConfig


class KnowledgeRetriever(Protocol):
    """Select bounded interview guidance from the packaged knowledge catalog."""

    def retrieve_topics(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig,
    ) -> list[str]:
        """Return relevant topic names without changing interview state."""
        ...
