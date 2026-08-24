from __future__ import annotations

import hashlib
import json
import math
import random
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pymupdf


SCHEMA_VERSION = "cv-question-rag.dataset.v1"


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
        ),
        encoding="utf-8",
    )


def _normalized(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[a-z0-9+#.]+", value))


def _contains_phrase(text: str, phrase: str) -> bool:
    normalized_phrase = _normalized(phrase)
    if len(normalized_phrase) < 3:
        return False
    return f" {normalized_phrase} " in f" {text} "


def _topic_id(domain: str, entry: dict[str, Any]) -> str:
    identity = "|".join(
        [domain, *entry.get("path", []), str(entry.get("title", ""))]
    )
    return "topic_" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]


def _extract_pdf(path: Path) -> tuple[str, int]:
    with pymupdf.open(path) as document:
        return "\n".join(page.get_text() for page in document), document.page_count


def _matches(text: str, catalog: dict[str, Any]) -> list[dict[str, Any]]:
    normalized_text = _normalized(text)
    matches: list[dict[str, Any]] = []
    for domain, entries in catalog.get("domains", {}).items():
        for entry in entries:
            title = str(entry.get("title", "")).strip()
            if not title or not _contains_phrase(normalized_text, title):
                continue
            matches.append(
                {
                    "domain": domain,
                    "title": title,
                    "topic_id": _topic_id(domain, entry),
                    "path": [str(value) for value in entry.get("path", [])],
                    "match_token_count": len(_normalized(title).split()),
                    "match_character_count": len(_normalized(title)),
                }
            )
    matches.sort(
        key=lambda row: (
            -row["match_token_count"],
            -row["match_character_count"],
            row["domain"],
            row["title"].casefold(),
        )
    )
    return matches


def _domain_matches(matches: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for match in matches:
        by_domain[match["domain"]].append(match)
    domain = max(
        by_domain,
        key=lambda key: (
            sum(row["match_token_count"] for row in by_domain[key]),
            sum(row["match_character_count"] for row in by_domain[key]),
            len(by_domain[key]),
            key,
        ),
    )
    return domain, by_domain[domain]


def _safe_profile(resume_id: str, domain: str, matches: list[dict[str, Any]]) -> dict[str, Any]:
    skills = list(dict.fromkeys(row["title"] for row in matches))[:8]
    role = domain.replace("_", " ")
    return {
        "name": f"Candidate {resume_id}",
        "years_experience": None,
        "recent_role": role,
        "specialization": role,
        "skills": skills,
        "skill_evidence": [
            {"skill": skill, "evidence": ["Exact catalog term detected in Resume"]}
            for skill in skills
        ],
        "projects": [
            {
                "name": "Redacted Resume evidence",
                "description": "Public Resume contains the selected catalog skills.",
                "technologies": skills,
                "role": role,
            }
        ],
        "experiences": [],
        "education": None,
    }


def _balanced_sample(rows: list[dict[str, Any]], count: int, seed: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["domain"]].append(row)
    for domain, values in grouped.items():
        random.Random(seed + int(hashlib.sha256(domain.encode()).hexdigest()[:8], 16)).shuffle(values)
    selected: list[dict[str, Any]] = []
    domain_names = sorted(grouped)
    while len(selected) < min(count, len(rows)):
        progressed = False
        for domain in domain_names:
            if grouped[domain] and len(selected) < count:
                selected.append(grouped[domain].pop())
                progressed = True
        if not progressed:
            break
    return selected


def _stratified_paths(
    paths: list[Path], *, corpus_dir: Path, limit: int | None, seed: int
) -> list[Path]:
    if limit is None or limit >= len(paths):
        return paths
    if limit < 1:
        raise ValueError("corpus_limit must be positive")
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in paths:
        grouped[path.relative_to(corpus_dir).parts[0]].append(path)
    for category, values in grouped.items():
        random.Random(
            seed + int(hashlib.sha256(category.encode()).hexdigest()[:8], 16)
        ).shuffle(values)
    selected: list[Path] = []
    while len(selected) < limit:
        progressed = False
        for category in sorted(grouped):
            if grouped[category] and len(selected) < limit:
                selected.append(grouped[category].pop())
                progressed = True
        if not progressed:
            break
    return selected


def _split(
    rows: list[dict[str, Any]], development_ratio: float, seed: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not 0 < development_ratio < 1:
        raise ValueError("development_ratio must be between zero and one")
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[row["domain"]].append(row)
    target = round(len(rows) * development_ratio)
    allocations = {
        domain: math.floor(len(values) * development_ratio)
        for domain, values in groups.items()
    }
    remaining = target - sum(allocations.values())
    priority = sorted(
        groups,
        key=lambda domain: (
            -(len(groups[domain]) * development_ratio - allocations[domain]),
            domain,
        ),
    )
    for domain in priority[:remaining]:
        allocations[domain] += 1
    development: list[dict[str, Any]] = []
    holdout: list[dict[str, Any]] = []
    for domain in sorted(groups):
        values = sorted(groups[domain], key=lambda row: row["resume_id"])
        random.Random(seed + int(hashlib.sha256(domain.encode()).hexdigest()[:8], 16)).shuffle(values)
        development.extend(values[: allocations[domain]])
        holdout.extend(values[allocations[domain] :])
    random.Random(seed).shuffle(development)
    random.Random(seed + 1).shuffle(holdout)
    return development, holdout


def prepare_dataset(
    *,
    corpus_dir: Path,
    catalog_path: Path,
    output_dir: Path,
    corpus_limit: int | None = None,
    sample_size: int = 300,
    development_ratio: float = 0.7,
    seed: int = 20260820,
) -> dict[str, Any]:
    """Create a reproducible, privacy-safe Resume-derived evaluation dataset."""
    if sample_size < 1:
        raise ValueError("sample_size must be positive")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    source_files = sorted(
        path
        for path in corpus_dir.rglob("*.pdf")
        if path.is_file() and "CHON_LOC_CV" in path.parts
    )
    files = _stratified_paths(
        source_files, corpus_dir=corpus_dir, limit=corpus_limit, seed=seed
    )
    seen_hashes: set[str] = set()
    candidates: list[dict[str, Any]] = []
    duplicates = 0
    unreadable = 0
    unmatched = 0
    for path in files:
        content = path.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if digest in seen_hashes:
            duplicates += 1
            continue
        seen_hashes.add(digest)
        try:
            text, pages = _extract_pdf(path)
        except Exception:
            unreadable += 1
            continue
        matches = _matches(text, catalog)
        if not matches:
            unmatched += 1
            continue
        domain, selected_matches = _domain_matches(matches)
        resume_id = f"CV-{digest[:12].upper()}"
        target = selected_matches[0]
        category = path.relative_to(corpus_dir).parts[0]
        candidates.append(
            {
                "resume_id": resume_id,
                "category": category,
                "source_bucket": "CHON_LOC_CV",
                "document_type": "pdf",
                "document_bytes": len(content),
                "document_pages": pages,
                "extractable_characters": len(text),
                "domain": domain,
                "level": "Middle",
                "language": "vi" if len(candidates) % 2 == 0 else "en",
                "target_topic_id": target["topic_id"],
                "target_topic": target["title"],
                "matched_topics": [
                    {"topic_id": row["topic_id"], "title": row["title"]}
                    for row in selected_matches[:8]
                ],
                "candidate_profile": _safe_profile(resume_id, domain, selected_matches),
                "label_source": "resume_exact_catalog_title",
                "source": "public_resume_derived",
            }
        )

    selected = _balanced_sample(candidates, sample_size, seed)
    development, holdout = _split(selected, development_ratio, seed)
    selected_sorted = sorted(selected, key=lambda row: row["resume_id"])
    _write_jsonl(output_dir / "corpus_manifest.jsonl", selected_sorted)
    _write_jsonl(output_dir / "development.jsonl", development)
    _write_jsonl(output_dir / "holdout.jsonl", holdout)
    summary = {
        "schema_version": SCHEMA_VERSION,
        "seed": seed,
        "privacy": {
            "source_is_public": True,
            "filenames_recorded": False,
            "resume_text_recorded": False,
            "personal_fields_recorded": False,
            "identifier": "CV- plus first 12 uppercase characters of SHA-256",
        },
        "inventory": {
            "source_pdf_files": len(source_files),
            "pdf_files": len(files),
            "corpus_limit": corpus_limit,
            "unique_files": len(seen_hashes),
            "duplicate_files": duplicates,
            "unreadable_files": unreadable,
            "unique_unmatched_files": unmatched,
            "eligible_files": len(candidates),
        },
        "dataset": {
            "requested": sample_size,
            "selected": len(selected),
            "development": len(development),
            "holdout": len(holdout),
            "domains": dict(sorted(Counter(row["domain"] for row in selected).items())),
            "categories": dict(sorted(Counter(row["category"] for row in selected).items())),
            "dataset_hash": _canonical_hash(selected_sorted),
        },
        "claim_boundary": (
            "Resume-derived exact catalog-title labels are source-derived, not human relevance labels; "
            "the dataset does not measure Resume extraction accuracy."
        ),
    }
    _write_json(output_dir / "DATASET_MANIFEST.json", summary)
    return summary
