from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def write_jsonl(path: Path, samples: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for sample in samples:
            stream.write(json.dumps(sample, ensure_ascii=False, separators=(",", ":")))
            stream.write("\n")


def append_jsonl(path: Path, sample: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(sample, ensure_ascii=False, separators=(",", ":")))
        stream.write("\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]
