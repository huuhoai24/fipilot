from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.settings import Settings, get_settings


REQUIRED_MODULES = {
    "faster-whisper": "faster_whisper",
    "silero-vad": "silero_vad",
    "numpy": "numpy",
    "soxr": "soxr",
    "torch": "torch",
    "torchaudio": "torchaudio",
    "vieneu": "vieneu",
}
HEAVY_MODEL_MODULES = ("faster_whisper", "silero_vad", "vieneu")


class SpeechRuntimeValidationError(RuntimeError):
    pass


def validate_required_packages() -> list[str]:
    missing = [
        distribution
        for distribution, module in REQUIRED_MODULES.items()
        if importlib.util.find_spec(module) is None
    ]
    if missing:
        raise SpeechRuntimeValidationError(
            "Missing speech runtime packages: " + ", ".join(sorted(missing))
        )
    return sorted(REQUIRED_MODULES)


def validate_cpu_configuration(settings: Settings) -> dict[str, str]:
    errors: list[str] = []
    if not settings.stt_model.strip():
        errors.append("STT_MODEL must not be empty")
    if settings.stt_device.lower() != "cpu":
        errors.append("STT_DEVICE must be cpu")
    if settings.stt_compute_type.lower() != "int8":
        errors.append("STT_COMPUTE_TYPE must be int8 for this CPU benchmark")
    if not settings.stt_language.strip():
        errors.append("STT_LANGUAGE must not be empty")
    if settings.tts_device.lower() != "cpu":
        errors.append("TTS_DEVICE must be cpu")
    if settings.speech_service_url:
        errors.append("SPEECH_SERVICE_URL must be empty for the single-container benchmark")
    if errors:
        raise SpeechRuntimeValidationError("; ".join(errors))
    return {
        "stt_model": settings.stt_model,
        "stt_device": settings.stt_device,
        "stt_compute_type": settings.stt_compute_type,
        "stt_language": settings.stt_language,
        "tts_device": settings.tts_device,
    }


def validate_lazy_model_loading(settings: Settings) -> list[str]:
    loaded_before = {name for name in HEAVY_MODEL_MODULES if name in sys.modules}

    from infrastructure.speech.stt.faster_whisper import FasterWhisperSTTFactory
    from infrastructure.speech.tts.vieneu import VieneuStreamingTTS
    from services.voice_session.audio_pipeline import SileroVADFactory

    stt_factory = FasterWhisperSTTFactory(
        model_name=settings.stt_model,
        device=settings.stt_device,
        compute_type=settings.stt_compute_type,
        language=settings.stt_language,
        partial_interval_ms=settings.stt_partial_interval_ms,
        vocabulary_profile=settings.stt_vocabulary_profile,
        custom_hotwords=settings.stt_hotwords,
        partial_max_audio_ms=settings.stt_partial_max_audio_ms,
        final_beam_size=settings.stt_final_beam_size,
    )
    vad_factory = SileroVADFactory(
        threshold=settings.vad_threshold,
        min_silence_ms=settings.vad_min_silence_ms,
        speech_pad_ms=settings.vad_speech_pad_ms,
    )
    tts = VieneuStreamingTTS(
        mode=settings.tts_mode,
        device=settings.tts_device,
        voice=settings.tts_voice,
        sample_rate=settings.tts_sample_rate,
        frame_duration_ms=settings.tts_frame_duration_ms,
    )
    try:
        tts_provider = getattr(tts._model_provider, "__self__", None)
        providers = {
            "faster-whisper": stt_factory.provider,
            "silero-vad": vad_factory.provider,
            "vieneu": tts_provider,
        }
        eager = [
            name
            for name, provider in providers.items()
            if provider is None or getattr(provider, "_model", object()) is not None
        ]
        loaded_after = {
            name for name in HEAVY_MODEL_MODULES if name in sys.modules
        }
        newly_imported = sorted(loaded_after - loaded_before)
        if eager or newly_imported:
            details = sorted(set(eager + newly_imported))
            raise SpeechRuntimeValidationError(
                "Speech models loaded eagerly: " + ", ".join(details)
            )
    finally:
        tts.close()
    return sorted(providers)


def validate_application_import(settings: Settings) -> list[str]:
    from core.startup import validate_runtime_settings
    from gateway.main import app

    validate_runtime_settings(settings)

    def collect_paths(routes) -> set[str]:
        paths: set[str] = set()
        for route in routes:
            path = getattr(route, "path", None)
            if path is not None:
                paths.add(path)
            nested_router = getattr(route, "original_router", None)
            if nested_router is not None:
                paths.update(collect_paths(nested_router.routes))
        return paths

    paths = collect_paths(app.routes)
    required_paths = {"/health", "/api/v2/voice/interview/{session_id}"}
    missing = sorted(required_paths - paths)
    if missing:
        raise SpeechRuntimeValidationError(
            "Application routes are missing: " + ", ".join(missing)
        )
    return sorted(required_paths)


def run_checks(settings: Settings | None = None) -> dict[str, Any]:
    active_settings = settings or get_settings()
    return {
        "status": "ok",
        "packages": validate_required_packages(),
        "configuration": validate_cpu_configuration(active_settings),
        "lazy_models": validate_lazy_model_loading(active_settings),
        "application_routes": validate_application_import(active_settings),
        "gpu_required": False,
        "models_downloaded": False,
    }


def main() -> int:
    try:
        result = run_checks()
    except Exception as error:
        print(json.dumps({"status": "error", "message": str(error)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
