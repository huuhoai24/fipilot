from __future__ import annotations

import argparse
import difflib
import json
import sys
import time
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from core.settings import get_settings
from infrastructure.speech.stt.faster_whisper import _FasterWhisperModelProvider
from infrastructure.speech.stt.vocabulary import vocabulary_hotwords


@dataclass(frozen=True)
class CodeSwitchCase:
    filename: str
    reference: str
    technical_terms: tuple[str, ...]


CASES = (
    CodeSwitchCase(
        "01-fastapi.wav",
        "Tôi build backend bằng FastAPI.",
        ("build", "backend", "FastAPI"),
    ),
    CodeSwitchCase(
        "02-langgraph.wav",
        "Tôi sử dụng LangGraph để orchestrate multi-agent workflow.",
        ("LangGraph", "orchestrate", "multi-agent workflow"),
    ),
    CodeSwitchCase(
        "03-cloud-run.wav",
        "Model YOLO được deploy bằng Docker trên Cloud Run.",
        ("Model", "YOLO", "deploy", "Docker", "Cloud Run"),
    ),
    CodeSwitchCase(
        "04-concurrency.wav",
        "Tôi dùng multiprocessing và multithreading để xử lý video.",
        ("multiprocessing", "multithreading", "video"),
    ),
)


def _score(reference: str, transcript: str) -> float:
    return round(
        difflib.SequenceMatcher(
            None,
            reference.casefold(),
            transcript.casefold(),
        ).ratio(),
        3,
    )


def _retained_terms(transcript: str, terms: tuple[str, ...]) -> list[str]:
    normalized = transcript.casefold()
    return [term for term in terms if term.casefold() in normalized]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare fixed-Vietnamese and per-segment multilingual STT.",
    )
    parser.add_argument(
        "audio_dir",
        type=Path,
        help="Directory containing the four sanitized WAV fixtures.",
    )
    args = parser.parse_args()
    missing = [
        case.filename
        for case in CASES
        if not (args.audio_dir / case.filename).is_file()
    ]
    if missing:
        parser.error(f"Missing sanitized audio fixtures: {', '.join(missing)}")

    settings = get_settings()
    provider = _FasterWhisperModelProvider(
        model_name=settings.stt_model,
        device=settings.stt_device,
        compute_type=settings.stt_compute_type,
    )
    model = provider._get_model()
    hotwords = vocabulary_hotwords(
        settings.stt_vocabulary_profile,
        settings.stt_hotwords,
    ) or None
    results = []
    for case in CASES:
        row: dict[str, object] = {
            "reference": case.reference,
            "audio": case.filename,
        }
        for label, multilingual in (("current", False), ("proposed", True)):
            started = time.perf_counter()
            segments, info = model.transcribe(
                str(args.audio_dir / case.filename),
                language="vi",
                multilingual=multilingual,
                beam_size=settings.stt_final_beam_size,
                vad_filter=False,
                condition_on_previous_text=False,
                word_timestamps=False,
                hotwords=hotwords,
            )
            transcript = " ".join(
                segment.text.strip() for segment in segments
            ).strip()
            row[label] = {
                "transcript": transcript,
                "similarity": _score(case.reference, transcript),
                "technical_terms_retained": _retained_terms(
                    transcript,
                    case.technical_terms,
                ),
                "reported_language": getattr(info, "language", None),
                "latency_ms": round((time.perf_counter() - started) * 1000, 1),
            }
        results.append(row)

    print(
        json.dumps(
            {
                "faster_whisper": version("faster-whisper"),
                "model": settings.stt_model,
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
