from __future__ import annotations

import argparse
import os
from pathlib import Path

import google.auth
from google.cloud import firestore

from infrastructure.interview_knowledge.firestore_vector import (
    CatalogVectorIndexer,
    VertexTextEmbedder,
)
from services.interview_knowledge.chunks import build_catalog_chunks


DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "services" / "interview_knowledge" / "catalog.json"


def _resolve_project(explicit_project: str | None) -> str:
    if explicit_project:
        return explicit_project
    environment_project = os.getenv("GOOGLE_CLOUD_PROJECT")
    if environment_project:
        return environment_project
    _, adc_project = google.auth.default()
    if not adc_project:
        raise RuntimeError(
            "Set GOOGLE_CLOUD_PROJECT or configure Application Default Credentials"
        )
    return adc_project


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Embed and idempotently index FiPilot interview knowledge in Firestore."
    )
    parser.add_argument("--project")
    parser.add_argument("--database", default="(default)")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--collection", default="interview_knowledge_chunks")
    parser.add_argument("--vector-field", default="embedding")
    parser.add_argument("--model", default="gemini-embedding-001")
    parser.add_argument("--location", default="global")
    parser.add_argument("--dimensions", type=int, default=768)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    project = _resolve_project(args.project)
    chunks = build_catalog_chunks(args.catalog)
    if args.limit is not None:
        if args.limit < 1:
            parser.error("--limit must be at least 1")
        chunks = chunks[: args.limit]

    print(f"Project: {project}")
    print(f"Database: {args.database}")
    print(f"Collection: {args.collection}")
    print(f"Model: {args.model}")
    print(f"Dimensions: {args.dimensions}")
    print(f"Chunks selected: {len(chunks)}")
    if not args.apply:
        print("Dry run only. Re-run with --apply to call Vertex AI and write Firestore.")
        return 0

    firestore_client = firestore.Client(project=project, database=args.database)
    embedder = VertexTextEmbedder(
        project=project,
        location=args.location,
        model=args.model,
        dimensions=args.dimensions,
    )
    indexer = CatalogVectorIndexer(
        firestore_client=firestore_client,
        embedder=embedder,
        collection_name=args.collection,
        vector_field=args.vector_field,
        batch_size=100,
        max_workers=args.workers,
    )

    def report_progress(position: int, total: int) -> None:
        if position == total or position % 25 == 0:
            print(f"Progress: {position}/{total}", flush=True)

    summary = indexer.sync(chunks, on_progress=report_progress)
    print(f"Unchanged: {summary.skipped_unchanged}")
    print(f"Embedded and written: {summary.embedded_and_written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
