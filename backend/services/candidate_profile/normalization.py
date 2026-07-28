from __future__ import annotations

import unicodedata


def normalize_profile_text(value: str | None) -> str:
    """Apply the shared Candidate Profile text normalization contract."""
    if value is None:
        return ""
    return " ".join(unicodedata.normalize("NFKC", value).split())


def normalized_comparison_key(value: str | None) -> str:
    """Return the shared case-insensitive key for skills and references."""
    return normalize_profile_text(value).casefold()
