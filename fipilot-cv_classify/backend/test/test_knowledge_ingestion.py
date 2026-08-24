import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fipilot.knowledge_ingestion import ingest_role
from fipilot.knowledge_index import _documents


class _Store:
    def __init__(self):
        self.call = None

    def replace_role(self, *, role_id, role_title, chunks):
        self.call = {
            "role_id": role_id,
            "role_title": role_title,
            "chunks": chunks,
        }


class KnowledgeIngestionTest(unittest.TestCase):
    def test_ingest_role_embeds_and_atomically_replaces_role_chunks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            domain.mkdir(parents=True)
            (domain / "Transactions.md").write_text(
                "# Transactions\nUse commit and rollback boundaries.",
                encoding="utf-8",
            )
            store = _Store()
            embedded_inputs = []

            def embedder(texts):
                embedded_inputs.extend(texts)
                return [[0.001] * 1536 for _ in texts]

            _documents.cache_clear()
            with patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root):
                summary = ingest_role(
                    "Backend Developer",
                    store=store,
                    embedder=embedder,
                )

        self.assertEqual(summary["role_id"], "backend-developer")
        self.assertEqual(summary["chunks"], 1)
        self.assertEqual(store.call["role_title"], "Backend Developer")
        [chunk] = store.call["chunks"]
        self.assertTrue(chunk["source"].endswith("Transactions.md"))
        self.assertEqual(len(chunk["content_hash"]), 64)
        self.assertEqual(len(chunk["embedding"]), 1536)
        self.assertIn("Backend Developer", embedded_inputs[0])


if __name__ == "__main__":
    unittest.main()
