from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from collections.abc import Callable
from typing import Any

from google.cloud import firestore
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector
from google.genai import types

from services.interview_knowledge.chunks import KnowledgeChunk
from shared.schemas import CandidateProfile, InterviewConfig


class VertexTextEmbedder:
    """Generate fixed-size Vertex embeddings for asymmetric retrieval."""

    def __init__(
        self,
        *,
        project: str,
        location: str = "global",
        model: str = "gemini-embedding-001",
        dimensions: int = 768,
        client: Any | None = None,
        max_attempts: int = 3,
    ) -> None:
        if not project:
            raise ValueError("A Google Cloud project is required for embeddings")
        if not 1 <= dimensions <= 2048:
            raise ValueError("Embedding dimensions must be between 1 and 2048")
        self.project = project
        self.location = location
        self.model = model
        self.dimensions = dimensions
        self.max_attempts = max(1, max_attempts)
        self._client = client or self._create_client()

    def _create_client(self):
        from google import genai

        return genai.Client(
            vertexai=True,
            project=self.project,
            location=self.location,
        )

    def embed_document(self, text: str, *, title: str) -> tuple[float, ...]:
        return self._embed(text, task_type="RETRIEVAL_DOCUMENT", title=title)

    def embed_query(self, text: str) -> tuple[float, ...]:
        return self._embed(text, task_type="RETRIEVAL_QUERY", title=None)

    def _embed(
        self,
        text: str,
        *,
        task_type: str,
        title: str | None,
    ) -> tuple[float, ...]:
        if not text.strip():
            raise ValueError("Embedding input cannot be blank")
        response = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                response = self._client.models.embed_content(
                    model=self.model,
                    contents=text,
                    config=types.EmbedContentConfig(
                        task_type=task_type,
                        output_dimensionality=self.dimensions,
                        title=title,
                    ),
                )
                break
            except Exception:
                if attempt >= self.max_attempts:
                    raise
                time.sleep(min(4.0, 0.5 * (2 ** (attempt - 1))))
        if response is None:  # pragma: no cover - loop always returns or raises
            raise RuntimeError("Vertex returned no embedding response")
        embeddings = response.embeddings or []
        if len(embeddings) != 1 or embeddings[0].values is None:
            raise RuntimeError("Vertex returned no embedding")
        values = tuple(float(value) for value in embeddings[0].values)
        if len(values) != self.dimensions:
            raise RuntimeError(
                f"Vertex returned {len(values)} dimensions; expected {self.dimensions}"
            )
        return values


def build_vector_query_text(
    candidate_profile: CandidateProfile,
    interview_config: InterviewConfig,
) -> str:
    """Project only interview-relevant fields; omit candidate identity."""

    values = [
        f"Target role: {candidate_profile.recent_role or candidate_profile.specialization or 'IT professional'}",
        f"Experience level: {interview_config.experience_level}",
        f"Interview language: {interview_config.language}",
    ]
    if candidate_profile.specialization:
        values.append(f"Specialization: {candidate_profile.specialization}")
    if candidate_profile.skills:
        values.append("Skills: " + ", ".join(candidate_profile.skills))
    if interview_config.objective:
        values.append(f"Objective: {interview_config.objective}")
    return "\n".join(values)


class FirestoreVectorKnowledgeRetriever:
    """Retrieve bounded planner context through Firestore KNN vector search."""

    def __init__(
        self,
        *,
        firestore_client: Any,
        embedder: VertexTextEmbedder,
        collection_name: str = "interview_knowledge_chunks",
        vector_field: str = "embedding",
        top_k: int = 5,
    ) -> None:
        if not 1 <= top_k <= 1000:
            raise ValueError("top_k must be between 1 and 1000")
        self._collection = firestore_client.collection(collection_name)
        self.embedder = embedder
        self.collection_name = collection_name
        self.vector_field = vector_field
        self.top_k = top_k

    def retrieve_topics(
        self,
        candidate_profile: CandidateProfile,
        interview_config: InterviewConfig,
    ) -> list[str]:
        query_text = build_vector_query_text(candidate_profile, interview_config)
        query_vector = self.embedder.embed_query(query_text)
        vector_query = self._collection.find_nearest(
            vector_field=self.vector_field,
            query_vector=Vector(query_vector),
            limit=self.top_k,
            distance_measure=DistanceMeasure.COSINE,
            distance_result_field="vector_distance",
        )
        results: list[str] = []
        for snapshot in vector_query.stream():
            data = snapshot.to_dict() or {}
            title = str(data.get("title", "")).strip()
            if not title:
                continue
            path = [str(value) for value in data.get("path", [])]
            topic_path = " > ".join((*path, title))
            context = f"Candidate-aligned topic: {topic_path}"
            anchors = [str(value) for value in data.get("anchors", [])]
            if anchors:
                context += " | anchors: " + "; ".join(anchors[:5])
            distance = data.get("vector_distance")
            if isinstance(distance, int | float):
                similarity = max(-1.0, min(1.0, 1.0 - float(distance)))
                context += f" | cosine similarity: {similarity:.4f}"
            results.append(context)
        return results


@dataclass(frozen=True)
class IndexingSummary:
    total_chunks: int
    skipped_unchanged: int
    embedded_and_written: int


class CatalogVectorIndexer:
    """Idempotently embed and upsert catalog chunks into one collection."""

    def __init__(
        self,
        *,
        firestore_client: Any,
        embedder: VertexTextEmbedder,
        collection_name: str = "interview_knowledge_chunks",
        vector_field: str = "embedding",
        batch_size: int = 400,
        max_workers: int = 1,
    ) -> None:
        if not 1 <= batch_size <= 500:
            raise ValueError("batch_size must be between 1 and 500")
        if not 1 <= max_workers <= 32:
            raise ValueError("max_workers must be between 1 and 32")
        self._client = firestore_client
        self._collection = firestore_client.collection(collection_name)
        self.embedder = embedder
        self.collection_name = collection_name
        self.vector_field = vector_field
        self.batch_size = batch_size
        self.max_workers = max_workers

    def sync(
        self,
        chunks: list[KnowledgeChunk],
        *,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> IndexingSummary:
        metadata_fields = [
            "content_sha256",
            "embedding_model",
            "embedding_dimensions",
        ]
        existing = {
            snapshot.id: snapshot.to_dict() or {}
            for snapshot in self._collection.select(metadata_fields).stream()
        }
        skipped = 0
        pending_chunks: list[KnowledgeChunk] = []
        for chunk in chunks:
            current = existing.get(chunk.document_id, {})
            if (
                current.get("content_sha256") == chunk.content_sha256
                and current.get("embedding_model") == self.embedder.model
                and current.get("embedding_dimensions") == self.embedder.dimensions
            ):
                skipped += 1
                continue
            pending_chunks.append(chunk)

        written = 0
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for start in range(0, len(pending_chunks), self.batch_size):
                group = pending_chunks[start : start + self.batch_size]
                embeddings = list(
                    executor.map(
                        lambda item: self.embedder.embed_document(
                            item.content,
                            title=item.title,
                        ),
                        group,
                    )
                )
                batch = self._client.batch()
                for chunk, embedding in zip(group, embeddings, strict=True):
                    payload = {
                        "schema_version": 1,
                        "topic_id": chunk.topic_id,
                        "domain_key": chunk.domain_key,
                        "domain_label": chunk.domain_label,
                        "path": list(chunk.path),
                        "title": chunk.title,
                        "anchors": list(chunk.anchors),
                        "content": chunk.content,
                        "content_sha256": chunk.content_sha256,
                        "embedding_model": self.embedder.model,
                        "embedding_dimensions": self.embedder.dimensions,
                        self.vector_field: Vector(embedding),
                        "updated_at": firestore.SERVER_TIMESTAMP,
                    }
                    batch.set(self._collection.document(chunk.document_id), payload)
                batch.commit()
                written += len(group)
                if on_progress:
                    on_progress(skipped + written, len(chunks))
        return IndexingSummary(
            total_chunks=len(chunks),
            skipped_unchanged=skipped,
            embedded_and_written=written,
        )
