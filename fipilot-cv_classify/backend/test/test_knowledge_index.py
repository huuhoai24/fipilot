import tempfile
import unittest
import os
from pathlib import Path
from unittest.mock import patch

from fipilot.knowledge_index import _documents, resolve_domain_folder, search_domain


class KnowledgeIndexTest(unittest.TestCase):
    def test_pgvector_is_used_when_configured(self):
        expected = [{
            "source": "Domains/Backend Developer/Transactions.md",
            "path": "Domains/Backend Developer/Transactions.md",
            "content": "Transaction isolation and rollback.",
            "score": 0.9,
            "method": "pgvector-hybrid",
        }]

        with (
            patch.dict(os.environ, {"KNOWLEDGE_RETRIEVAL_BACKEND": "pgvector"}),
            patch("fipilot.vector_store.search_pgvector", return_value=expected),
        ):
            hits = search_domain("transaction failure recovery", "Backend Developer", top_k=1)

        self.assertEqual(hits, expected)

    def test_pgvector_failure_falls_back_to_packaged_knowledge(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            domain.mkdir(parents=True)
            (domain / "Transactions.md").write_text(
                "# Transactions\nUse transaction boundaries and rollback.",
                encoding="utf-8",
            )
            _documents.cache_clear()
            with (
                patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root),
                patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing"),
                patch.dict(os.environ, {"KNOWLEDGE_RETRIEVAL_BACKEND": "pgvector"}),
                patch("fipilot.vector_store.search_pgvector", side_effect=RuntimeError("offline")),
            ):
                hits = search_domain("transaction rollback", "Backend Developer", top_k=1)

        self.assertEqual(hits[0]["method"], "lexical")
        self.assertTrue(hits[0]["source"].endswith("Transactions.md"))

    def test_all_canonical_roles_resolve_to_their_knowledge_folders(self):
        expected = {
            "AI Engineer": "AI_Enginner",
            "Backend Developer": "Backend Developer",
            "Business Analyst": "Business Analyst",
            "Data Engineer": "Data Engineer",
            "Data Scientist": "Data Scientist",
            "DevOps Engineer": "DevOps Engineer",
            "Full Stack Developer": "Full stack Developer",
            "Software Engineer": "Software Engineer",
            "Tester QA QC": "Tester_QA_QC",
            "Web Developer": "Web Developer",
        }

        self.assertEqual(
            {role: resolve_domain_folder(role).name for role in expected},
            expected,
        )

    def test_lexical_rag_returns_bounded_grounded_chunks_without_a_vector_index(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            (domain / "Database").mkdir(parents=True)
            (domain / "Web").mkdir(parents=True)
            (domain / "Database" / "PostgreSQL.md").write_text(
                "# PostgreSQL transactions\nUse transaction boundaries, rollback, indexes, and isolation levels.",
                encoding="utf-8",
            )
            (domain / "Web" / "CSS.md").write_text(
                "# CSS layout\nUse Grid and Flexbox for responsive pages.",
                encoding="utf-8",
            )

            with (
                patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root),
                patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing-index"),
            ):
                hits = search_domain(
                    "Built FastAPI endpoints with PostgreSQL transactions and rollback",
                    "Backend Developer",
                    top_k=2,
                )

        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["method"], "lexical")
        self.assertTrue(hits[0]["source"].endswith("PostgreSQL.md"))
        self.assertIn("transaction boundaries", hits[0]["content"])
        self.assertLessEqual(len(hits[0]["content"]), 1800)
        self.assertGreater(hits[0]["score"], 0)

    def test_lexical_rag_prefers_specific_resume_terms_over_common_api_terms(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            domain.mkdir(parents=True)
            (domain / "Error Documentation.md").write_text(
                "# API error handling\nDocument API error responses and API error codes clearly.",
                encoding="utf-8",
            )
            (domain / "Rollback Strategy.md").write_text(
                "# Transaction rollback\nUse PostgreSQL transaction boundaries and rollback safely.",
                encoding="utf-8",
            )
            (domain / "API Basics.md").write_text(
                "# API basics\nAn API handler receives requests and returns responses.",
                encoding="utf-8",
            )

            with (
                patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root),
                patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing-index"),
            ):
                hits = search_domain(
                    "Built FastAPI API error handling with PostgreSQL transaction rollback",
                    "Backend Developer",
                    top_k=2,
                )

        self.assertTrue(hits[0]["source"].endswith("Rollback Strategy.md"))

    def test_rag_reg_semantic_morphology_retrieves_relevant_chunk_amid_noise(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            domain.mkdir(parents=True)
            (domain / "Scale.md").write_text(
                "Reduced API response time with Redis caching and horizontal scaling.",
                encoding="utf-8",
            )
            (domain / "CSS.md").write_text(
                "Responsive grid layouts, typography, and button colors.",
                encoding="utf-8",
            )
            (domain / "Hiring.md").write_text(
                "Interview scheduling and candidate communication guidance.",
                encoding="utf-8",
            )

            _documents.cache_clear()
            with (
                patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root),
                patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing-index"),
                patch.dict(os.environ, {"KNOWLEDGE_RETRIEVAL_BACKEND": "local"}),
            ):
                hits = search_domain(
                    "How did the candidate improve system scalability?",
                    "Backend Developer",
                    top_k=2,
                )

        self.assertTrue(hits)
        self.assertTrue(hits[0]["source"].endswith("Scale.md"))

    def test_rag_reg_no_matching_evidence_returns_empty_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            domain.mkdir(parents=True)
            (domain / "CSS.md").write_text(
                "Responsive typography and accessible color contrast.",
                encoding="utf-8",
            )

            _documents.cache_clear()
            with (
                patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root),
                patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing-index"),
                patch.dict(os.environ, {"KNOWLEDGE_RETRIEVAL_BACKEND": "local"}),
            ):
                hits = search_domain(
                    "PostgreSQL transaction rollback isolation",
                    "Backend Developer",
                    top_k=3,
                )

        self.assertEqual(hits, [])

    def test_rag_reg_duplicate_content_does_not_occupy_multiple_top_k_slots(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "Knowledge"
            domain = root / "Domains" / "Backend Developer"
            domain.mkdir(parents=True)
            duplicate = "Redis cache invalidation ownership and stale-data recovery."
            (domain / "Cache A.md").write_text(duplicate, encoding="utf-8")
            (domain / "Cache B.md").write_text(duplicate, encoding="utf-8")
            (domain / "Cache Failure.md").write_text(
                "Cache invalidation failure handling uses metrics and rollback.",
                encoding="utf-8",
            )

            _documents.cache_clear()
            with (
                patch("fipilot.knowledge_index.KNOWLEDGE_DIR", root),
                patch("fipilot.knowledge_index.INDEX_DIR", Path(directory) / "missing-index"),
                patch.dict(os.environ, {"KNOWLEDGE_RETRIEVAL_BACKEND": "local"}),
            ):
                hits = search_domain(
                    "cache invalidation failure recovery",
                    "Backend Developer",
                    top_k=3,
                )

        normalized_contents = {" ".join(hit["content"].casefold().split()) for hit in hits}
        self.assertEqual(len(hits), len(normalized_contents))
        self.assertTrue(any(hit["source"].endswith("Cache Failure.md") for hit in hits))


if __name__ == "__main__":
    unittest.main()
