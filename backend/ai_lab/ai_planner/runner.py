from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

from ai_lab._runtime import create_llm_service, create_run_directory, print_output, read_json, utc_timestamp, validate_temperature, write_artifacts
from ai_lab.ai_planner.agent import PlannerLabAgent
from ai_lab.ai_planner.prompt import build_prompt
from ai_lab.ai_planner.schemas import InterviewPlan, PlannerInput


DEFAULT_RUNS_DIR = Path(__file__).with_name("runs")
TEST_DIR = Path(__file__).with_name("test")


def parse_input(path: str | Path) -> PlannerInput:
    return PlannerInput.model_validate(read_json(path))


def _write_json(path: Path, data: dict) -> None:
    """Write a dict as pretty-printed JSON to *path*."""
    import json
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _save_test_artifacts(input_payload: dict, output: InterviewPlan) -> None:
    """Save input/output of the latest run into ai_planner/test/."""
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    _write_json(TEST_DIR / "input.json", input_payload)
    _write_json(TEST_DIR / "output.json", output.model_dump(mode="json"))


async def run(input_path: str | Path, *, model: str | None = None, temperature: float = PlannerLabAgent.TEMPERATURE, runs_dir: str | Path = DEFAULT_RUNS_DIR) -> InterviewPlan:
    temperature = validate_temperature(temperature)
    input_data = parse_input(input_path)
    payload = input_data.model_dump(mode="json")
    prompt = build_prompt(input_data)
    llm = create_llm_service()
    selected_model = llm.route_model(task_type=PlannerLabAgent.TASK_TYPE, model=model)
    timestamp = utc_timestamp()
    directory = create_run_directory(runs_dir, timestamp)
    try:
        output = await PlannerLabAgent(llm).run(input_data, prompt=prompt, model=model, temperature=temperature)
        output = InterviewPlan.model_validate(output.model_dump(mode="json"))
    except Exception as error:
        write_artifacts(directory, input_payload=payload, prompt=prompt, output=None, ai="ai_planner", model=selected_model, task_type=PlannerLabAgent.TASK_TYPE, temperature=temperature, timestamp=timestamp, success=False, error=f"{type(error).__name__}: {error}")
        raise
    write_artifacts(directory, input_payload=payload, prompt=prompt, output=output, ai="ai_planner", model=selected_model, task_type=PlannerLabAgent.TASK_TYPE, temperature=temperature, timestamp=timestamp, success=True)
    _save_test_artifacts(payload, output)
    print_output(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the standalone Interview Planner lab")
    parser.add_argument("input")
    parser.add_argument("--model")
    parser.add_argument("--temperature", type=float, default=PlannerLabAgent.TEMPERATURE)
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR))
    args = parser.parse_args()
    asyncio.run(run(args.input, model=args.model, temperature=args.temperature, runs_dir=args.runs_dir))


if __name__ == "__main__":
    main()
