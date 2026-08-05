from __future__ import annotations

import sys
import unittest
from unittest.mock import patch

from core.settings import Settings
from scripts.check_speech_runtime import (
    REQUIRED_MODULES,
    SpeechRuntimeValidationError,
    validate_application_import,
    validate_cpu_configuration,
    validate_lazy_model_loading,
    validate_required_packages,
)


class SpeechRuntimeCheckTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(
            APP_ENV="test",
            AUTH_ENABLED=False,
            GOOGLE_CLOUD_PROJECT="test-project",
            STT_MODEL="small",
            STT_DEVICE="cpu",
            STT_COMPUTE_TYPE="int8",
            STT_LANGUAGE="vi",
            TTS_DEVICE="cpu",
            SPEECH_SERVICE_URL="",
        )

    def test_required_package_check_does_not_import_models(self):
        before = set(sys.modules)
        with patch("scripts.check_speech_runtime.importlib.util.find_spec") as finder:
            finder.return_value = object()
            packages = validate_required_packages()

        self.assertEqual(packages, sorted(REQUIRED_MODULES))
        self.assertEqual(
            {"faster_whisper", "silero_vad", "vieneu"} & (set(sys.modules) - before),
            set(),
        )

    def test_cpu_configuration_accepts_single_container_settings(self):
        result = validate_cpu_configuration(self.settings)

        self.assertEqual(result["stt_model"], "small")
        self.assertEqual(result["stt_device"], "cpu")
        self.assertEqual(result["tts_device"], "cpu")

    def test_cpu_configuration_rejects_gpu(self):
        settings = Settings(
            APP_ENV="test",
            AUTH_ENABLED=False,
            GOOGLE_CLOUD_PROJECT="test-project",
            STT_MODEL="small",
            STT_DEVICE="cuda",
            STT_COMPUTE_TYPE="float16",
            STT_LANGUAGE="vi",
            TTS_DEVICE="cuda",
        )

        with self.assertRaisesRegex(SpeechRuntimeValidationError, "STT_DEVICE"):
            validate_cpu_configuration(settings)

    def test_model_factories_remain_lazy(self):
        models = validate_lazy_model_loading(self.settings)

        self.assertEqual(models, ["faster-whisper", "silero-vad", "vieneu"])

    def test_gateway_import_exposes_health_and_voice_routes(self):
        paths = validate_application_import(self.settings)

        self.assertEqual(
            paths,
            ["/api/v2/voice/interview/{session_id}", "/health"],
        )


if __name__ == "__main__":
    unittest.main()
