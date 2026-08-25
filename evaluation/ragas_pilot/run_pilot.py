from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evaluation.ragas_pilot.runner import PilotRunner  # noqa: E402


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the FiPilot RAGAS-style pilot")
    parser.add_argument("--smoke-size", type=int, default=10)
    parser.add_argument("--target-size", type=int, default=30)
    parser.add_argument("--robustness-subset", type=int, default=2)
    return parser.parse_args()


async def _run(arguments: argparse.Namespace) -> int:
    runner = PilotRunner(
        output_root=REPO_ROOT / "evaluation" / "ragas_pilot",
        catalog_path=REPO_ROOT
        / "backend"
        / "services"
        / "interview_knowledge"
        / "catalog.json",
        smoke_size=arguments.smoke_size,
        target_size=arguments.target_size,
        robustness_subset=arguments.robustness_subset,
    )
    result = await runner.run()
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return 0


def main() -> int:
    return asyncio.run(_run(_arguments()))


if __name__ == "__main__":
    raise SystemExit(main())
