from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from ai_lab._runtime import (
    create_llm_service,
    create_run_directory,
    print_output,
    read_json,
    utc_timestamp,
    validate_temperature,
    write_artifacts,
)
from ai_lab.ai_cv.agent import CVLabAgent
from ai_lab.ai_cv.prompt import build_prompt
from ai_lab.ai_cv.schemas import CVInput, CandidateProfile


DEFAULT_RUNS_DIR = Path(__file__).with_name("runs")


def parse_input(path: str | Path) -> CVInput:
    return CVInput.model_validate(read_json(path))


async def run(
    input_path: str | Path,
    *,
    model: str | None = None,
    temperature: float = CVLabAgent.TEMPERATURE,
    runs_dir: str | Path = DEFAULT_RUNS_DIR,
) -> CandidateProfile:
    temperature = validate_temperature(temperature)
    input_data = parse_input(input_path)
    input_payload = input_data.model_dump(mode="json")
    prompt = build_prompt(input_data.resume_text)
    llm = create_llm_service(resume_route=True)
    selected_model = llm.route_model(task_type=CVLabAgent.TASK_TYPE, model=model)
    timestamp = utc_timestamp()
    run_directory = create_run_directory(runs_dir, timestamp)
    output = None
    try:
        output = await CVLabAgent(llm).run(
            input_data,
            prompt=prompt,
            model=model,
            temperature=temperature,
        )
        output = CandidateProfile.model_validate(output.model_dump(mode="json"))
    except Exception as error:
        write_artifacts(
            run_directory,
            input_payload=input_payload,
            prompt=prompt,
            output=None,
            ai="ai_cv",
            model=selected_model,
            task_type=CVLabAgent.TASK_TYPE,
            temperature=temperature,
            timestamp=timestamp,
            success=False,
            error=f"{type(error).__name__}: {error}",
        )
        raise
    write_artifacts(
        run_directory,
        input_payload=input_payload,
        prompt=prompt,
        output=output,
        ai="ai_cv",
        model=selected_model,
        task_type=CVLabAgent.TASK_TYPE,
        temperature=temperature,
        timestamp=timestamp,
        success=True,
    )
    print_output(output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the standalone Resume AI lab")
    parser.add_argument("input", help="Path to an input JSON file")
    parser.add_argument("--model", help="Override the production model route")
    parser.add_argument("--temperature", type=float, default=CVLabAgent.TEMPERATURE)
    parser.add_argument("--runs-dir", default=str(DEFAULT_RUNS_DIR))
    args = parser.parse_args()
    asyncio.run(
        run(
            args.input,
            model=args.model,
            temperature=args.temperature,
            runs_dir=args.runs_dir,
        )
    )


if __name__ == "__main__":
    main()
