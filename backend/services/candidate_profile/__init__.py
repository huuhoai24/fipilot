"""Candidate Profile domain behavior."""

from services.candidate_profile.normalization import (
    normalize_profile_text,
    normalized_comparison_key,
)
from services.candidate_profile.readiness import evaluate_interview_readiness

__all__ = [
    "evaluate_interview_readiness",
    "normalize_profile_text",
    "normalized_comparison_key",
]
