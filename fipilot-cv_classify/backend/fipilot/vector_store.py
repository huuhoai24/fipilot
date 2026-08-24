"""PostgreSQL pgvector adapter for interview knowledge retrieval."""

from __future__ import annotations

import math
import re
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from fipilot.database import get_engine
from fipilot.role_catalog import role_definition

EMBEDDING_DIMENSIONS = 1536
RRF_K = 60
LEXICAL_STOP_WORDS = {
    "and", "the", "with", "from", "for", "using", "built", "worked",
    "project", "engineer", "developer", "target", "role", "experience",
    "position", "this", "that", "into", "cua", "cho", "voi", "trong",
}

VECTOR_SEARCH_SQL = text(
    """
    SELECT
        source,
        content,
        1 - (embedding <=> CAST(:embedding AS vector)) AS score
    FROM knowledge_chunks
    WHERE role_id = :role_id
    ORDER BY embedding <=> CAST(:embedding AS vector)
    LIMIT :candidate_k
    """
)

LEXICAL_SEARCH_SQL = text(
    """
    WITH search_query AS (
        SELECT websearch_to_tsquery('simple', :lexical_query) AS value
    )
    SELECT
        source,
        content,
        ts_rank_cd(search_vector, search_query.value) AS score
    FROM knowledge_chunks, search_query
    WHERE role_id = :role_id
      AND search_vector @@ search_query.value
    ORDER BY score DESC
    LIMIT :candidate_k
    """
)

REPLACE_ROLE_SQL = text(
    """
    INSERT INTO knowledge_chunks (
        id,
        role_id,
        role_title,
        source,
        chunk_index,
        content,
        content_hash,
        embedding
    ) VALUES (
        :id,
        :role_id,
        :role_title,
        :source,
        :chunk_index,
        :content,
        :content_hash,
        CAST(:embedding AS vector)
    )
    """
)


def _vector_literal(vector: list[float]) -> str:
    if len(vector) != EMBEDDING_DIMENSIONS:
        raise ValueError(
            f"Expected a {EMBEDDING_DIMENSIONS}-dimension embedding, got {len(vector)}"
        )
    values = [float(value) for value in vector]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Embedding contains a non-finite value")
    return "[" + ",".join(format(value, ".9g") for value in values) + "]"


def _lexical_query(query: str) -> str:
    tokens = []
    seen = set()
    for token in re.findall(r"[\w+#.]+", query.casefold()):
        clean = token.strip(".")
        if len(clean) < 2 or clean in LEXICAL_STOP_WORDS or clean in seen:
            continue
        seen.add(clean)
        tokens.append(clean)
    return " OR ".join(tokens[:32])


def _fuse_rankings(
    vector_rows: list[dict[str, Any]],
    lexical_rows: list[dict[str, Any]],
    top_k: int,
) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for method, rows in (("pgvector", vector_rows), ("postgres-lexical", lexical_rows)):
        for rank, row in enumerate(rows, start=1):
            source = str(row["source"])
            content = str(row["content"])
            key = (source, content)
            hit = merged.setdefault(
                key,
                {
                    "source": source,
                    "path": source,
                    "content": content,
                    "score": 0.0,
                    "methods": set(),
                },
            )
            hit["score"] += 1 / (RRF_K + rank)
            hit["methods"].add(method)

    results = []
    for hit in merged.values():
        methods = hit.pop("methods")
        hit["score"] = round(hit["score"], 6)
        hit["method"] = (
            "pgvector-hybrid" if len(methods) > 1 else next(iter(methods))
        )
        results.append(hit)
    return sorted(results, key=lambda hit: (-hit["score"], hit["source"]))[:top_k]


class PgVectorKnowledgeStore:
    """Store and retrieve a complete role knowledge snapshot in PostgreSQL."""

    def __init__(self, engine: Engine | None = None):
        self.engine = engine or get_engine()
        if self.engine is None:
            raise RuntimeError("DATABASE_URL is required for pgvector retrieval")

    def search(
        self,
        *,
        role_id: str,
        query: str,
        query_embedding: list[float],
        top_k: int,
    ) -> list[dict[str, Any]]:
        candidate_k = max(top_k * 4, 20)
        parameters = {
            "role_id": role_id,
            "query": query,
            "lexical_query": _lexical_query(query),
            "embedding": _vector_literal(query_embedding),
            "candidate_k": candidate_k,
        }
        with self.engine.connect() as connection:
            vector_rows = list(
                connection.execute(VECTOR_SEARCH_SQL, parameters).mappings().all()
            )
            lexical_rows = list(
                connection.execute(LEXICAL_SEARCH_SQL, parameters).mappings().all()
            )
        return _fuse_rankings(vector_rows, lexical_rows, top_k)

    def replace_role(
        self,
        *,
        role_id: str,
        role_title: str,
        chunks: list[dict[str, Any]],
    ) -> None:
        parameters = [
            {
                **chunk,
                "role_id": role_id,
                "role_title": role_title,
                "embedding": _vector_literal(chunk["embedding"]),
            }
            for chunk in chunks
        ]
        with self.engine.begin() as connection:
            connection.execute(
                text("DELETE FROM knowledge_chunks WHERE role_id = :role_id"),
                {"role_id": role_id},
            )
            if parameters:
                connection.execute(REPLACE_ROLE_SQL, parameters)


def search_pgvector(query: str, role: str, top_k: int) -> list[dict[str, Any]]:
    definition = role_definition(role)
    if definition is None:
        return []

    from fipilot.knowledge_index import _embed_texts, _get_client

    [query_embedding] = _embed_texts(_get_client(), [query])
    return PgVectorKnowledgeStore().search(
        role_id=definition["id"],
        query=query,
        query_embedding=query_embedding,
        top_k=top_k,
    )
