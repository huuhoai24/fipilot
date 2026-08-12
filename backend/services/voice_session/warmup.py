from __future__ import annotations

import asyncio
from typing import Any


async def warm_up_speech_runtime(
    pipeline_factory: Any,
    tts_service: Any,
    *,
    prewarm_tts: bool = True,
    prewarm_stt_vad: bool = True,
) -> Any | None:
    """Optionally load process-local speech models before a candidate turn.

    When both groups are selected, TTS remains first because the opening
    question is the first inference a speech session needs.
    """
    tts_metrics = None
    if prewarm_tts and hasattr(tts_service, "warm_up"):
        tts_metrics = await tts_service.warm_up()

    if prewarm_stt_vad:
        stt_factory = getattr(pipeline_factory, "stt_factory", None)
        if stt_factory is not None and hasattr(stt_factory, "warm_up"):
            await asyncio.to_thread(stt_factory.warm_up)

        vad_factory = getattr(pipeline_factory, "vad_factory", None)
        vad_provider = getattr(vad_factory, "provider", None)
        if vad_provider is not None and hasattr(vad_provider, "get_model"):
            await asyncio.to_thread(vad_provider.get_model)
    return tts_metrics
