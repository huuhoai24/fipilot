import unittest

from fipilot.vector_store import PgVectorKnowledgeStore


class _Mappings:
    def __init__(self, rows):
        self.rows = rows

    def all(self):
        return self.rows


class _Result:
    def __init__(self, rows):
        self.rows = rows

    def mappings(self):
        return _Mappings(self.rows)


class _Connection:
    def __init__(self, result_sets):
        self.result_sets = iter(result_sets)
        self.parameters = []

    def execute(self, _statement, _parameters):
        self.parameters.append(_parameters)
        return _Result(next(self.result_sets))

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None


class _Engine:
    def __init__(self, result_sets):
        self.connection = _Connection(result_sets)

    def connect(self):
        return self.connection


class PgVectorKnowledgeStoreTest(unittest.TestCase):
    def test_search_fuses_semantic_and_lexical_rankings(self):
        vector_rows = [
            {
                "source": "Domains/Backend Developer/Transactions.md",
                "content": "Use transaction boundaries and rollback.",
                "score": 0.91,
            },
            {
                "source": "Domains/Backend Developer/Caching.md",
                "content": "Cache invalidation requires an ownership strategy.",
                "score": 0.84,
            },
        ]
        lexical_rows = [
            {
                "source": "Domains/Backend Developer/Caching.md",
                "content": "Cache invalidation requires an ownership strategy.",
                "score": 0.32,
            },
            {
                "source": "Domains/Backend Developer/Errors.md",
                "content": "Document stable API error codes.",
                "score": 0.21,
            },
        ]
        store = PgVectorKnowledgeStore(engine=_Engine([vector_rows, lexical_rows]))

        hits = store.search(
            role_id="backend-developer",
            query="Redis cache consistency and rollback",
            query_embedding=[0.001] * 1536,
            top_k=3,
        )

        self.assertEqual(hits[0]["source"], "Domains/Backend Developer/Caching.md")
        self.assertEqual(hits[0]["method"], "pgvector-hybrid")
        self.assertEqual({hit["source"] for hit in hits}, {
            "Domains/Backend Developer/Transactions.md",
            "Domains/Backend Developer/Caching.md",
            "Domains/Backend Developer/Errors.md",
        })
        lexical_parameters = store.engine.connection.parameters[1]
        self.assertEqual(
            lexical_parameters["lexical_query"],
            "redis OR cache OR consistency OR rollback",
        )


if __name__ == "__main__":
    unittest.main()
