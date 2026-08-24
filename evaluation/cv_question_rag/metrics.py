from __future__ import annotations

import re
from collections import Counter
from typing import Any


TOKENS = re.compile(r"[a-z0-9+#.]+", re.IGNORECASE)
STOP = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "of",
    "in",
    "your",
    "you",
    "would",
    "how",
    "what",
}


def _normalize(value: str) -> str:
    return " ".join(TOKENS.findall(value.lower()))


def grounding_overlap(question: str, contexts: list[dict[str, Any]]) -> float:
    question_tokens = {
        token
        for token in TOKENS.findall(question.lower())
        if token not in STOP and len(token) > 2
    }
    context_tokens = {
        token
        for item in contexts
        for token in TOKENS.findall(
            f"{item.get('topic', '')} {item.get('content', '')}".lower()
        )
        if token not in STOP and len(token) > 2
    }
    return (
        len(question_tokens & context_tokens) / len(question_tokens)
        if question_tokens
        else 0.0
    )


def duplicate_statistics(questions: list[str]) -> dict[str, float]:
    normalized = [_normalize(value) for value in questions]
    counts = Counter(normalized)
    duplicate_outputs = sum(value - 1 for value in counts.values() if value > 1)
    openings = Counter(" ".join(value.split()[:4]) for value in normalized)
    repeated_openings = sum(value - 1 for value in openings.values() if value > 1)
    sample_count = len(questions)
    return {
        "normalized_exact_duplicate_rate": (
            duplicate_outputs / sample_count if sample_count else 0.0
        ),
        "opening_phrase_repetition_rate": (
            repeated_openings / sample_count if sample_count else 0.0
        ),
    }

