from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from core.settings import get_settings
from infrastructure.speech.stt.faster_whisper import FasterWhisperSTTFactory
from infrastructure.speech.tts.vieneu import VieneuStreamingTTS
from services.voice_session.audio_pipeline import AudioPipelineFactory, SileroVADFactory


@lru_cache
def get_speech_runtime() -> tuple[AudioPipelineFactory, Any]:
    settings = get_settings()
    stt_provider = os.getenv("STT_PROVIDER", settings.stt_provider)
    tts_provider = os.getenv("TTS_PROVIDER", settings.tts_provider)

    if stt_provider == "azure":
        from infrastructure.speech.stt.azure import AzureSTTFactory

        stt_factory: Any = AzureSTTFactory(
            speech_key=settings.azure_speech_key,
            speech_region=settings.azure_speech_region,
            speech_endpoint=settings.azure_speech_endpoint,
            default_locale=settings.azure_stt_language,
        )
    else:
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

    pipeline_factory = AudioPipelineFactory(
        stt_factory=stt_factory,
        vad_factory=SileroVADFactory(
            threshold=settings.vad_threshold,
            min_silence_ms=settings.vad_min_silence_ms,
            speech_pad_ms=settings.vad_speech_pad_ms,
        ),
        queue_size=settings.stt_audio_queue_size,
    )

    if tts_provider == "azure":
        from infrastructure.speech.tts.azure import AzureStreamingTTS

        tts: Any = AzureStreamingTTS(
            speech_key=settings.azure_speech_key,
            speech_region=settings.azure_speech_region,
            speech_endpoint=settings.azure_speech_endpoint,
            voice=settings.azure_speech_voice,
            sample_rate=settings.tts_sample_rate,
            frame_duration_ms=settings.tts_frame_duration_ms,
        )
    else:
        tts = VieneuStreamingTTS(
            mode=settings.tts_mode,
            device=settings.tts_device,
            voice=settings.tts_voice,
            sample_rate=settings.tts_sample_rate,
            frame_duration_ms=settings.tts_frame_duration_ms,
        )
    return pipeline_factory, tts
