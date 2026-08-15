from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from evaluation.ragas_pilot.dataset import build_controlled_case_specs


CATALOG_PATH = Path("backend/services/interview_knowledge/catalog.json")


def test_controlled_cases_are_derived_from_real_catalog_metadata() -> None:
    specs = build_controlled_case_specs(CATALOG_PATH, limit=30)
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    catalog_topics = {
        (domain, entry["title"], tuple(entry.get("path", [])))
        for domain, entries in catalog["domains"].items()
        for entry in entries
    }

    assert len(specs) == 30
    assert Counter(spec.domain_key for spec in specs) == {
        domain: 3 for domain in catalog["domains"]
    }
    assert all(spec.source_type == "synthetic_controlled" for spec in specs)
    assert all(
        (spec.domain_key, spec.topic_title, tuple(spec.topic_path)) in catalog_topics
        for spec in specs
    )
    assert all(spec.sample_id.startswith("pilot-") for spec in specs)
