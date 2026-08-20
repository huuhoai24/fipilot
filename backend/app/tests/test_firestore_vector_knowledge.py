from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from core.dependencies import build_interview_knowledge_retriever
from core.settings import Settings
from infrastructure.interview_knowledge.firestore_vector import (
    CatalogVectorIndexer,
    FirestoreVectorKnowledgeRetriever,
    VertexTextEmbedder,
)
from services.interview_knowledge.chunks import build_catalog_chunks
from services.interview_knowledge.local import LocalKnowledgeRetriever
from shared.schemas import CandidateProfile, InterviewConfig


class FakeEmbeddingModels:
    def __init__(self, values: list[float]):
        self.values = values
        self.calls: list[dict] = []

    def embed_content(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            embeddings=[SimpleNamespace(values=list(self.values))]
        )


class FakeEmbeddingClient:
    def __init__(self, values: list[float]):
        self.models = FakeEmbeddingModels(values)


class FakeDocument:
    def __init__(self, payload: dict):
        self._payload = payload

    def to_dict(self) -> dict:
        return dict(self._payload)


class FakeVectorQuery:
    def __init__(self, documents: list[FakeDocument]):
        self.documents = documents

    def stream(self):
        return iter(self.documents)


class FakeCollection:
    def __init__(self, documents: list[FakeDocument]):
        self.documents = documents
        self.find_nearest_kwargs: dict | None = None

    def find_nearest(self, **kwargs):
        self.find_nearest_kwargs = kwargs
        return FakeVectorQuery(self.documents)


class FakeFirestoreClient:
    def __init__(self, collection: FakeCollection):
        self.collection_value = collection
        self.collection_name: str | None = None

    def collection(self, name: str) -> FakeCollection:
        self.collection_name = name
        return self.collection_value


class FakeIndexSnapshot(FakeDocument):
    def __init__(self, document_id: str, payload: dict):
        super().__init__(payload)
        self.id = document_id


class FakeDocumentReference:
    def __init__(self, document_id: str):
        self.id = document_id


class FakeIndexCollection:
    def __init__(self, existing: list[FakeIndexSnapshot]):
        self.existing = existing

    def stream(self):
        return iter(self.existing)

    def select(self, fields: list[str]):
        return self

    def document(self, document_id: str):
        return FakeDocumentReference(document_id)


class FakeBatch:
    def __init__(self, writes: list[tuple[str, dict]]):
        self.writes = writes
        self.pending: list[tuple[str, dict]] = []

    def set(self, reference: FakeDocumentReference, payload: dict):
        self.pending.append((reference.id, payload))

    def commit(self):
        self.writes.extend(self.pending)
        self.pending = []


class FakeIndexFirestoreClient:
    def __init__(self, collection: FakeIndexCollection):
        self.collection_value = collection
        self.writes: list[tuple[str, dict]] = []

    def collection(self, name: str):
        return self.collection_value

    def batch(self):
        return FakeBatch(self.writes)


class FakeRecordingEmbedder:
    model = "gemini-embedding-001"
    dimensions = 3

    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def embed_document(self, text: str, *, title: str):
        self.calls.append((text, title))
        return (0.1, 0.2, 0.3)


class FirestoreVectorKnowledgeTests(unittest.TestCase):
    def test_catalog_builds_stable_chunks_from_actual_topic_metadata(self):
        catalog = {
            "version": 1,
            "domains": {
                "Backend_Developer": [
                    {
                        "title": "Authentication",
                        "path": ["Backend", "Security"],
                        "anchors": ["JWT validation", "authorization failures"],
                    }
                ]
            },
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            catalog_path = Path(temp_dir) / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

            first = build_catalog_chunks(catalog_path)
            second = build_catalog_chunks(catalog_path)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 1)
        self.assertEqual(first[0].domain_key, "Backend_Developer")
        self.assertEqual(
            first[0].topic_id,
            "Backend_Developer::Backend::Security::Authentication",
        )
        self.assertIn("JWT validation", first[0].content)
        self.assertEqual(len(first[0].document_id), 32)

    def test_vertex_embedder_uses_asymmetric_retrieval_tasks(self):
        client = FakeEmbeddingClient([0.1, 0.2, 0.3])
        embedder = VertexTextEmbedder(
            project="project-id",
            location="global",
            model="gemini-embedding-001",
            dimensions=3,
            client=client,
        )

        document = embedder.embed_document("document body", title="Authentication")
        query = embedder.embed_query("How should JWT validation work?")

        self.assertEqual(document, (0.1, 0.2, 0.3))
        self.assertEqual(query, (0.1, 0.2, 0.3))
        document_config = client.models.calls[0]["config"]
        query_config = client.models.calls[1]["config"]
        self.assertEqual(document_config.task_type, "RETRIEVAL_DOCUMENT")
        self.assertEqual(document_config.title, "Authentication")
        self.assertEqual(query_config.task_type, "RETRIEVAL_QUERY")
        self.assertIsNone(query_config.title)
        self.assertEqual(document_config.output_dimensionality, 3)

    def test_retriever_runs_cosine_knn_and_returns_planner_context(self):
        collection = FakeCollection(
            [
                FakeDocument(
                    {
                        "domain_label": "Backend Developer",
                        "path": ["Backend", "Security"],
                        "title": "Authentication",
                        "anchors": ["JWT validation", "authorization failures"],
                        "vector_distance": 0.08,
                    }
                )
            ]
        )
        firestore_client = FakeFirestoreClient(collection)
        embedding_client = FakeEmbeddingClient([0.1, 0.2, 0.3])
        embedder = VertexTextEmbedder(
            project="project-id",
            location="global",
            model="gemini-embedding-001",
            dimensions=3,
            client=embedding_client,
        )
        retriever = FirestoreVectorKnowledgeRetriever(
            firestore_client=firestore_client,
            embedder=embedder,
            collection_name="interview_knowledge_chunks",
            vector_field="embedding",
            top_k=5,
        )

        results = retriever.retrieve_topics(
            CandidateProfile(
                name="Private Candidate Name",
                recent_role="Backend Developer",
                skills=["FastAPI", "JWT"],
            ),
            InterviewConfig(
                experience_level="junior",
                objective="Practice authentication design",
            ),
        )

        self.assertEqual(firestore_client.collection_name, "interview_knowledge_chunks")
        self.assertEqual(collection.find_nearest_kwargs["vector_field"], "embedding")
        self.assertEqual(collection.find_nearest_kwargs["limit"], 5)
        self.assertEqual(
            collection.find_nearest_kwargs["distance_measure"].name,
            "COSINE",
        )
        self.assertEqual(
            collection.find_nearest_kwargs["distance_result_field"],
            "vector_distance",
        )
        query_text = embedding_client.models.calls[0]["contents"]
        self.assertIn("Backend Developer", query_text)
        self.assertIn("FastAPI", query_text)
        self.assertNotIn("Private Candidate Name", query_text)
        self.assertIn("Authentication", results[0])
        self.assertIn("JWT validation", results[0])

    def test_factory_keeps_local_default_and_builds_vector_adapter_opt_in(self):
        local = build_interview_knowledge_retriever(Settings())
        self.assertIsInstance(local, LocalKnowledgeRetriever)

        collection = FakeCollection([])
        firestore_client = FakeFirestoreClient(collection)
        embedding_client = FakeEmbeddingClient([0.1, 0.2, 0.3])
        settings = Settings(
            google_cloud_project="project-id",
            interview_knowledge_backend="firestore_vector",
            interview_knowledge_embedding_dimensions=3,
        )

        vector = build_interview_knowledge_retriever(
            settings,
            firestore_client=firestore_client,
            embedding_client=embedding_client,
        )

        self.assertIsInstance(vector, FirestoreVectorKnowledgeRetriever)

    def test_indexer_is_idempotent_for_unchanged_catalog_chunks(self):
        catalog = {
            "domains": {
                "Backend_Developer": [
                    {
                        "title": "Authentication",
                        "path": ["Security"],
                        "anchors": ["JWT validation"],
                    },
                    {
                        "title": "Authorization",
                        "path": ["Security"],
                        "anchors": ["role checks"],
                    },
                ]
            }
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "catalog.json"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            chunks = build_catalog_chunks(path)

        existing = FakeIndexSnapshot(
            chunks[0].document_id,
            {
                "content_sha256": chunks[0].content_sha256,
                "embedding_model": "gemini-embedding-001",
                "embedding_dimensions": 3,
            },
        )
        client = FakeIndexFirestoreClient(FakeIndexCollection([existing]))
        embedder = FakeRecordingEmbedder()
        indexer = CatalogVectorIndexer(
            firestore_client=client,
            embedder=embedder,
            collection_name="interview_knowledge_chunks",
            vector_field="embedding",
            batch_size=100,
        )

        summary = indexer.sync(chunks)

        self.assertEqual(summary.total_chunks, 2)
        self.assertEqual(summary.skipped_unchanged, 1)
        self.assertEqual(summary.embedded_and_written, 1)
        self.assertEqual(len(embedder.calls), 1)
        self.assertEqual(len(client.writes), 1)
        written = client.writes[0][1]
        self.assertEqual(written["topic_id"], chunks[1].topic_id)
        self.assertEqual(tuple(written["embedding"]), (0.1, 0.2, 0.3))


if __name__ == "__main__":
    unittest.main()
