from __future__ import annotations

import asyncio
import os
import unittest
from types import SimpleNamespace
from unittest import mock

from core.settings import Settings
from infrastructure.speech.stt.azure import (
    AzureStreamingSTT,
    AzureStreamingSTTFactory,
)
from infrastructure.speech.tts.azure import (
    AzureStreamingTTS,
    AzureTTSError,
)


class _FakePushStream:
    def __init__(self, stream_format=None) -> None:
        self.stream_format = stream_format
        self.written: list[bytes] = []
        self.closed = False

    def write(self, audio_bytes: bytes) -> None:
        self.written.append(audio_bytes)

    def close(self) -> None:
        self.closed = True


class _Signal:
    def __init__(self) -> None:
        self.handler = None

    def connect(self, handler) -> None:
        self.handler = handler


class _FakeRecognizer:
    def __init__(self) -> None:
        self.recognizing = _Signal()
        self.recognized = _Signal()
        self.canceled = _Signal()
        self.session_stopped = _Signal()
        self.started = False
        self.stopped = False

    class _AsyncOp:
        def __init__(self, done) -> None:
            self._done = done

        def get(self, timeout: float | None = None) -> None:
            self._done()

    def start_continuous_recognition_async(self) -> "_FakeRecognizer._AsyncOp":
        self.started = True
        return self._AsyncOp(lambda: None)

    def stop_continuous_recognition_async(self) -> "_FakeRecognizer._AsyncOp":
        self.stopped = True
        self.session_stopped.handler(None)
        return self._AsyncOp(lambda: None)


def _build_fake_sdk():
    captured: dict[str, object] = {}

    class FakeSpeechConfig:
        def __init__(self, *, subscription: str, region: str) -> None:
            captured["subscription"] = subscription
            captured["region"] = region
            self.speech_recognition_language = None

    def push_audio_input_stream(stream_format=None) -> _FakePushStream:
        if "stream" not in captured:
            captured["stream"] = _FakePushStream(stream_format)
        return captured["stream"]

    recognizer = _FakeRecognizer()
    fake_sdk = SimpleNamespace(
        SpeechConfig=FakeSpeechConfig,
        SpeechRecognizer=lambda speech_config, audio_config: recognizer,
        ResultReason=SimpleNamespace(RecognizedSpeech="RecognizedSpeech"),
        audio=SimpleNamespace(
            AudioStreamFormat=lambda **kwargs: kwargs,
            PushAudioInputStream=push_audio_input_stream,
            AudioConfig=lambda stream=None: SimpleNamespace(stream=stream),
        ),
    )
    captured["recognizer"] = recognizer
    return fake_sdk, captured


def _event(text: str) -> SimpleNamespace:
    return SimpleNamespace(
        result=SimpleNamespace(
            text=text,
            reason="RecognizedSpeech",
        )
    )


async def _drain(aiter):
    return [chunk async for chunk in aiter]


class AzureStreamingSTTTests(unittest.TestCase):
    def _make_stt(self):
        fake_sdk, captured = _build_fake_sdk()
        stt = AzureStreamingSTT(
            speech_key="key",
            speech_region="southeastasia",
            language="vi",
            partial_interval_ms=0,
            sdk_provider=lambda: fake_sdk,
        )
        asyncio.run(stt.start_session())
        recognizer = captured["recognizer"]
        stream = captured["stream"]
        return stt, recognizer, stream

    def test_start_session_configures_azure_and_starts_recognition(self):
        stt, recognizer, stream = self._make_stt()

        self.assertTrue(recognizer.started)
        self.assertEqual(stream.stream_format["samples_per_second"], 16000)
        self.assertEqual(stream.stream_format["bits_per_sample"], 16)
        self.assertEqual(stream.stream_format["channels"], 1)
        # Language mapping follows the minimal deployment's vi-VN locale.
        self.assertEqual(stt._language_tag, "vi-VN")

    def test_append_audio_writes_raw_pcm_to_the_push_stream(self):
        stt, _recognizer, stream = self._make_stt()

        asyncio.run(stt.append_audio(b"\x01\x00" * 512))

        self.assertEqual(stream.written, [b"\x01\x00" * 512])
        self.assertFalse(stream.closed)

    def test_partial_flow_publishes_deferred_partials(self):
        stt, recognizer, _stream = self._make_stt()

        recognizer.recognizing.handler(_event("Xin"))
        self.assertTrue(stt.partial_due())
        partial = asyncio.run(stt.transcribe_partial())

        assert partial is not None
        self.assertEqual(partial.type.value, "partial")
        self.assertEqual(partial.text, "Xin")
        self.assertEqual(partial.language, "vi-VN")

        recognizer.recognized.handler(_event("Xin chao ban"))
        partial_two = asyncio.run(stt.transcribe_partial())

        assert partial_two is not None
        self.assertEqual(partial_two.text, "Xin chao ban")

    def test_finish_session_joins_recognized_segments_into_one_final(self):
        stt, recognizer, stream = self._make_stt()

        recognizer.recognized.handler(_event("Toi la dev"))
        recognizer.recognized.handler(_event("lam viec voi python"))
        final = asyncio.run(stt.finish_session())

        self.assertTrue(recognizer.stopped)
        self.assertTrue(stream.closed)
        assert final is not None
        self.assertEqual(final.type.value, "final")
        self.assertEqual(final.text, "Toi la dev lam viec voi python")
        self.assertLessEqual(final.confidence, 1.0)

    def test_finish_session_without_speech_returns_none(self):
        stt, _recognizer, _stream = self._make_stt()

        self.assertIsNone(asyncio.run(stt.finish_session()))

    def test_factory_maps_requested_language_per_session(self):
        factory = AzureStreamingSTTFactory(
            speech_key="key",
            speech_region="region",
            language="vi",
        )

        self.assertEqual(factory.create_for_language("en")._language_tag, "en-US")
        self.assertEqual(factory.create_for_language(None)._language_tag, "vi-VN")


class AzureStreamingTTSTests(unittest.TestCase):
    def _make_tts(self, **overrides) -> AzureStreamingTTS:
        return AzureStreamingTTS(
            speech_key="key",
            speech_region="southeastasia",
            **overrides,
        )

    def test_stream_yields_fixed_pcm_frames_at_the_contract_rate(self):
        tts = self._make_tts(sample_rate=24000, frame_duration_ms=100)
        pcm = b"\x00\x01" * 24_000  # one second of mono 16-bit audio
        with mock.patch.object(tts, "_synthesize_pcm", return_value=pcm):
            chunks = asyncio.run(_drain(tts.synthesize_stream("Xin chao")))

        # 24000 samples/s * 2 bytes * 100 ms = 4800 bytes per frame.
        self.assertEqual([len(chunk.bytes) for chunk in chunks], [4800] * 10)
        self.assertTrue(all(chunk.sample_rate == 24000 for chunk in chunks))
        self.assertTrue(all(chunk.format == "pcm" for chunk in chunks))

    def test_stream_keeps_the_trailing_partial_frame(self):
        tts = self._make_tts(sample_rate=24000, frame_duration_ms=100)
        pcm = b"\x00\x01" * 12_001  # half a second plus one sample
        with mock.patch.object(tts, "_synthesize_pcm", return_value=pcm):
            chunks = asyncio.run(_drain(tts.synthesize_stream("hello")))

        self.assertEqual(chunks[-1].bytes, pcm[-2:])
        self.assertEqual(len(chunks), 6)

    def test_blank_text_skips_synthesis_entirely(self):
        tts = self._make_tts()
        with mock.patch.object(tts, "_synthesize_pcm") as synthesize:
            chunks = asyncio.run(_drain(tts.synthesize_stream("   ")))

        synthesize.assert_not_called()
        self.assertEqual(chunks, [])

    def test_synthesis_failure_raises_domain_error(self):
        tts = self._make_tts()
        with mock.patch.object(
            tts,
            "_synthesize_pcm",
            side_effect=AzureTTSError("Azure Speech REST failed (401): bad key"),
        ):
            with self.assertRaises(AzureTTSError):
                asyncio.run(_drain(tts.synthesize_stream("text")))

    def test_requires_key_and_region(self):
        with self.assertRaises(AzureTTSError):
            AzureStreamingTTS(speech_key="", speech_region="")


class AzureSettingsAndWiringTests(unittest.TestCase):
    def test_env_credentials_populate_speech_settings(self):
        with mock.patch.dict(
            os.environ,
            {
                "AZURE_SPEECH_KEY": "test-key",
                "AZURE_SPEECH_REGION": "southeastasia",
                "AZURE_SPEECH_VOICE": "vi-VN-HoaiMyNeural",
            },
            clear=False,
        ):
            settings = Settings()

        self.assertEqual(settings.azure_speech_key, "test-key")
        self.assertEqual(settings.azure_speech_region, "southeastasia")
        self.assertEqual(settings.speech.tts_azure_voice, "vi-VN-HoaiMyNeural")

    def test_defaults_keep_local_stack_when_azure_is_absent(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AZURE_SPEECH_KEY", None)
            os.environ.pop("AZURE_SPEECH_REGION", None)
            settings = Settings()

        self.assertIsNone(settings.azure_speech_key)
        self.assertIsNone(settings.azure_speech_region)

    def _settings_with(self, **overrides):
        settings = SimpleNamespace(
            azure_speech_key=None,
            azure_speech_region=None,
            speech_service_url=None,
            speech_service_token=None,
            speech=SimpleNamespace(tts_azure_voice=None),
            tts_mode="v3turbo",
            tts_device="auto",
            tts_voice=None,
            tts_sample_rate=24000,
            tts_frame_duration_ms=100,
            stt_model="large-v3",
            stt_device="cpu",
            stt_compute_type="int8",
            stt_language="vi",
            stt_vocabulary_profile="auto",
            stt_hotwords=[],
            stt_partial_interval_ms=2500,
            stt_partial_max_audio_ms=20000,
            stt_final_beam_size=5,
            stt_audio_queue_size=800,
            vad_threshold=0.5,
            vad_min_silence_ms=900,
            vad_speech_pad_ms=120,
        )
        for name, value in overrides.items():
            setattr(settings, name, value)
        return settings

    def test_gateway_routes_both_seams_to_azure_when_configured(self):
        from core.dependencies import (
            _build_audio_pipeline_factory,
            _build_streaming_tts,
        )

        settings = self._settings_with(
            azure_speech_key="k",
            azure_speech_region="r",
            speech_service_url="http://localhost:9000",
        )

        pipeline_factory = _build_audio_pipeline_factory(settings)
        tts = _build_streaming_tts(settings)

        self.assertIsInstance(pipeline_factory.stt_factory, AzureStreamingSTTFactory)
        self.assertIsInstance(tts, AzureStreamingTTS)

    def test_gateway_keeps_remote_service_without_azure(self):
        from core.dependencies import _build_audio_pipeline_factory
        from infrastructure.speech.remote import RemoteAudioPipelineFactory

        settings = self._settings_with(speech_service_url="http://localhost:9000")

        pipeline_factory = _build_audio_pipeline_factory(settings)

        self.assertIsInstance(pipeline_factory, RemoteAudioPipelineFactory)

    def test_gateway_keeps_local_stack_without_any_provider(self):
        from core.dependencies import _build_audio_pipeline_factory
        from infrastructure.speech.stt.faster_whisper import FasterWhisperSTTFactory
        from services.voice_session.audio_pipeline import AudioPipelineFactory

        settings = self._settings_with()

        pipeline_factory = _build_audio_pipeline_factory(settings)

        self.assertIsInstance(pipeline_factory, AudioPipelineFactory)
        self.assertIsInstance(pipeline_factory.stt_factory, FasterWhisperSTTFactory)


if __name__ == "__main__":
    unittest.main()
