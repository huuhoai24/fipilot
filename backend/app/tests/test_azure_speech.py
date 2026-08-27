from __future__ import annotations

import asyncio
import types

import pytest

from infrastructure.speech.stt.azure import (
    AzureSTTFactory,
    _resolve_stt_locale,
)
from infrastructure.speech.tts.azure import AzureStreamingTTS


# --------------------------------------------------------------------------- #
# Fake Azure Speech SDK for hermetic STT tests                                 #
# --------------------------------------------------------------------------- #
class _FakeEvent:
    def __init__(self) -> None:
        self.handlers: list = []

    def connect(self, handler) -> None:  # pragma: no cover - trivial
        self.handlers.append(handler)

    def fire(self, evt) -> None:  # pragma: no cover - trivial
        for handler in self.handlers:
            handler(evt)


class _FakeResult:
    def __init__(self, text: str, json: str | None = None) -> None:
        self.text = text
        self.json = json or "{}"


class _FakeSpeechEvt:
    def __init__(self, text: str, json: str | None = None) -> None:
        self.result = _FakeResult(text, json)


class _FakePushAudioInputStream:
    def __init__(self, stream_format) -> None:
        self.stream_format = stream_format
        self.written = bytearray()

    def write(self, data: bytes) -> None:
        self.written.extend(data)

    def close(self) -> None:  # pragma: no cover - trivial
        self.closed = True


class _FakeRecognizer:
    def __init__(self, *args, **kwargs) -> None:
        self.speech_config = kwargs.get("speech_config")
        self.audio_config = kwargs.get("audio_config")
        self.recognizing = _FakeEvent()
        self.recognized = _FakeEvent()

    def start_continuous_recognition(self) -> None:  # pragma: no cover - trivial
        self.started = True

    def stop_continuous_recognition(self) -> None:  # pragma: no cover - trivial
        self.stopped = True

    def start_continuous_recognition_async(self):  # pragma: no cover - trivial
        return _FakeFuture(self.start_continuous_recognition)

    def stop_continuous_recognition_async(self):  # pragma: no cover - trivial
        return _FakeFuture(self.stop_continuous_recognition)


class _FakeFuture:
    def __init__(self, callback) -> None:
        self.callback = callback

    def get(self) -> None:
        self.callback()


class _FakeSynthesizer:
    def __init__(self, *args, **kwargs) -> None:
        self.speech_config = kwargs.get("speech_config")

    def speak_text_async(self, text: str):  # pragma: no cover - trivial
        class _Future:
            def get(self):
                return _FakeSynthResult(text)

        return _Future()


class _FakeSynthResult:
    def __init__(self, text: str) -> None:
        self.reason = _FakeResultReason.SynthesizingAudioCompleted
        self.audio_data = b"MP3BYTES:" + text.encode("utf-8")


class _FakeResultReason:
    SynthesizingAudioCompleted = "completed"


def _make_fake_speechsdk() -> tuple[types.ModuleType, dict]:
    recorder: dict = {"recognizers": [], "synthesizers": []}

    def _make_recognizer(*args, **kwargs):
        recognizer = _FakeRecognizer(*args, **kwargs)
        recorder["recognizers"].append(recognizer)
        return recognizer

    def _make_synthesizer(*args, **kwargs):
        synthesizer = _FakeSynthesizer(*args, **kwargs)
        recorder["synthesizers"].append(synthesizer)
        return synthesizer

    audio_mod = types.SimpleNamespace(
        AudioStreamFormat=lambda *a, **k: object(),
        PushAudioInputStream=_FakePushAudioInputStream,
        AudioConfig=lambda *a, **k: object(),
    )
    sdk = types.SimpleNamespace(
        SpeechConfig=_FakeSpeechConfig,
        SpeechRecognizer=_make_recognizer,
        SpeechSynthesizer=_make_synthesizer,
        ResultReason=_FakeResultReason,
        audio=audio_mod,
    )
    recorder["sdk"] = sdk
    return sdk, recorder


class _FakeSpeechConfig:
    def __init__(self, subscription=None, region=None, endpoint=None) -> None:
        self.subscription = subscription
        self.region = region
        self.endpoint = endpoint
        self.speech_recognition_language = None
        self.speech_synthesis_voice_name = None


# --------------------------------------------------------------------------- #
# STT tests                                                                    #
# --------------------------------------------------------------------------- #
def test_resolve_stt_locale():
    assert _resolve_stt_locale("vi", "vi-VN") == "vi-VN"
    assert _resolve_stt_locale("en", "vi-VN") == "en-US"
    assert _resolve_stt_locale("fr", "vi-VN") == "vi-VN"


def test_azure_stt_factory_language_mapping(monkeypatch):
    import infrastructure.speech.stt.azure as azure_stt

    sdk, recorder = _make_fake_speechsdk()
    monkeypatch.setattr(azure_stt, "speechsdk", sdk)

    factory = AzureSTTFactory(
        speech_key="k", speech_region="r", default_locale="vi-VN"
    )
    for session_lang, expected in (("vi", "vi-VN"), ("en", "en-US")):
        stt = factory.create_for_language(session_lang)
        asyncio.run(stt.start_session())
        config = recorder["recognizers"][-1].speech_config
        assert config.speech_recognition_language == expected


def test_azure_stt_partial_and_final(monkeypatch):
    import infrastructure.speech.stt.azure as azure_stt

    sdk, recorder = _make_fake_speechsdk()
    monkeypatch.setattr(azure_stt, "speechsdk", sdk)

    stt = AzureSTTFactory(speech_key="k", speech_region="r").create_for_language("vi")
    asyncio.run(stt.start_session())
    recognizer = recorder["recognizers"][-1]

    # A recognizing callback should surface as a PARTIAL event.
    recognizer.recognizing.fire(
        _FakeSpeechEvt("xin chao", '{"Confidence": 0.9}')
    )
    partial = asyncio.run(stt.process_audio_chunk(b"\x00\x00" * 100))
    assert partial is not None
    assert partial.type.value == "partial"
    assert partial.text == "xin chao"
    assert partial.language == "vi-VN"
    assert partial.confidence == 0.9

    # Azure can finalize before VAD has endpointed. It must be held until
    # finish so the pipeline submits one final answer, not a duplicate.
    recognizer.recognized.fire(_FakeSpeechEvt("xin chao a"))
    assert asyncio.run(stt.process_audio_chunk(b"\x00\x00" * 100)) is None
    final = asyncio.run(stt.finish_session())
    assert final is not None
    assert final.type.value == "final"
    assert final.text == "xin chao a"

    # Draining again returns None (queue empty).
    assert asyncio.run(stt.process_audio_chunk(b"")) is None


def test_azure_stt_empty_result_ignored(monkeypatch):
    import infrastructure.speech.stt.azure as azure_stt

    sdk, recorder = _make_fake_speechsdk()
    monkeypatch.setattr(azure_stt, "speechsdk", sdk)

    stt = AzureSTTFactory(speech_key="k", speech_region="r").create_for_language("vi")
    asyncio.run(stt.start_session())
    recognizer = recorder["recognizers"][-1]
    recognizer.recognizing.fire(_FakeSpeechEvt(""))
    assert asyncio.run(stt.finish_session()) is None


def test_azure_stt_requires_credentials():
    from infrastructure.speech.stt.azure import AzureSTTError

    with pytest.raises(AzureSTTError):
        AzureSTTFactory(speech_key="", speech_region="").create()


# --------------------------------------------------------------------------- #
# TTS tests                                                                    #
# --------------------------------------------------------------------------- #
def test_azure_tts_stream_chunks_and_format(monkeypatch):
    import infrastructure.speech.tts.azure as azure_tts

    sdk, recorder = _make_fake_speechsdk()
    monkeypatch.setattr(azure_tts, "speechsdk", sdk)

    # Mock ffmpeg to emit a known block of raw PCM16 bytes.
    pcm_bytes = bytes(range(256)) * 50  # 12800 bytes
    fake_run = lambda *a, **k: types.SimpleNamespace(
        returncode=0, stdout=pcm_bytes, stderr=b""
    )
    monkeypatch.setattr(azure_tts.subprocess, "run", fake_run)

    tts = AzureStreamingTTS(speech_key="k", speech_region="r", voice="vi-VN-HoaiMyNeural")
    chunks = asyncio.run(_collect_list(tts.synthesize_stream("x")))

    assert chunks, "expected at least one chunk"
    sample_rates = {c.sample_rate for c in chunks}
    formats = {c.format for c in chunks}
    assert sample_rates == {24000}
    assert formats == {"pcm"}
    total = sum(len(c.bytes) for c in chunks)
    assert total == len(pcm_bytes)
    # First chunk length should equal the configured frame size (<= pcm length).
    assert len(chunks[0].bytes) == tts._frame_bytes


def test_azure_tts_warmup_does_not_raise(monkeypatch):
    import infrastructure.speech.tts.azure as azure_tts

    sdk, recorder = _make_fake_speechsdk()
    monkeypatch.setattr(azure_tts, "speechsdk", sdk)
    monkeypatch.setattr(
        azure_tts.subprocess,
        "run",
        lambda *a, **k: types.SimpleNamespace(
            returncode=0, stdout=b"\x00\x01" * 100, stderr=b""
        ),
    )

    tts = AzureStreamingTTS(speech_key="k", speech_region="r")
    asyncio.run(tts.warm_up())  # must not raise


def test_azure_tts_requires_credentials():
    from infrastructure.speech.tts.azure import AzureTTSError

    with pytest.raises(AzureTTSError):
        AzureStreamingTTS(speech_key="", speech_region="")


async def _collect_list(iterator):
    return [item async for item in iterator]
