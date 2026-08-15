from __future__ import annotations

import math
import re
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class RetrievalConfig:
    embedding_model: str = "gemini-embedding-001"
    output_dimensionality: int = 768
    vector_database: str = "Cloud Firestore Vector Search"
    collection: str = "interview_knowledge_chunks"
    vector_field: str = "embedding"
    top_k: int = 5
    similarity_metric: str = "COSINE"


@dataclass(frozen=True)
class KnowledgeChunk:
    chunk_id: str
    domain: str
    text: str


@dataclass(frozen=True)
class SearchResult:
    rank: int
    chunk_id: str
    domain: str
    score: float
    text: str


@dataclass(frozen=True)
class PrototypeState:
    config: RetrievalConfig
    indexed_chunks: int
    simulated_dimensions: int
    query: str = ""
    query_vector: tuple[float, ...] = ()
    results: tuple[SearchResult, ...] = ()


CONCEPTS: tuple[tuple[str, ...], ...] = (
    ("python", "fastapi", "api", "backend", "server"),
    ("database", "postgresql", "sql", "transaction", "firestore"),
    ("rag", "retrieval", "embedding", "vector", "similarity"),
    ("llm", "prompt", "gemini", "agent", "langgraph", "orchestration"),
    ("machine", "learning", "model", "pytorch", "training", "inference"),
    ("docker", "kubernetes", "cloud", "devops", "deployment"),
    ("react", "typescript", "frontend", "browser", "ui"),
    ("test", "testing", "playwright", "pytest", "quality"),
    ("speech", "stt", "tts", "audio", "whisper", "voice"),
    ("state", "memory", "session", "workflow", "transition"),
    ("độ trễ", "latency", "timeout", "retry", "performance"),
    ("tiếng việt", "vietnamese", "multilingual", "language"),
)


CHUNKS: tuple[KnowledgeChunk, ...] = (
    KnowledgeChunk("backend-001", "Backend", "FastAPI dependency boundaries, REST APIs, request timeouts, and bounded retries."),
    KnowledgeChunk("database-001", "Backend", "PostgreSQL transactions, optimistic concurrency, and idempotent writes."),
    KnowledgeChunk("rag-001", "AI Engineer", "RAG retrieves relevant competency chunks with embeddings and vector similarity."),
    KnowledgeChunk("agent-001", "AI Engineer", "Agent workflow state, LangGraph-style orchestration, memory, and reliable transitions."),
    KnowledgeChunk("ml-001", "AI Engineer", "PyTorch model training, evaluation, inference optimization, and feature caching."),
    KnowledgeChunk("cloud-001", "DevOps", "Docker containers deployed to Cloud Run with observability and bounded scaling."),
    KnowledgeChunk("frontend-001", "Frontend", "React and TypeScript browser UI with accessible state feedback."),
    KnowledgeChunk("testing-001", "QA", "Playwright end-to-end testing, pytest contracts, and regression evidence."),
    KnowledgeChunk("speech-001", "Speech", "Vietnamese speech recognition using Whisper STT with technical vocabulary."),
    KnowledgeChunk("latency-001", "Architecture", "Measure API latency, model timeout, retry behavior, and cold-start performance."),
)


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9+#.]+|[à-ỹ]+(?:\s+[à-ỹ]+)?", text.casefold()))


def fake_embed(text: str) -> tuple[float, ...]:
    """Deterministic stand-in for the proposed Vertex embedding call."""
    lowered = text.casefold()
    tokens = _tokens(text)
    values = []
    for terms in CONCEPTS:
        score = sum(1.0 for term in terms if term in tokens or term in lowered)
        values.append(score)
    magnitude = math.sqrt(sum(value * value for value in values))
    if magnitude == 0:
        return tuple(0.0 for _ in values)
    return tuple(value / magnitude for value in values)


def cosine_similarity(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


INDEX = tuple((chunk, fake_embed(chunk.text)) for chunk in CHUNKS)


def initial_state() -> PrototypeState:
    return PrototypeState(
        config=RetrievalConfig(),
        indexed_chunks=len(INDEX),
        simulated_dimensions=len(CONCEPTS),
    )


def retrieve(state: PrototypeState, query: str) -> PrototypeState:
    query_vector = fake_embed(query)
    scored = sorted(
        (
            (cosine_similarity(query_vector, vector), chunk)
            for chunk, vector in INDEX
        ),
        key=lambda item: (-item[0], item[1].chunk_id),
    )[: state.config.top_k]
    results = tuple(
        SearchResult(
            rank=index,
            chunk_id=chunk.chunk_id,
            domain=chunk.domain,
            score=score,
            text=chunk.text,
        )
        for index, (score, chunk) in enumerate(scored, start=1)
    )
    return replace(
        state,
        query=query,
        query_vector=query_vector,
        results=results,
    )
