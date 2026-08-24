from __future__ import annotations


QUESTION_BUDGET_USD = 3.0
QUESTION_HARD_CEILING_USD = 5.0
PRICES_PER_MILLION = {
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.0},
    "gemini-embedding-001": {"input": 0.15, "output": 0.0},
}


class BudgetExceeded(RuntimeError):
    pass


def _model_cost(
    model: str, calls: int, input_tokens: int, output_tokens: int
) -> dict:
    prices = PRICES_PER_MILLION[model]
    cost = (
        input_tokens / 1_000_000 * prices["input"]
        + output_tokens / 1_000_000 * prices["output"]
    )
    return {
        "calls": calls,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": cost,
    }


def estimate_cost(
    *,
    base_scenarios: int,
    question_calls: int,
    judge_calls: int,
    repeatability_calls: int,
    embedding_calls: int,
    cached_calls: int,
    flash_input_tokens: int,
    flash_output_tokens: int,
    pro_input_tokens: int,
    pro_output_tokens: int,
    embedding_input_tokens: int,
) -> dict:
    costs = {
        "gemini-2.5-flash": _model_cost(
            "gemini-2.5-flash",
            question_calls + repeatability_calls,
            flash_input_tokens,
            flash_output_tokens,
        ),
        "gemini-2.5-pro": _model_cost(
            "gemini-2.5-pro", judge_calls, pro_input_tokens, pro_output_tokens
        ),
        "gemini-embedding-001": _model_cost(
            "gemini-embedding-001", embedding_calls, embedding_input_tokens, 0
        ),
    }
    total = sum(value["estimated_cost_usd"] for value in costs.values())
    if total > QUESTION_HARD_CEILING_USD:
        raise BudgetExceeded(
            f"QUESTION BUDGET GATE BLOCKED: ${total:.4f} exceeds "
            f"${QUESTION_HARD_CEILING_USD:.2f}"
        )
    return {
        "base_scenarios": base_scenarios,
        "question_generator_calls": question_calls,
        "judge_calls": judge_calls,
        "repeatability_calls": repeatability_calls,
        "query_embedding_calls": embedding_calls,
        "cached_calls": cached_calls,
        "estimated_input_tokens": (
            flash_input_tokens + pro_input_tokens + embedding_input_tokens
        ),
        "estimated_output_tokens": flash_output_tokens + pro_output_tokens,
        "cost_by_model": costs,
        "total_estimated_cost_usd": total,
        "budget_usd": QUESTION_BUDGET_USD,
        "hard_ceiling_usd": QUESTION_HARD_CEILING_USD,
        "budget_status": (
            "PASS" if total <= QUESTION_BUDGET_USD else "WITHIN_HARD_CEILING"
        ),
    }

