from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from scripts.cache_speech_models import (
    STT_REQUIRED_FILES,
    TTS_MODEL_SNAPSHOTS,
    cache_speech_models,
)


class SpeechModelCacheTests(unittest.TestCase):
    def test_cache_downloads_stt_and_required_tts_snapshots(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            def download_stt(**kwargs):
                destination = Path(kwargs["output_dir"])
                destination.mkdir(parents=True, exist_ok=True)
                for relative in STT_REQUIRED_FILES:
                    (destination / relative).write_bytes(b"model")
                return str(destination)

            def download_snapshot(**kwargs):
                destination = root / kwargs["repo_id"].replace("/", "--")
                for relative in kwargs["allow_patterns"]:
                    artifact = destination / relative
                    artifact.parent.mkdir(parents=True, exist_ok=True)
                    artifact.write_bytes(b"model")
                return str(destination)

            stt_download = Mock(side_effect=download_stt)
            snapshot_download = Mock(side_effect=download_snapshot)
            result = cache_speech_models(
                stt_model="small",
                stt_output_dir=root / "stt",
                stt_download=stt_download,
                snapshot_download=snapshot_download,
            )

        stt_download.assert_called_once()
        self.assertEqual(stt_download.call_args.kwargs["size_or_id"], "small")
        self.assertEqual(snapshot_download.call_count, len(TTS_MODEL_SNAPSHOTS))
        self.assertEqual(
            {call.kwargs["repo_id"] for call in snapshot_download.call_args_list},
            set(TTS_MODEL_SNAPSHOTS),
        )
        self.assertEqual(result["stt_model"], "small")
        self.assertEqual(result["tts_snapshots"], sorted(TTS_MODEL_SNAPSHOTS))

    def test_cache_rejects_an_incomplete_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            def download_stt(**kwargs):
                destination = Path(kwargs["output_dir"])
                destination.mkdir(parents=True, exist_ok=True)
                for relative in STT_REQUIRED_FILES:
                    (destination / relative).write_bytes(b"model")
                return str(destination)

            with self.assertRaisesRegex(RuntimeError, "snapshot is incomplete"):
                cache_speech_models(
                    stt_model="small",
                    stt_output_dir=root / "stt",
                    stt_download=download_stt,
                    snapshot_download=Mock(return_value=str(root / "empty")),
                )

    def test_cloud_run_image_uses_baked_models_without_hub_requests(self):
        backend_root = Path(__file__).resolve().parents[2]
        dockerfile = (backend_root / "Dockerfile").read_text(encoding="utf-8")
        cloud_run_environment = (
            backend_root / ".env.cloudrun.cpu.example"
        ).read_text(encoding="utf-8")

        self.assertIn("scripts/cache_speech_models.py", dockerfile)
        self.assertIn("--stt-model large-v3", dockerfile)
        self.assertNotIn("--stt-model large-v3-turbo", dockerfile)
        self.assertIn(
            "STT_MODEL=/opt/fipilot/models/faster-whisper-large-v3",
            dockerfile,
        )
        self.assertIn("HF_HUB_OFFLINE=1", dockerfile)
        self.assertIn("HF_HUB_DISABLE_XET=1", dockerfile)
        self.assertIn(
            "STT_MODEL=/opt/fipilot/models/faster-whisper-large-v3",
            cloud_run_environment,
        )
        self.assertIn("EVALUATOR_TASK_TYPE=complex", cloud_run_environment)


if __name__ == "__main__":
    unittest.main()
