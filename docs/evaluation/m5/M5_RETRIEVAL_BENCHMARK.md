# M5 Retrieval Benchmark

Status: **CLOSED**

Corpus identity: `passed`. The hash discrepancy is a reporting typo; all 4,492 vector records match the current M3 artifacts by ID, content/input hash, cache key, version, and dimension.

Dataset: 50 M1 compatibility, 50 preserved M4 stress, 72 frozen development, and 48 frozen holdout cases. HUMAN LABELLED = NO; Human validation = NOT EVALUATED.

Predefined tuning objective: lexicographic: Recall@5, MRR@8, Precision@5, shallower depth, no diversification, balanced weights, domain filter.

## Frozen holdout quality

| Metric | Lexical | Vector | Hybrid |
|---|---:|---:|---:|
| Hit@1 | 0.6458 | 0.9167 | 0.9375 |
| Hit@5 | 0.6667 | 1.0000 | 1.0000 |
| Recall@5 | 0.6667 | 1.0000 | 1.0000 |
| Precision@5 | 0.1417 | 0.2083 | 0.2083 |
| MRR@8 | 0.6562 | 0.9531 | 0.9688 |

Recommendation: **INSUFFICIENT_EVIDENCE**. Production activation ready: **NO**.

## Frozen configurations

```json
{
  "configuration_hash": "395ed7e1259a77175148417e3071c2447a46e4067732a547238fde6403b7915b",
  "development_hash": "8aabbeabeff57b24307f05f667198f0f0faca5775bb5b3b9cf777341734b465e",
  "holdout_hash": "cf377de0b24772881112a70e3533abae65536dab0de6c052535b4b51730f1ae8",
  "hybrid": {
    "candidate_depth": 8,
    "development_hash": "8aabbeabeff57b24307f05f667198f0f0faca5775bb5b3b9cf777341734b465e",
    "diversify_by_content_hash": false,
    "filter_strategy": "domain_level",
    "holdout_hash": "cf377de0b24772881112a70e3533abae65536dab0de6c052535b4b51730f1ae8",
    "lexical_weight": 0.75,
    "output_k": 8,
    "rrf_k": 60,
    "vector_weight": 1.0
  },
  "lexical": {
    "candidate_depth": 20,
    "implementation": "production weighted lexical overlap + domain selection + exact-title bonus",
    "output_k": 8,
    "production_top_k_unchanged": 8
  },
  "objective_defined_before_tuning": "lexicographic: Recall@5, MRR@8, Precision@5, shallower depth, no diversification, balanced weights, domain filter",
  "schema_version": "m5.freeze.v1",
  "vector": {
    "candidate_depth": 20,
    "diversify_by_content_hash": false,
    "filter_strategy": "domain_level",
    "lexical_weight": 0.0,
    "rrf_k": 0,
    "vector_weight": 1.0
  }
}
```

## Development selection

| System | Hit@5 | Recall@5 | Precision@5 | MRR@8 |
|---|---:|---:|---:|---:|
| Lexical | 0.6667 | 0.6528 | 0.1389 | 0.6181 |
| Vector selected | 0.9722 | 0.9583 | 0.2000 | 0.9357 |
| Hybrid selected | 1.0000 | 0.9861 | 0.2056 | 0.9630 |

## Category, domain, and paired evidence

| Slice | System | N | Hit@5 | Recall@5 | MRR@8 |
|---|---|---:|---:|---:|---:|
| exact_terminology | lexical | 3 | 1.0000 | 1.0000 | 1.0000 |
| exact_terminology | vector | 3 | 1.0000 | 1.0000 | 0.8333 |
| exact_terminology | hybrid | 3 | 1.0000 | 1.0000 | 0.8333 |
| semantic_paraphrase | lexical | 11 | 1.0000 | 1.0000 | 1.0000 |
| semantic_paraphrase | vector | 11 | 1.0000 | 1.0000 | 0.9545 |
| semantic_paraphrase | hybrid | 11 | 1.0000 | 1.0000 | 1.0000 |
| vietnamese | lexical | 2 | 1.0000 | 1.0000 | 1.0000 |
| vietnamese | vector | 2 | 1.0000 | 1.0000 | 0.7500 |
| vietnamese | hybrid | 2 | 1.0000 | 1.0000 | 1.0000 |
| role_skill_seniority | lexical | 18 | 0.1111 | 0.1111 | 0.1111 |
| role_skill_seniority | vector | 18 | 1.0000 | 1.0000 | 0.9583 |
| role_skill_seniority | hybrid | 18 | 1.0000 | 1.0000 | 0.9722 |
| multi_concept | lexical | 2 | 1.0000 | 1.0000 | 1.0000 |
| multi_concept | vector | 2 | 1.0000 | 1.0000 | 1.0000 |
| multi_concept | hybrid | 2 | 1.0000 | 1.0000 | 1.0000 |
| low_overlap | lexical | 2 | 1.0000 | 1.0000 | 1.0000 |
| low_overlap | vector | 2 | 1.0000 | 1.0000 | 1.0000 |
| low_overlap | hybrid | 2 | 1.0000 | 1.0000 | 1.0000 |
| high_overlap | lexical | 2 | 1.0000 | 1.0000 | 1.0000 |
| high_overlap | vector | 2 | 1.0000 | 1.0000 | 1.0000 |
| high_overlap | hybrid | 2 | 1.0000 | 1.0000 | 1.0000 |

| Domain | N | Hybrid Hit@5 | Hybrid Recall@5 | Hybrid MRR@8 |
|---|---:|---:|---:|---:|
| AI_Engineer | 4 | 1.0000 | 1.0000 | 1.0000 |
| Backend_Developer | 4 | 1.0000 | 1.0000 | 1.0000 |
| Business_Analyst | 5 | 1.0000 | 1.0000 | 0.9000 |
| Data_Engineer | 5 | 1.0000 | 1.0000 | 1.0000 |
| Data_Scientist | 5 | 1.0000 | 1.0000 | 1.0000 |
| DevOps_Engineer | 5 | 1.0000 | 1.0000 | 1.0000 |
| Full_Stack_Developer | 5 | 1.0000 | 1.0000 | 1.0000 |
| Software_Engineer | 5 | 1.0000 | 1.0000 | 1.0000 |
| Tester_QA_QC | 5 | 1.0000 | 1.0000 | 0.8000 |
| Web_Developer | 5 | 1.0000 | 1.0000 | 1.0000 |

Paired Hit@5 outcomes: `{"lexical_vs_hybrid_at_5": {"both_hit": 32, "both_miss": 0, "left_hit_right_miss": 0, "left_miss_right_hit": 16}, "lexical_vs_vector_at_5": {"both_hit": 32, "both_miss": 0, "left_hit_right_miss": 0, "left_miss_right_hit": 16}, "vector_vs_hybrid_at_5": {"both_hit": 48, "both_miss": 0, "left_hit_right_miss": 0, "left_miss_right_hit": 0}}`.

| Dataset | System | Hit@1 | Hit@5 | Recall@5 | MRR@8 |
|---|---|---:|---:|---:|---:|
| m1_compatibility | lexical | 0.8400 | 1.0000 | 1.0000 | 0.9117 |
| m1_compatibility | vector | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| m1_compatibility | hybrid | 0.0000 | 1.0000 | 1.0000 | 0.4690 |
| m4_paraphrase_stress | lexical | 0.1200 | 0.4600 | 0.4400 | 0.2607 |
| m4_paraphrase_stress | vector | 0.6800 | 0.9800 | 0.9567 | 0.8087 |
| m4_paraphrase_stress | hybrid | 0.6200 | 0.9600 | 0.9400 | 0.7537 |

## Filters and duplicates

The development grid compared no filter, domain, and strict domain+level, with and without content-hash diversification. Strict domain+level won the new development objective, while diversification was disabled because it produced no quality gain. Holdout duplicate-result rate@5 was `0.0083` and unique-content rate@5 was `0.9917`.

Compatibility evidence also exposes a safety issue: strict level filtering excludes foundational `level=unspecified` chunks on M1. This materially lowers exact-term ranking, so the frozen quality winner is not activation-ready.

## Cost and operations

Vertex calls/tokens/estimated cost: `43` / `10119` / `$0.001518`. Firestore returned-document/read estimate: `1488`; writes: `0`.

## Council answers

- Vector DB stores M3 knowledge embeddings plus chunk/topic IDs, content/provenance, filters, hashes, corpus and embedding versions; it contains no candidate PII.
- Embedded documents use deterministic M4 `m4.v1` context-enriched text. Queries use deterministic role/domain/level/topic/objective/query fields with no generative expansion.
- Each `RETRIEVAL_QUERY` vector is compared with 768D `RETRIEVAL_DOCUMENT` vectors using Firestore COSINE distance.
- Hybrid is the frozen-holdout quality winner, raising Hit@5/Recall@5 from `0.6667/0.6667` to `1.0000/1.0000`. The architectural recommendation remains `INSUFFICIENT_EVIDENCE` because its gain over Vector is small, preserved-stress MRR is lower, and strict level filtering fails compatibility ranking.

Vector search compares `RETRIEVAL_QUERY` 768D `gemini-embedding-001` vectors against M4 `RETRIEVAL_DOCUMENT` vectors using Firestore COSINE distance. Hybrid uses deterministic RRF rather than mixing lexical and cosine scores.

Latency is separated in `LATENCY_REPORT.md`; cold behavior is retained. Production remains weighted lexical Top-K 8.

## Limitations

- All labels are synthetic-controlled and source-derived; none are human-reviewed production judgments.
- HOLDOUT has 48 cases. Exact/high-overlap, Vietnamese, low-overlap, and multi-concept slices contain only 2–3 cases each, so category conclusions are directional.
- Forty frozen cases deliberately cover M3 level guidance/evaluation knowledge. This exposes a real lexical coverage gap but also makes the new benchmark unlike the catalog-backed M1 distribution.
- Strict level filtering wins the new frozen benchmark but fails M1 compatibility ranking when useful foundational chunks are marked `level=unspecified`; it must be redesigned and rebenchmarked before activation.
- Firestore operation counts are returned-document/read estimates, not an invoice. The per-1,000-query estimate excludes Firestore charges.
- Hybrid is only the frozen-holdout quality winner; the architectural recommendation is `INSUFFICIENT_EVIDENCE`, and no Planner activation is approved.
