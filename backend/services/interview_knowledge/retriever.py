from __future__ import annotations

from typing import Protocol

from shared.schemas import CandidateProfile, InterviewConfig


class KnowledgeRetriever(Protocol):
    """Future seam for selecting interview topics from curated knowledge."""

    def retrieve_topics(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig,
    ) -> list[str]:
        """Return relevant topic names without changing interview state."""
        ...
