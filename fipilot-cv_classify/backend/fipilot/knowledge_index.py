"""Bounded hybrid retrieval over the packaged interview knowledge base."""

from __future__ import annotations

import argparse
import difflib
import json
import logging
import math
import os
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from fipilot.role_catalog import knowledge_domain_for_role

load_dotenv()

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "Knowledge"
INDEX_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
EMBED_MODEL = os.getenv("AZURE_EMBEDDING_MODEL", "text-embedding-3-small")
MAX_CHUNK_CHARS = 1800
BATCH_SIZE = 200
STOP_WORDS = {
    "and", "the", "with", "from", "for", "using", "built", "worked", "project",
    "engineer", "developer", "candidate", "how", "did", "this", "that", "into",
    "cua", "cho", "voi", "trong",
}

MORPHOLOGICAL_SUFFIXES = (
    "ization", "isation", "ability", "ibility", "ation", "ition", "ment", "ness",
    "ingly", "edly", "ing", "ed",
)


def _get_client() -> OpenAI:
    endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT", "").rstrip("/")
    api_key = os.getenv("AZURE_FOUNDRY_API_KEY", "")
    if not endpoint or not api_key:
        raise RuntimeError("Azure embedding service is not configured")
    return OpenAI(api_key=api_key, base_url=endpoint + "/openai/v1/")


def _normalize(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum())


def _stem_token(token: str) -> str:
    for suffix in MORPHOLOGICAL_SUFFIXES:
        if token.endswith(suffix) and len(token) - len(suffix) >= 4:
            token = token[:-len(suffix)]
            break
    if token.endswith("e") and len(token) > 4:
        token = token[:-1]
    elif token.endswith("s") and len(token) > 4:
        token = token[:-1]
    return token


def _tokens(value: str) -> set[str]:
    return {
        _stem_token(token)
        for token in re.findall(r"[a-z0-9+#]+", value.casefold())
        if len(token) >= 2 and token not in STOP_WORDS
    }


def resolve_domain_folder(role: str) -> Path:
    domains_root = KNOWLEDGE_DIR / "Domains"
    canonical_folder = knowledge_domain_for_role(role)
    if canonical_folder is not None:
        domain_dir = domains_root / canonical_folder
        if domain_dir.is_dir():
            return domain_dir
    candidates = sorted(d.name for d in domains_root.iterdir() if d.is_dir())
    normalized_candidates = [_normalize(candidate) for candidate in candidates]
    match = difflib.get_close_matches(
        _normalize(role), normalized_candidates, n=1, cutoff=0.62
    )
    if not match:
        raise ValueError(
            f"Cannot resolve role '{role}' to any Domain folder. Available: {candidates}"
        )
    return domains_root / candidates[normalized_candidates.index(match[0])]


def _split_markdown(content: str) -> list[str]:
    sections: list[str] = []
    current: list[str] = []
    for line in content.splitlines():
        if line.lstrip().startswith("#") and current:
            sections.append("\n".join(current).strip())
            current = []
        current.append(line)
    if current:
        sections.append("\n".join(current).strip())

    chunks: list[str] = []
    for section in sections:
        remaining = section
        while len(remaining) > MAX_CHUNK_CHARS:
            cut = remaining.rfind("\n", 0, MAX_CHUNK_CHARS)
            if cut < MAX_CHUNK_CHARS // 2:
                cut = remaining.rfind(" ", 0, MAX_CHUNK_CHARS)
            if cut <= 0:
                cut = MAX_CHUNK_CHARS
            chunks.append(remaining[:cut].strip())
            remaining = remaining[cut:].strip()
        if remaining:
            chunks.append(remaining)
    return chunks


@lru_cache(maxsize=16)
def _documents(domain_dir: Path) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    for path in sorted(domain_dir.rglob("*.md")):
        if not path.is_file():
            continue
        source = str(path.relative_to(KNOWLEDGE_DIR)).replace("\\", "/")
        for content in _split_markdown(path.read_text(encoding="utf-8")):
            documents.append({"source": source, "content": content})
    return documents


def _deduplicate_ranked_hits(hits: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
    unique: list[dict[str, Any]] = []
    seen_content: set[str] = set()
    for hit in hits:
        normalized_content = " ".join(str(hit.get("content", "")).casefold().split())
        if not normalized_content or normalized_content in seen_content:
            continue
        seen_content.add(normalized_content)
        unique.append(hit)
        if len(unique) == top_k:
            break
    return unique


def _lexical_search(query: str, documents: list[dict[str, str]], top_k: int) -> list[dict[str, Any]]:
    query_tokens = _tokens(query)
    if not query_tokens:
        return []
    tokenized_documents = [
        _tokens(f'{document["source"]} {document["content"]}')
        for document in documents
    ]
    document_frequency = Counter(
        token for tokens in tokenized_documents for token in tokens
    )
    document_count = max(len(documents), 1)

    def inverse_document_frequency(token: str) -> float:
        return math.log((document_count + 1) / (document_frequency[token] + 1)) + 1

    query_weight = sum(inverse_document_frequency(token) for token in query_tokens)
    scored: list[tuple[float, dict[str, str]]] = []
    for document, document_tokens in zip(documents, tokenized_documents, strict=True):
        source_tokens = _tokens(document["source"])
        content_tokens = _tokens(document["content"])
        source_score = sum(
            inverse_document_frequency(token)
            for token in query_tokens & source_tokens
        )
        content_score = sum(
            inverse_document_frequency(token)
            for token in query_tokens & content_tokens
        )
        coverage = len(query_tokens & document_tokens) / len(query_tokens)
        raw_score = source_score * 1.5 + content_score + coverage
        if raw_score > 0:
            scored.append((raw_score / query_weight, document))
    scored.sort(key=lambda item: (-item[0], item[1]["source"]))
    ranked_hits = [
        {
            "source": document["source"],
            "path": document["source"],
            "content": document["content"][:MAX_CHUNK_CHARS],
            "score": round(score, 4),
            "method": "lexical",
        }
        for score, document in scored
    ]
    return _deduplicate_ranked_hits(ranked_hits, top_k)


def _embed_texts(client: OpenAI, texts: list[str]) -> list[list[float]]:
    vectors = []
    for index in range(0, len(texts), BATCH_SIZE):
        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=texts[index : index + BATCH_SIZE],
        )
        vectors.extend(item.embedding for item in response.data)
    return vectors


def _build_index(domain_dir: Path) -> Path:
    import numpy as np

    documents = _documents(domain_dir)
    if not documents:
        raise ValueError(f"No Markdown knowledge was found in {domain_dir}")
    texts = [document["content"] for document in documents]
    embeddings = np.array(_embed_texts(_get_client(), texts), dtype=np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings /= np.where(norms == 0, 1, norms)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_path = INDEX_DIR / f"domain_index_{domain_dir.name}.npz"
    np.savez_compressed(
        index_path,
        embeddings=embeddings,
        sources=np.array([document["source"] for document in documents]),
        texts=np.array(texts),
    )
    return index_path


def _vector_search(query: str, index_path: Path, top_k: int) -> list[dict[str, Any]]:
    import numpy as np

    data = np.load(index_path, allow_pickle=False)
    embeddings = data["embeddings"]
    if "sources" in data and "texts" in data:
        sources = data["sources"].astype(str)
        texts = data["texts"].astype(str)
    else:
        legacy = data["paths"].astype(str)
        sources = np.array([value.split("\n", 1)[0] for value in legacy])
        texts = np.array([value.split("\n", 1)[-1] for value in legacy])

    [query_vector] = _embed_texts(_get_client(), [query])
    vector = np.array(query_vector, dtype=np.float32)
    norm = np.linalg.norm(vector)
    if norm == 0:
        return []
    scores = embeddings @ (vector / norm)
    indexes = np.argsort(scores)[::-1][:top_k]
    return [
        {
            "source": sources[index],
            "path": sources[index],
            "content": texts[index][:MAX_CHUNK_CHARS],
            "score": round(float(scores[index]), 4),
            "method": "vector",
        }
        for index in indexes
        if scores[index] > 0
    ]


def build_index(role: str) -> Path:
    return _build_index(resolve_domain_folder(role))


def build_all_indexes() -> None:
    for domain_dir in sorted((KNOWLEDGE_DIR / "Domains").iterdir()):
        if domain_dir.is_dir():
            _build_index(domain_dir)


def search_domain(query: str, role: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Retrieve bounded knowledge chunks, using vectors when an index is available."""

    if os.getenv("KNOWLEDGE_RETRIEVAL_BACKEND", "local").casefold() == "pgvector":
        try:
            from fipilot.vector_store import search_pgvector

            database_hits = search_pgvector(query, role, top_k)
            if database_hits:
                return _deduplicate_ranked_hits(database_hits, top_k)
        except Exception:
            logger.warning(
                "pgvector retrieval failed; using packaged knowledge fallback",
                exc_info=True,
            )

    domain_dir = resolve_domain_folder(role)
    documents = _documents(domain_dir)
    lexical_hits = _lexical_search(query, documents, top_k)
    index_path = INDEX_DIR / f"domain_index_{domain_dir.name}.npz"
    if not index_path.exists():
        return lexical_hits
    try:
        vector_hits = _vector_search(query, index_path, top_k)
    except (ImportError, RuntimeError, OSError, ValueError):
        return lexical_hits

    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for hit in lexical_hits:
        merged[(hit["source"], hit["content"])] = {**hit, "score": hit["score"] * 0.35}
    for hit in vector_hits:
        key = (hit["source"], hit["content"])
        if key in merged:
            merged[key]["score"] += hit["score"] * 0.65
            merged[key]["method"] = "hybrid"
        else:
            merged[key] = {**hit, "score": hit["score"] * 0.65}
    ranked_hits = sorted(merged.values(), key=lambda hit: (-hit["score"], hit["source"]))
    return _deduplicate_ranked_hits(ranked_hits, top_k)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or search interview knowledge indexes")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--role", default="AI Engineer")
    subparsers.add_parser("build-all")
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--role", default="AI Engineer")
    search_parser.add_argument("--desc", required=True)
    search_parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    if args.command == "build":
        print(build_index(args.role))
    elif args.command == "build-all":
        build_all_indexes()
    else:
        print(json.dumps(search_domain(args.desc, args.role, args.top_k), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
