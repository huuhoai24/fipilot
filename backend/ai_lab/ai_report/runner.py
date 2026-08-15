from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from ai_lab._runtime import create_llm_service, create_run_directory, print_output, read_json, utc_timestamp, validate_temperature, write_artifacts
from ai_lab.ai_report.agent import ReportLabAgent
from ai_lab.ai_report.prompt import build_prompt
from ai_lab.ai_report.schemas import InterviewReport, ReportInput


DEFAULT_RUNS_DIR = Path(__file__).with_name("runs")


def parse_input(path: str | Path) -> ReportInput:
    return ReportInput.model_validate(read_json(path))


async def run(input_path: str | Path, *, model: str | None = None, temperature: float = ReportLabAgent.TEMPERATURE, runs_dir: str | Path = DEFAULT_RUNS_DIR) -> InterviewReport:
    temperature = validate_temperature(temperature)
    input_data = parse_input(input_path)
    payload = input_data.model_dump(mode="json")
    prompt = build_prompt(input_data)
    llm = create_llm_service()
    selected_model = llm.route_model(task_type=ReportLabAgent.TASK_TYPE, model=model)
    timestamp = utc_timestamp()
    directory = create_run_directory(runs_dir, timestamp)
    try:
        output = await ReportLabAgent(llm).run(input_data, prompt=prompt, model=model, temperature=temperature)
        output = InterviewReport.model_validate(output.model_dump(mode="json"))
    except Exception as error:
        write_artifacts(directory, input_payload=payload, prompt=prompt, output=None, ai="ai_report", model=selected_model, task_type=ReportLabAgent.TASK_TYPE, temperature=temperature, timestamp=timestamp, success=False, error=f"{type(error).__name__}: {error}")
        raise
    write_artifacts(directory, input_payload=payload, prompt=prompt, output=output, ai="ai_report", model=selected_model, task_type=ReportLabAgent.TASK_TYPE, temperature=temperature, timestamp=timestamp, success=True)
    print_output(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the standalone Report Generator lab")
    parser.add_argument("input")
    parser.add_argument("--model")
    parser.add_argument("--temperature", type=float, default=ReportLabAgent.TEMPERATURE)
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR))
    args = parser.parse_args()
    asyncio.run(run(args.input, model=args.model, temperature=args.temperature, runs_dir=args.runs_dir))


if __name__ == "__main__":
    main()
