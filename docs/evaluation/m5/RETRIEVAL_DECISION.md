# M5 Retrieval Decision

Architectural recommendation: **INSUFFICIENT_EVIDENCE**

Production activation ready: **NO**

Decision rule: A more complex retriever requires >=0.05 absolute Recall@5 or MRR@8 gain, no material exact-term loss, and best Recall@5.

Measured hybrid gain: `0.3333`; measured vector gain: `0.3333`. Operational activation remains deferred because labels are synthetic-controlled and no Planner wiring or human validation is authorized in M5. Future vector failure policy is lexical-only, but it is not active and benchmark runs never fallback.

## Evidence matrix

| Criterion | Lexical | Vector | Hybrid |
|---|---|---|---|
| Frozen holdout quality | Hit@5 `0.6667`, MRR `0.6562` | Hit@5 `1.0000`, MRR `0.9531` | Hit@5 `1.0000`, MRR `0.9688` |
| Preserved stress MRR | `0.2607` | `0.8087` | `0.7537` |
| M1 compatibility MRR | `0.9117` | `0.0000` under unsafe strict level filter | `0.4690` under unsafe strict level filter |
| Online P95 | `8.55 ms` | `1591.87 ms` | parallel `1556.28 ms` |
| Vertex dependency/cost | None | Required; estimated `$0.009070`/1,000, Firestore excluded | Same plus lexical execution |
| Operational complexity | Lowest | Vertex + Firestore + indexes/cache | Highest: both retrievers, bounded concurrency, deterministic RRF |
| Determinism | Fully local | Deterministic ranking for fixed embeddings; remote query embedding dependency | Deterministic fusion for fixed input rankings |
| Failure mode | Local failure only | Explicit vector error during benchmark | Future recommendation: vector unavailable → lexical-only; not active in M5 |

Future output-K recommendation remains `8`. Frozen holdout saturates at K=5, but the preserved stress set still recovers additional cases by K=8; M5 does not change production Top-K.
