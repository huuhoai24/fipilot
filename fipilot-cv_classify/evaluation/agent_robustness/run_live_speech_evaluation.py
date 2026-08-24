"""Cost-bounded live Azure Speech integration checks."""

from __future__ import annotations

import json
import os
import sys
import time
import wave
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BACKEND_ROOT = ROOT.parent.parent / "backend"
sys.path.insert(0, str(BACKEND_ROOT))
os.chdir(BACKEND_ROOT)

from dotenv import load_dotenv

load_dotenv()

from fipilot.stt import recognize_vietnamese
from fipilot.tts import synthesize_speech


def main() -> None:
    results = []
    started = time.perf_counter()
    audio = b""
    try:
        audio = synthesize_speech("Xin chào, đây là bài kiểm tra phỏng vấn kỹ thuật.")
        with wave.open(BytesIO(audio), "rb") as wav:
            evidence = {
                "bytes": len(audio),
                "channels": wav.getnchannels(),
                "sample_rate": wav.getframerate(),
                "duration_seconds": round(wav.getnframes() / wav.getframerate(), 2),
            }
        results.append({
            "test_id": "SPEECH-LIVE-001",
            "agent": "synthesize_speech",
            "scenario": "Vietnamese text to WAV",
            "expected": "Non-empty decodable WAV within proxy timeout",
            "actual": {**evidence, "elapsed_seconds": round(time.perf_counter() - started, 2)},
            "status": "PASS" if evidence["bytes"] > 44 and evidence["channels"] == 1 else "FAIL",
            "severity": "",
        })
    except Exception as error:
        results.append({
            "test_id": "SPEECH-LIVE-001",
            "agent": "synthesize_speech",
            "scenario": "Vietnamese text to WAV",
            "expected": "Non-empty decodable WAV within proxy timeout",
            "actual": f"{type(error).__name__}: {error}",
            "status": "BLOCKED",
            "severity": "MEDIUM",
        })

    started = time.perf_counter()
    if not audio:
        results.append({
            "test_id": "SPEECH-LIVE-002",
            "agent": "recognize_vietnamese",
            "scenario": "Recognize generated Vietnamese speech",
            "expected": "Non-empty transcript",
            "actual": "TTS prerequisite blocked",
            "status": "BLOCKED",
            "severity": "MEDIUM",
        })
    else:
        try:
            transcript = recognize_vietnamese(audio)
            results.append({
                "test_id": "SPEECH-LIVE-002",
                "agent": "recognize_vietnamese",
                "scenario": "Recognize generated Vietnamese speech",
                "expected": "Non-empty transcript with Vietnamese greeting content",
                "actual": {"transcript": transcript, "elapsed_seconds": round(time.perf_counter() - started, 2)},
                "status": "PASS" if transcript and any(token in transcript.casefold() for token in ("xin chào", "kiểm tra", "phỏng vấn")) else "PARTIAL",
                "severity": "MEDIUM" if not transcript else "",
            })
        except Exception as error:
            results.append({
                "test_id": "SPEECH-LIVE-002",
                "agent": "recognize_vietnamese",
                "scenario": "Recognize generated Vietnamese speech",
                "expected": "Non-empty transcript with Vietnamese greeting content",
                "actual": f"{type(error).__name__}: {error}",
                "status": "BLOCKED",
                "severity": "MEDIUM",
            })

    statuses = ("PASS", "FAIL", "PARTIAL", "BLOCKED", "NOT TESTED", "NOT EVALUATED")
    payload = {
        "summary": {status: sum(item["status"] == status for item in results) for status in statuses},
        "results": results,
    }
    output = ROOT / "live_speech_results.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"results": len(results), "summary": payload["summary"], "evidence": str(output)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
