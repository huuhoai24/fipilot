# M7.1 Evaluator Calibration Report

## Decision

**M7.1 STATUS = PARTIAL**  
**PRODUCTION_ACTIVATION_READY = NO**

The predeclared safety-first selection rule returned `NO_SAFE_WINNER`. Consequently, no M7.1 configuration was frozen, no M7.1 HOLDOUT was run, and the production Answer Evaluation seam remains byte-for-byte aligned with the M7 hashes.

## Evidence discipline

- Root-cause work used frozen M7 DEVELOPMENT identities and DEVELOPMENT outputs only.
- M7 HOLDOUT was used only through already-published aggregate M7 metrics; no HOLDOUT sample was inspected for tuning.
- M7 benchmark, split, reference, RAGAS, raw-output, report, and holdout-lock artifacts were not modified.
- Existing M7 reference/RAGAS outputs were reused; static reference re-evaluation calls were zero.
- No expert human ground truth was used. Results remain automated reference-based evidence, with possible correlated Gemini-family bias.

## Root cause and seam audit

The production prompt had no explicit semantic critical-error contract and no stable 0–10 anchors. The schema had no structured critical-error decision. M7's detection field was a lexical proxy rather than a semantic contract. Text and Voice shared parsing and schema, but differed in model, thinking configuration, mode context, and a Voice brevity instruction. The exact audit is in `TEXT_VOICE_ALIGNMENT_REPORT.md`; the 20-row DEVELOPMENT failure inventory is in `evaluation/m71/experiments/DEVELOPMENT_FAILURES.jsonl`.

## Frozen experiment design

The configuration catalog and selection rule were hashed before paid execution. Only two bounded configurations were retained:

| Config | Models | Change | Execution |
| --- | --- | --- | --- |
| A0 `a0-production-baseline` | Text Pro / Voice Flash | M7 production behavior | Reused DEVELOPMENT outputs; diagnostic only because the source run was invalidated for ordering and feedback was incomplete |
| A2 `a2-shared-critical-anchors` | Text Pro / Voice Flash | One shared core, explicit general critical-error policy, explicit 0–10 anchors, structured critical-error fields | Complete paid DEVELOPMENT run |

Pro/Pro was excluded before the paid comparison under the minimum-complexity and $4 default-budget rules. This means M7.1 did not establish whether model homogeneity alone would solve cross-mode disagreement.

## DEVELOPMENT results

| Metric | A0 Text | A0 Voice | A2 Text | A2 Voice |
| --- | ---: | ---: | ---: | ---: |
| MAE | 1.220 | 1.148 | 1.017 | .777 |
| Spearman | .938 | .916 | .901 | .947 |
| Tier exact | 72.92% | 68.75% | 72.92% | 81.25% |
| Tier adjacent | 100% | 100% | 100% | 100% |
| Pairwise ordering | 94.44% | 90.28% | 95.83% | 97.22% |
| Strict monotonic groups | 66.67% | 58.33% | 75.0% | 83.33% |
| Dangerous overscore | 0% | 0% | 0% | 0% |
| Critical detection | 100% | 83.33% | 100% | 100% |

| Cross-mode metric | A0 DEVELOPMENT | A2 DEVELOPMENT |
| --- | ---: | ---: |
| Mean absolute difference | .956 | 1.079 |
| P95 absolute difference | 2.3 | 2.5 |
| Exact tier agreement | 83.33% | 83.33% |
| Material disagreement | 8.33% | 16.67% |

A0 feedback and repeatability are not presented as comparable DEVELOPMENT metrics because its reused M7 source run was explicitly invalidated and completed only 30/96 feedback bundles. A2 completed all 96 feedback bundles and the limited repeatability subset.

## Gate outcome

A2 passed critical-error detection, dangerous-over-score, pairwise ordering, Spearman, Voice monotonicity, and score-feedback consistency gates. It failed:

- Text strict monotonicity: 75% versus the required 80%.
- Material Text/Voice disagreement: 16.67% versus the maximum 5%.
- Text unsupported feedback: 16.67% versus the maximum 5%.
- Voice unsupported feedback: 12.5% versus the maximum 5%.

The shared critical policy fixed DEVELOPMENT critical-error recognition without unsafe high scores, and MAE improved relative to A0. It did not align raw scores across heterogeneous models and it worsened the unsupported-feedback signal. Under the frozen rule, lower MAE cannot override those failures.

## Feedback and repeatability

| DEVELOPMENT metric | A2 Text | A2 Voice |
| --- | ---: | ---: |
| RAGAS faithfulness | .622 | .449 |
| Grounding rate | 27.08% | 18.75% |
| Unsupported feedback | 16.67% | 12.5% |
| Critical-error mention | 100% | 100% |
| Actionability | 75.0% | 68.75% |
| Score-feedback consistency | 100% | 100% |

Repeatability used 10 answers × 3 evaluations per mode. Text mean score variance was .043, tier-flip rate 0%, and feedback token Jaccard .347. Voice mean score variance was .100, tier-flip rate 0%, and feedback token Jaccard .650. Voice exceeded a one-point score range on 20% of repeated answers.

## Latency and cost

| DEVELOPMENT provider call | Mean ms | Median ms | P95 ms |
| --- | ---: | ---: | ---: |
| A2 Text / Pro | 18,158.7 | 18,319.2 | 21,454.4 |
| A2 Voice / Flash | 2,964.1 | 2,819.6 | 4,048.1 |

Provider-reported A2 production-evaluator usage was conservatively estimated at $1.404151 for 136 calls including repeats. Exact RAGAS provider usage is unavailable, so the conservative M7.1 total remains the dry-run $1.69 envelope, under the $4 default budget and $7 hard ceiling. There were zero static-reference re-judging calls. A2 was not activated, so actual production cost impact is zero.

## HOLDOUT and activation

`NOT RUN — NO SAFE DEVELOPMENT WINNER` applies to every M7.1 HOLDOUT metric. There is no `m71_frozen_config_hash`. The A2 candidate config hash (`c6b44ac2e39753c8737836c60ac274ef3a6fc563560c3c2cf83bf7cfb8ebdc89`) identifies DEVELOPMENT evidence only and must not be interpreted as a frozen winner.

Decisions:

- `TEXT_EVALUATOR_NEEDS_OPTIMIZATION`
- `VOICE_EVALUATOR_NEEDS_OPTIMIZATION`
- `TEXT_VOICE_ALIGNMENT_REQUIRED`
- Production score trust: `LOW`
- `PRODUCTION_ACTIVATION_READY = NO`

## Remaining blockers

M7.1 still needs a bounded DEVELOPMENT candidate that simultaneously reduces model-dependent score mapping and unsupported feedback while preserving the newly demonstrated critical-error safety. Only after such a candidate passes the frozen DEVELOPMENT gates may one unchanged HOLDOUT run and production activation be considered. No M8 work should begin while M7.1 remains PARTIAL.
