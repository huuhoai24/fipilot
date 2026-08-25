# M4 Local / Firestore Parity

Status: **passed**

- Same corpus, query vectors, domain filters, COSINE measure, and Top-K 8 are used on both sides.
- Aggregate parity: `{"first_result_agreement": 1.0, "latency": {"mean_ms": 716.6017949994421, "median_ms": 618.7693499960005, "p95_ms": 987.6643999596126}, "rank_agreement": 1.0, "sample_count": 100, "status": "passed", "top_k_set_overlap": 1.0}`.
- Firestore returns cosine distance; local returns cosine similarity. Ranking comparison uses chunk IDs rather than fabricated equivalent score fields.
- Structured errors are retained in `ERROR_ANALYSIS.md`; there is no lexical fallback.
