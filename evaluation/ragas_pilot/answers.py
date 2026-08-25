from __future__ import annotations

from typing import Any


QUALITY_ORDER = ["weak", "partial", "good", "strong"]


def build_controlled_answers(
    *,
    expected_points: list[str],
    language: str,
) -> list[dict[str, Any]]:
    points = [point.strip() for point in expected_points if point.strip()]
    first = points[0] if points else "the main technical requirement"
    all_points = "; ".join(points) if points else first
    if language == "vi":
        texts = {
            "weak": "Tôi chưa biết cách giải quyết và sẽ dùng mặc định mà không kiểm tra.",
            "partial": f"Tôi sẽ xem xét {first}, nhưng chưa phân tích các trade-off còn lại.",
            "good": (
                f"Tôi sẽ xử lý các điểm chính gồm {all_points}. "
                "Tôi sẽ kiểm tra kết quả và giải thích lựa chọn triển khai."
            ),
            "strong": (
                f"Tôi sẽ xử lý đầy đủ {all_points}; sau đó so sánh trade-off, "
                "đo kết quả, kiểm thử failure cases và nêu cách rollback hoặc cải tiến."
            ),
        }
    else:
        texts = {
            "weak": "I do not know how to solve this and would use defaults without validation.",
            "partial": f"I would consider {first}, but I cannot yet explain the remaining trade-offs.",
            "good": (
                f"I would address the main points: {all_points}. "
                "I would validate the result and explain the implementation choice."
            ),
            "strong": (
                f"I would address {all_points}; then compare trade-offs, measure the "
                "result, test failure cases, and explain rollback or improvement options."
            ),
        }
    return [
        {
            "quality_tier": tier,
            "source_type": "synthetic_controlled",
            "controlled_intent": (
                "ordinal behavior probe only; not a human score or reference answer"
            ),
            "quality_ladder_validated": False,
            "expected_quality_order": QUALITY_ORDER,
            "answer": texts[tier],
        }
        for tier in QUALITY_ORDER
    ]
