"""Embed packaged role knowledge and publish it atomically to pgvector."""

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from collections import defaultdict
from collections.abc import Callable
from typing import Any, Protocol

from fipilot.knowledge_index import _documents, _embed_texts, _get_client, resolve_domain_folder
from fipilot.role_catalog import ROLE_CATALOG, role_definition
from fipilot.vector_store import EMBEDDING_DIMENSIONS, PgVectorKnowledgeStore

Embedder = Callable[[list[str]], list[list[float]]]


class RoleSnapshotStore(Protocol):
    def replace_role(
        self,
        *,
        role_id: str,
        role_title: str,
        chunks: list[dict[str, Any]],
    ) -> None: ...


def _default_embedder(texts: list[str]) -> list[list[float]]:
    return _embed_texts(_get_client(), texts)


def ingest_role(
    role: str,
    *,
    store: RoleSnapshotStore | None = None,
    embedder: Embedder | None = None,
) -> dict[str, Any]:
    """Replace one role snapshot only after every chunk has a valid embedding."""

    definition = role_definition(role)
    if definition is None:
        raise ValueError(f"Unsupported interview role: {role}")

    documents = _documents(resolve_domain_folder(definition["title"]))
    if not documents:
        raise ValueError(f"No knowledge documents found for {definition['title']}")

    embedding_inputs = [
        f"Interview role: {definition['title']}\nSource: {document['source']}\n\n{document['content']}"
        for document in documents
    ]
    embeddings = (embedder or _default_embedder)(embedding_inputs)
    if len(embeddings) != len(documents):
        raise ValueError("Embedding service returned a different number of vectors than chunks")
    if any(len(vector) != EMBEDDING_DIMENSIONS for vector in embeddings):
        raise ValueError(f"Every embedding must have {EMBEDDING_DIMENSIONS} dimensions")

    source_indexes: defaultdict[str, int] = defaultdict(int)
    chunks = []
    for document, embedding in zip(documents, embeddings, strict=True):
        source = document["source"]
        chunk_index = source_indexes[source]
        source_indexes[source] += 1
        identity = f"{definition['id']}|{source}|{chunk_index}"
        chunks.append(
            {
                "id": str(uuid.uuid5(uuid.NAMESPACE_URL, identity)),
                "source": source,
                "chunk_index": chunk_index,
                "content": document["content"],
                "content_hash": hashlib.sha256(
                    document["content"].encode("utf-8")
                ).hexdigest(),
                "embedding": embedding,
            }
        )

    target_store = store or PgVectorKnowledgeStore()
    target_store.replace_role(
        role_id=definition["id"],
        role_title=definition["title"],
        chunks=chunks,
    )
    return {
        "role_id": definition["id"],
        "role": definition["title"],
        "knowledge_domain": definition["knowledge_domain"],
        "chunks": len(chunks),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish interview knowledge to pgvector")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--role", help="Canonical role title or id")
    selection.add_argument("--all", action="store_true", help="Publish all supported roles")
    args = parser.parse_args()

    roles = [args.role] if args.role else [item["title"] for item in ROLE_CATALOG]
    for role in roles:
        print(json.dumps(ingest_role(role), ensure_ascii=False))


if __name__ == "__main__":
    main()
