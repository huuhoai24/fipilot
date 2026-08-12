from __future__ import annotations

import argparse
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any


TTS_MODEL_SNAPSHOTS: dict[str, tuple[str, ...]] = {
    "pnnbao-ump/VieNeu-TTS-v3-Turbo": (
        "config.json",
        "onnx_int8/config.json",
        "onnx_int8/tokenizer.json",
        "onnx_int8/vieneu_prefill.onnx",
        "onnx_int8/vieneu_decode_step.onnx",
        "onnx_int8/vieneu_acoustic_cached.onnx",
        "onnx_int8/vieneu_backbone_shared.data",
        "onnx_int8/vieneu_v3_heads.npz",
    ),
    "OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX": (
        "codec_browser_onnx_meta.json",
        "moss_audio_tokenizer_decode_full.onnx",
        "moss_audio_tokenizer_decode_shared.data",
        "moss_audio_tokenizer_decode_step.onnx",
        "moss_audio_tokenizer_encode.onnx",
        "moss_audio_tokenizer_encode.data",
    ),
}
STT_REQUIRED_FILES = (
    "config.json",
    "model.bin",
    "tokenizer.json",
)


def _require_files(root: Path, files: tuple[str, ...], *, model_name: str) -> None:
    missing = [relative for relative in files if not (root / relative).is_file()]
    if missing:
        raise RuntimeError(
            f"Cached {model_name} snapshot is incomplete: {', '.join(missing)}"
        )


def cache_speech_models(
    *,
    stt_model: str,
    stt_output_dir: Path,
    stt_download: Callable[..., str] | None = None,
    snapshot_download: Callable[..., str] | None = None,
) -> dict[str, Any]:
    if stt_download is None:
        from faster_whisper.utils import download_model

        stt_download = download_model
    if snapshot_download is None:
        from huggingface_hub import snapshot_download as hub_snapshot_download

        snapshot_download = hub_snapshot_download

    token = os.getenv("HF_TOKEN") or None
    stt_output_dir.mkdir(parents=True, exist_ok=True)
    stt_path = stt_download(
        size_or_id=stt_model,
        output_dir=str(stt_output_dir),
        use_auth_token=token,
    )
    _require_files(Path(stt_path), STT_REQUIRED_FILES, model_name="STT")

    snapshots: dict[str, str] = {}
    for repo_id, files in TTS_MODEL_SNAPSHOTS.items():
        snapshot_path = snapshot_download(
            repo_id=repo_id,
            repo_type="model",
            allow_patterns=list(files),
            token=token,
        )
        _require_files(Path(snapshot_path), files, model_name=repo_id)
        snapshots[repo_id] = str(snapshot_path)

    return {
        "status": "ok",
        "stt_model": stt_model,
        "stt_path": str(stt_path),
        "tts_snapshots": sorted(snapshots),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cache the public CPU speech models inside a container image."
    )
    parser.add_argument("--stt-model", default="large-v3-turbo")
    parser.add_argument(
        "--stt-output-dir",
        type=Path,
        default=Path("/opt/fipilot/models/faster-whisper-large-v3-turbo"),
    )
    args = parser.parse_args()
    result = cache_speech_models(
        stt_model=args.stt_model,
        stt_output_dir=args.stt_output_dir,
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
