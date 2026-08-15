from __future__ import annotations

import sys
from pathlib import Path


BACKEND_ROOT = Path("backend").resolve()
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from core.settings import Settings  # noqa: E402
from evaluation.ragas_pilot.runtime_config import with_adc_project_fallback  # noqa: E402


def test_adc_project_fallback_configures_only_the_evaluation_copy() -> None:
    original = Settings(google_cloud={"project": None, "location": "us-central1"})

    resolved = with_adc_project_fallback(original, adc_project="pilot-project")

    assert original.google_cloud_project is None
    assert resolved.google_cloud_project == "pilot-project"
    assert resolved.google_cloud_location == "us-central1"
