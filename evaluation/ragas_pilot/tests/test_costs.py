from __future__ import annotations

import pytest

from evaluation.ragas_pilot.tracking import estimate_visible_token_cost_usd


def test_cost_estimate_uses_recorded_vertex_standard_token_prices() -> None:
    calls = [
        {
            "model": "gemini-2.5-flash",
            "estimated_input_tokens": 1000,
            "estimated_output_tokens": 1000,
            "status": "completed",
        },
        {
            "model": "gemini-2.5-pro",
            "estimated_input_tokens": 1000,
            "estimated_output_tokens": 1000,
            "status": "completed",
        },
    ]

    assert estimate_visible_token_cost_usd(calls) == pytest.approx(0.01405)
