from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DOMAIN_KEYS = {
    "ai_enginner": "AI_Engineer",
    "ai_engineer": "AI_Engineer",
    "backend_developer": "Backend_Developer",
    "back_end_developer": "Backend_Developer",
    "business_analyst": "Business_Analyst",
    "data_engineer": "Data_Engineer",
    "data_scientist": "Data_Scientist",
    "devops_engineer": "DevOps_Engineer",
    "full_stack_developer": "Full_Stack_Developer",
    "software_engineer": "Software_Engineer",
    "tester_qa_qc": "Tester_QA_QC",
    "web_developer": "Web_Developer",
}


def _domain_key(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return DOMAIN_KEYS.get(normalized, normalized.title())


def _clean_section(value: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", value).strip()


def _markdown_summary(path: Path) -> tuple[str, list[str]]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    title = path.stem
    anchors: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
        elif stripped.startswith("- ") and len(anchors) < 8:
            anchor = stripped[2:].strip()
            if anchor:
                anchors.append(anchor[:240])
    return title, anchors


def build_catalog(source_root: Path) -> dict:
    domains_root = source_root / "Domains"
    levels_root = source_root / "Levels"
    if not domains_root.is_dir() or not levels_root.is_dir():
        raise FileNotFoundError(
            f"Expected Domains and Levels under knowledge source: {source_root}"
        )

    domains: dict[str, list[dict]] = {}
    for domain_dir in sorted(path for path in domains_root.iterdir() if path.is_dir()):
        key = _domain_key(domain_dir.name)
        entries = domains.setdefault(key, [])
        for markdown_path in sorted(domain_dir.rglob("*.md")):
            title, anchors = _markdown_summary(markdown_path)
            relative_parts = markdown_path.relative_to(domain_dir).parts[:-1]
            entries.append(
                {
                    "title": title,
                    "path": [_clean_section(part) for part in relative_parts],
                    "anchors": anchors,
                }
            )

    levels: dict[str, dict[str, list[str]]] = {}
    for domain_dir in sorted(path for path in levels_root.iterdir() if path.is_dir()):
        key = _domain_key(domain_dir.name)
        domain_levels = levels.setdefault(key, {})
        for markdown_path in sorted(domain_dir.glob("*.md")):
            _, anchors = _markdown_summary(markdown_path)
            domain_levels[markdown_path.stem.title()] = anchors

    return {"version": 1, "domains": domains, "levels": levels}


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Build the packaged interview knowledge catalog")
    parser.add_argument("--source", type=Path, default=repo_root / "Knowledge")
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root
        / "backend"
        / "services"
        / "interview_knowledge"
        / "catalog.json",
    )
    args = parser.parse_args()

    catalog = build_catalog(args.source.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    topic_count = sum(len(entries) for entries in catalog["domains"].values())
    print(f"Wrote {topic_count} topics across {len(catalog['domains'])} domains to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
