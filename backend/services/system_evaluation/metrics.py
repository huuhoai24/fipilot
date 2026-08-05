from __future__ import annotations

import math
import re
import unicodedata
from collections.abc import Iterable, Sequence
from typing import Any


_non_word = re.compile(r"[^\w]+", re.UNICODE)
_whitespace = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return _whitespace.sub(" ", normalized).strip()


def word_units(value: str) -> list[str]:
    return [unit for unit in _non_word.sub(" ", normalize_text(value)).split() if unit]


def character_units(value: str) -> list[str]:
    return list(normalize_text(value).replace(" ", ""))


def edit_distance(reference: Sequence[str], hypothesis: Sequence[str]) -> int:
    previous = list(range(len(hypothesis) + 1))
    for ref_index, reference_unit in enumerate(reference, start=1):
        current = [ref_index]
        for hyp_index, hypothesis_unit in enumerate(hypothesis, start=1):
            substitution = previous[hyp_index - 1] + (
                reference_unit != hypothesis_unit
            )
            current.append(
                min(
                    current[-1] + 1,
                    previous[hyp_index] + 1,
                    substitution,
                )
            )
        previous = current
    return previous[-1]


def error_counts(reference: str, hypothesis: str) -> tuple[int, int, int, int]:
    reference_words = word_units(reference)
    hypothesis_words = word_units(hypothesis)
    reference_characters = character_units(reference)
    hypothesis_characters = character_units(hypothesis)
    return (
        edit_distance(reference_words, hypothesis_words),
        len(reference_words),
        edit_distance(reference_characters, hypothesis_characters),
        len(reference_characters),
    )


def safe_rate(errors: int, reference_units: int) -> float:
    if reference_units == 0:
        return 0.0 if errors == 0 else 1.0
    return errors / reference_units


def normalized_skill_set(skills: Iterable[str]) -> set[str]:
    return {normalize_text(skill) for skill in skills if normalize_text(skill)}


def skill_counts(
    expected_skills: Iterable[str], predicted_skills: Iterable[str]
) -> tuple[int, int, int]:
    expected = normalized_skill_set(expected_skills)
    predicted = normalized_skill_set(predicted_skills)
    return len(expected & predicted), len(predicted), len(expected)


def precision_recall_f1(
    true_positive: int,
    predicted_count: int,
    expected_count: int,
) -> tuple[float, float, float]:
    precision = true_positive / predicted_count if predicted_count else 0.0
    recall = true_positive / expected_count if expected_count else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return precision, recall, f1


def values_match(actual: Any, expected: Any) -> bool:
    if isinstance(expected, str):
        return isinstance(actual, str) and normalize_text(actual) == normalize_text(expected)
    if isinstance(expected, (int, float)) and not isinstance(expected, bool):
        return (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and math.isclose(float(actual), float(expected), abs_tol=0.25)
        )
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        if all(isinstance(item, str) for item in expected + actual):
            return normalized_skill_set(actual) == normalized_skill_set(expected)
        return actual == expected
    return actual == expected


def profile_field_counts(
    actual_profile: dict[str, Any], expected_fields: dict[str, Any]
) -> tuple[int, int]:
    correct = sum(
        values_match(actual_profile.get(field_name), expected_value)
        for field_name, expected_value in expected_fields.items()
    )
    return correct, len(expected_fields)


def average(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def percentile(values: Sequence[float], percentile_value: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * percentile_value
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def mean_absolute_deviation(values: Sequence[float]) -> float | None:
    mean = average(values)
    if mean is None:
        return None
    return sum(abs(value - mean) for value in values) / len(values)
