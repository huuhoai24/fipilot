# M4 Embedding & Vector Retrieval Shadow Index

Status: **CLOSED**

## Isolation

M4 consumes immutable M3 artifacts and writes only to `fipilot_m4_knowledge_vectors`. Production continues to use weighted lexical retrieval with Top-K 8. M4 is not imported by the Planner or production dependency graph.

## What is embedded

Primary document representation `m4.v1`:

```text
Domain: <M3 domain>
Level: <M3 level>
Topic: <M3 topic>
Subtopic: <M3 subtopic when present>
Section: <M3 heading path>
Type: <M3 content type>

<unaltered M3 content>
```

The provider title parameter is disabled because the SDK exposes one title at batch-config level; using it for mixed-title batches would be incorrect. Existing title/heading values remain in `embedding_text` and record metadata.

## Embedding configuration

- Provider/model/location: Vertex AI / `gemini-embedding-001` / `global`.
- Explicit dimension: `768` (provider default verified as 3,072, never assumed).
- Documents: `RETRIEVAL_DOCUMENT`; queries: `RETRIEVAL_QUERY`; `SEMANTIC_SIMILARITY` is not used.
- Provider limits enforced: 250 inputs/request, 20,000 tokens/request, 2,048 tokens/input, `auto_truncate=false`.
- Successful primary vectors: `4492/4492`; invalid `0`.

## Which vectors are compared

Each deterministic `RETRIEVAL_QUERY` vector is compared with the filtered set of M3 chunk `RETRIEVAL_DOCUMENT` vectors. The local oracle computes cosine similarity `q·d / (||q|| ||d||)`. Firestore uses `COSINE` distance and reports distance; M4 displays `1 - distance` as cosine similarity.

## Vector database contents

Each document retains the 768D vector, chunk/topic IDs, canonical content and embedding text, domain, level, topic, subtopic, content type, full source provenance, content/input hashes, corpus/schema/embedding versions, model, task type, dimension, and cache key. No candidate data or PII is stored.

## Retrieval results

- M1 controlled vector: Hit@1/3/5/8 `0.8000 / 1.0000 / 1.0000 / 1.0000`; Recall@1/3/5/8 `0.7000 / 1.0000 / 1.0000 / 1.0000`; Precision@5/8 `0.2400 / 0.1500`; MRR@8 `0.8967`.
- Stress lexical: Hit@1/3/5/8 `0.1000 / 0.3600 / 0.4400 / 0.5400`; Recall@1/3/5/8 `0.0900 / 0.3300 / 0.4200 / 0.5200`; Precision@5/8 `0.0960 / 0.0725`; MRR@8 `0.2467`.
- Stress vector: Hit@1/3/5/8 `0.6800 / 0.9200 / 0.9800 / 1.0000`; Recall@1/3/5/8 `0.6150 / 0.9000 / 0.9567 / 0.9817`; Precision@5/8 `0.2240 / 0.1450`; MRR@8 `0.8087`.

These are preliminary shadow metrics. M1 is catalog-backed; the stress set is synthetic controlled. Neither selects the production retriever.

## Tiny chunks and duplicates

- Tiny-chunk query subset: `5` cases.
- Duplicate effect@5: `{"duplicate_result_rate": 0.008, "unique_content_rate": 0.992, "unique_topic_rate": 0.968}`.
- Exact duplicates remain indexed; M4 measures ranking concentration and does not remove or diversify them.

## Incremental behavior

Cache keys include input hash, model, dimension, task, provider/location, title policy, representation version, and embedding version. Unchanged inputs reuse cached vectors; additions/modifications embed; deletions perform index deletes without embedding. Simulation: `passed`.

## Firestore

- Collection: `fipilot_m4_knowledge_vectors`; vector field `embedding`; 768D flat COSINE indexes.
- Sync: `{"added": 0, "deleted": 0, "deletes": 0, "existing_records": 4492, "expected_records": 4492, "modified": 0, "reads": 4492, "unchanged": 4492, "writes": 0}`.
- Integrity: `{"duplicate_vector_records": 0, "expected_chunks": 4492, "invalid_vectors": 0, "missing_chunk_ids": [], "missing_vectors": 0, "reads": 4492, "stale_chunk_ids": [], "stale_vectors": 0, "status": "passed", "stored_vectors": 4492, "wrong_corpus_version": 0, "wrong_dimension": 0}`.
- Domain/level metadata filters: `{"domain": {"result_count": 8, "status": "passed"}, "level": {"result_count": 8, "status": "passed"}}`.
- Index evidence: `{"collection": "fipilot_m4_knowledge_vectors", "database": "(default)", "indexes": [{"fields": ["domain ASC", "__name__ ASC", "embedding FLAT VECTOR<768>"], "id": "CICAgJim14AK", "state": "READY"}, {"fields": ["level ASC", "__name__ ASC", "embedding FLAT VECTOR<768>"], "id": "CICAgJjF9oIK", "state": "READY"}, {"fields": ["__name__ ASC", "embedding FLAT VECTOR<768>"], "id": "CICAgJiUpoMK", "state": "READY"}], "project": "project-7dffc340-f73f-4e62-aec", "retrieved_at": "2026-08-19T00:28:37.0001437Z", "status": "READY"}`.
- Local/Firestore parity: `{"first_result_agreement": 1.0, "latency": {"mean_ms": 716.6017949994421, "median_ms": 618.7693499960005, "p95_ms": 987.6643999596126}, "rank_agreement": 1.0, "sample_count": 100, "status": "passed", "top_k_set_overlap": 1.0}`.
- Live end-to-end smoke: `{"embedding_latency_ms": 19333.666799997445, "end_to_end_latency_ms": 19982.340299990028, "firestore_search_latency_ms": 648.670399968978, "latency": {"mean_ms": 19982.340299990028, "median_ms": 19982.340299990028, "p95_ms": 19982.340299990028}, "result_count": 8, "sample_count": 1, "status": "passed"}`.

## Cost and storage

- Vertex provider requests: `86`; cache hits: `19028`.
- Estimated Vertex cost: `$0.062286`; known invoiced cost: `None`.
- Firestore reads/writes/deletes: `38400 / 4492 / 0`.
- Raw vector payload and Firestore storage values are estimates, not billed storage.

## Latency

- Offline context-enriched document batches: `{"mean_ms": 3438.074486662582, "median_ms": 3098.204900044948, "p95_ms": 3622.1768999821506}`.
- Online query embedding batch: `{"mean_ms": 2412.8860000055283, "median_ms": 2412.8860000055283, "p95_ms": 2412.8860000055283}`.
- Local M1 search: `{"mean_ms": 1.7205380008090287, "median_ms": 1.7340999911539257, "p95_ms": 2.1800000104121864}`.
- Firestore search across parity cases: `{"mean_ms": 716.6017949994421, "median_ms": 618.7693499960005, "p95_ms": 987.6643999596126}`.
- Live end-to-end sample: `{"embedding_latency_ms": 19333.666799997445, "end_to_end_latency_ms": 19982.340299990028, "firestore_search_latency_ms": 648.670399968978, "latency": {"mean_ms": 19982.340299990028, "median_ms": 19982.340299990028, "p95_ms": 19982.340299990028}, "result_count": 8, "sample_count": 1, "status": "passed"}`. This has one sample, so mean, median, and P95 are identical and must not be generalized.

## Limitations

- Embedding billing metadata exposes token/character usage but not the final invoice; exact cost remains null.
- Stress labels are manually controlled against M3 IDs, not human production judgments.
- Near-semantic relevance outside the labelled target is not exhaustively judged.
- M5 must perform the formal lexical/vector/hybrid decision.
