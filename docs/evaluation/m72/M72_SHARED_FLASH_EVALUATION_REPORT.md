# M7.2 Ultra-Low-Cost Shared Flash Evaluator

## Decision

**M7.2 STATUS = PARTIAL**  
**PRODUCTION_ACTIVATION_READY = NO**  
**PRODUCTION SCORE TRUST = LOW**

The one allowed shared-Flash candidate failed Stage 1 because semantic unsupported feedback was 25% (2/8), above the frozen Stage 1 ceiling of 12.5% and final target of 5%. Per protocol, paid execution stopped. Stage 2 DEVELOPMENT, freeze, HOLDOUT, repeatability, latency follow-up, model search, and activation were not run.

## New M7.2 cost

| Item | Result |
| --- | ---: |
| Shared Flash evaluator calls | 8 |
| Evaluator cache hits | 0 |
| Feedback semantic bundles | 8 |
| Feedback cache hits | 0 |
| Static reference calls | 0 |
| Flash provider estimate | $0.003239 |
| Semantic-judge conservative envelope | $0.032000 |
| **NEW M7.2 conservative estimate** | **$0.035239** |
| Default / hard budget | $0.50 / $1.00 |

Exact RAGAS provider token usage and invoice cost are unavailable. M7 and M7.1 historical costs are kept separate from incremental M7.2 cost.

## Shared Flash configuration

- Model: `gemini-2.5-flash` only.
- Task type: `simple`; temperature `0.1`; thinking budget `0`.
- Prompt: `answer-evaluator.shared-flash.v1`.
- Rubric: unchanged `answer-rubric.anchored.v1` score anchors.
- Feedback: `evidence-constrained-feedback.v1`.
- Candidate config hash: `1e9e99f3fa8e9c7a37cf9933b13be025598e63eb150716daf2a57ea25b4339bf`.
- Prompt hash: `d393a082da462e2d59ae719b433740ec178170df92855358c92cd05b7ea2aed7`.
- Schema/parser: evaluation-only `M72AnswerEvaluation`; Vertex `generate_json` plus Pydantic.
- Identical textual question, answer, and context use one semantic evaluator result projected to Text and Voice.

A2 Voice evaluator outputs were not reused because the evidence-constrained feedback prompt changed the evaluator cache identity. Static M7 references were reused without calls.

## Stage 0

Stage 0 passed with zero paid calls. Schema/prompt, one-call projection, cache behavior, smoke selection, deterministic filters, budget blocking, M7 reference integrity, and production isolation were validated.

## Stage 1

The frozen eight-answer set contained two critical/WEAK, two PARTIAL controls, two GOOD, and two STRONG answers. The frozen M7 DEVELOPMENT data has no non-critical construction-WEAK answer: every WEAK fixture carries a critical-error label. Therefore a non-overlapping interpretation of “two critical plus two weak” was impossible without duplicating that property; two PARTIAL controls were used and this deviation is explicit. Five items were chosen from A2 Voice unsupported-feedback cases to stress the root blocker.

| Metric | Result | Stage 1 gate |
| --- | ---: | ---: |
| Critical detection | 100% | 100% — PASS |
| Dangerous overscore | 0% | 0% — PASS |
| Schema failures | 0 | 0 — PASS |
| MAE | .839 | No major regression — PASS |
| Mean score delta from A2 Voice | .563 | ≤1.0 — PASS |
| Maximum reference tier distance | 1 | ≤1 — PASS |
| Unsupported feedback | 25% | ≤12.5% — **FAIL** |

The two semantic unsupported labels were `m7_ref_017_weak` and `m7_ref_002_partial`. Deterministic filters found no empty feedback, missing structured critical decision, unsupported candidate quote/technology, or schema inconsistency; the remaining defect was semantic and required the locked feedback judge.

## Directional score evidence

Stage 1 also produced Spearman .946, tier exact agreement 87.5%, tier adjacent agreement 100%, critical mention 100%, actionability 100%, and score-feedback consistency 100%. Pairwise and monotonicity both measured 100%, but only one complete within-group pair existed in the tiny mixed smoke set. These are directional smoke signals, not DEVELOPMENT acceptance evidence.

## Text/Voice alignment

Evaluator-only cross-mode difference is zero by architecture: the same textual input is evaluated once, and the same result is projected to both modes. Stage 1 therefore recorded mean/P95 score difference 0, exact tier agreement 100%, and material disagreement 0%. This does not measure real speech input variability. STT can change the transcript and remains a separate input-layer limitation.

## Latency and production cost direction

The eight real-time Flash calls had mean 3,709.7 ms, median 3,297.1 ms, and maximum 6,546.2 ms. This is an N=8 Stage 1 sample, not the post-HOLDOUT five-call production latency protocol and not a reliable P95.

Stage 1 Flash usage implies approximately $0.405 per 1,000 evaluator calls, versus the M7 current Text Pro estimate of $18.44 and current Voice Flash estimate of $0.275. The directional Text saving would be about 97.8%, but the candidate failed quality and was not activated; these figures are estimates, not billing claims.

## Statistical limitation

No expert human ground truth was used. Results remain automated reference-based evidence. The feedback judge and evaluator are Gemini-family systems, so correlated-model bias remains possible. N=8 cannot establish DEVELOPMENT or production score trust. The smoke coverage uses two PARTIAL controls because frozen M7 DEVELOPMENT contains no non-critical WEAK fixtures; it is not an exact non-overlapping realization of the requested category wording.

## Stop condition

No additional prompt, Pro, Flash-Lite, Gemini version, Stage 2, or HOLDOUT run was attempted after failure. Production remains unchanged at its M7 configuration. M8 must not start while this evaluator gate remains unresolved.
