from __future__ import annotations

from functools import lru_cache

from core.settings import get_settings
from infrastructure.speech.stt.faster_whisper import FasterWhisperSTTFactory
from infrastructure.speech.tts.vieneu import VieneuStreamingTTS
from services.voice_session.audio_pipeline import AudioPipelineFactory, SileroVADFactory


@lru_cache
def get_speech_runtime() -> tuple[AudioPipelineFactory, VieneuStreamingTTS]:
    settings = get_settings()
    pipeline_factory = AudioPipelineFactory(
        stt_factory=FasterWhisperSTTFactory(
            model_name=settings.stt_model,
            device=settings.stt_device,
            compute_type=settings.stt_compute_type,
            language=settings.stt_language,
            partial_interval_ms=settings.stt_partial_interval_ms,
            vocabulary_profile=settings.stt_vocabulary_profile,
            custom_hotwords=settings.stt_hotwords,
        ),
        vad_factory=SileroVADFactory(
            threshold=settings.vad_threshold,
            min_silence_ms=settings.vad_min_silence_ms,
            speech_pad_ms=settings.vad_speech_pad_ms,
        ),
        queue_size=settings.stt_audio_queue_size,
    )
    tts = VieneuStreamingTTS(
        mode=settings.tts_mode,
        device=settings.tts_device,
        voice=settings.tts_voice,
        sample_rate=settings.tts_sample_rate,
        frame_duration_ms=settings.tts_frame_duration_ms,
    )
    return pipeline_factory, tts
