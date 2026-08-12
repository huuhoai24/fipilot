from __future__ import annotations

import unittest

from services.voice_session.warmup import warm_up_speech_runtime


class _Warmable:
    def __init__(self, name: str, order: list[str]) -> None:
        self.name = name
        self.order = order

    def warm_up(self) -> None:
        self.order.append(self.name)


class _Provider:
    def __init__(self, order: list[str]) -> None:
        self.order = order

    def get_model(self):
        self.order.append("vad")
        return object()


class _VADFactory:
    def __init__(self, order: list[str]) -> None:
        self.provider = _Provider(order)


class _Factory:
    def __init__(self, order: list[str]) -> None:
        self.stt_factory = _Warmable("stt", order)
        self.vad_factory = _VADFactory(order)


class _TTS:
    def __init__(self, order: list[str]) -> None:
        self.order = order

    async def warm_up(self) -> None:
        self.order.append("tts")


class SpeechWarmupTests(unittest.IsolatedAsyncioTestCase):
    async def test_warmup_prioritizes_first_question_audio_then_stt(self):
        order: list[str] = []

        await warm_up_speech_runtime(_Factory(order), _TTS(order))

        self.assertEqual(order, ["tts", "stt", "vad"])

    async def test_tts_only_prewarm_does_not_initialize_stt_or_vad(self):
        order: list[str] = []

        await warm_up_speech_runtime(
            _Factory(order),
            _TTS(order),
            prewarm_tts=True,
            prewarm_stt_vad=False,
        )

        self.assertEqual(order, ["tts"])


if __name__ == "__main__":
    unittest.main()
