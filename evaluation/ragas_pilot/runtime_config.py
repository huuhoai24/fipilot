from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from core.settings import Settings  # noqa: E402


def with_adc_project_fallback(
    settings: Settings,
    *,
    adc_project: str | None,
) -> Settings:
    if settings.google_cloud_project:
        return settings
    if not adc_project:
        raise RuntimeError(
            "The pilot requires GOOGLE_CLOUD_PROJECT or a project resolved by ADC"
        )
    return settings.model_copy(
        update={
            "google_cloud": settings.google_cloud.model_copy(
                update={"project": adc_project}
            )
        }
    )


def resolve_evaluation_settings(settings: Settings) -> Settings:
    if settings.google_cloud_project:
        return settings
    import google.auth

    _, adc_project = google.auth.default()
    return with_adc_project_fallback(settings, adc_project=adc_project)
