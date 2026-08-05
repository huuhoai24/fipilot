from __future__ import annotations

import asyncio
from typing import Any


async def warm_up_speech_runtime(
    pipeline_factory: Any,
    tts_service: Any,
) -> None:
    """Load shared speech models before the first candidate turn.

    TTS is first because the opening question is the first inference a speech
    session needs. STT and VAD then load while the candidate hears and reads it.
    """
    if hasattr(tts_service, "warm_up"):
        await tts_service.warm_up()

    stt_factory = getattr(pipeline_factory, "stt_factory", None)
    if stt_factory is not None and hasattr(stt_factory, "warm_up"):
        await asyncio.to_thread(stt_factory.warm_up)

    vad_factory = getattr(pipeline_factory, "vad_factory", None)
    vad_provider = getattr(vad_factory, "provider", None)
    if vad_provider is not None and hasattr(vad_provider, "get_model"):
        await asyncio.to_thread(vad_provider.get_model)
