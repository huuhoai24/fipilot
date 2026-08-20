# M6 Question Generation Quality Report

Status: CLOSED. Evidence is synthetic controlled + blinded Gemini 2.5 Pro judge; human validation is NOT COMPLETED.

## Dataset

80 scenarios; development 48; holdout 32; 10 domains; Intern/Junior/Middle/Senior; English and Vietnamese. Human-review pack: 20 scenarios / 80 outputs, labels pending.

## Frozen configuration

Question Generator `gemini-2.5-flash`, temperature 0.2, thinking budget 0; Lexical production Top-K 8; Vector Top-K 8; Hybrid RRF k=60, weights .75/1.0, Top-K 8; compatible levels `same_plus_unspecified`; judge `gemini-2.5-pro`, temperature 0, thinking budget 128. Configuration hash `6f68de3e4b72cdd27acbbf9a2c51d45c90a68010201dfa61266fd65c1696773b`.

## Holdout question quality

| Metric | No RAG | Lexical | Vector | Hybrid |
|---|---:|---:|---:|---:|
| Technical validity | 1.0000 | 1.0000 | 0.9688 | 0.9688 |
| Role relevance | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| CV alignment | 1.0000 | 1.0000 | 1.0000 | 0.9688 |
| Difficulty exact | 0.8750 | 0.9375 | 0.9062 | 0.9062 |
| Specificity (0–2) | 1.8750 | 1.8750 | 1.9375 | 1.8750 |
| Hallucination | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Grounding (0–2) | N/A | 1.6562 | 1.8750 | 1.6875 |
| Retrieval utilization | N/A | 1.0000 | 1.0000 | 0.9688 |

## Development summary

Development n=48 per condition. Technical validity: No-RAG 0.9792, Lexical 0.9792, Vector 0.9792, Hybrid 0.9792. Vector grounding/utilization were 1.5000/0.9167; Hybrid 1.4375/0.8958. The level strategy was selected only from development retrieval evidence before holdout.

## Decisions

Question Generator: **QG_ACCEPTABLE**. RAG for Question Generation: **INSUFFICIENT_EVIDENCE**. Production activation ready: **NO** because human review is not completed.

## Council-facing evidence

- RAG primarily changed grounding: holdout means Lexical 1.6562, Vector 1.8750, Hybrid 1.6875. It did not produce a clear overall preference win.
- Without RAG, technical validity remained 1.0000, specificity 1.8750, and pairwise results were mostly ties or small margins.
- Vector did not clearly improve generated questions over Lexical: pairwise 7–7–18; specificity delta +0.0625; technical-validity delta -0.0312.
- Quality is reported as technical validity, role/CV alignment, difficulty agreement, specificity, clarity, answerability, redundancy, and hallucination—not generic “accuracy.”
- Unsupported candidate-claim rate was 0.0000. Technical false-premise rate reached 0.0312 for Hybrid and 0 for the other conditions.
- Grounding is verified with blinded judge score, cited chunk IDs, deterministic concept overlap, retrieved chunk/topic IDs, and source provenance.

## Interpretation

RAG impact is measured by paired questions with identical scenario/model/settings and only the evaluation-only retrieved-context block changed. No-RAG remains the ablation. Vector's semantic recovery is assessed in `16` lexical-miss/vector-hit holdout scenarios. Hybrid marginal value is evaluated through paired Vector-vs-Hybrid results, not retrieval MRR alone.

Do not call these values real-world accuracy or human accuracy. Every holdout condition has n=32; Vietnamese and targeted slices are directional.

## Limitations

- Human labels are not completed, so LLM-judge agreement with people is unknown and activation is NO.
- The frozen holdout contains only English outputs; all 20 Vietnamese scenarios landed in development. Vietnamese results are development-only and cannot be generalized as holdout evidence.
- Production retrieval currently feeds the Planner; production Question Generator does not accept raw chunks. M6 therefore used an evaluation-only fixed context block appended to the unchanged production QG prompt. This isolates RAG impact but is not an end-to-end production topology test.
- Vector search used frozen local M4 vectors for reproducibility; query-embedding latency is batch-amortized rather than per-request Firestore E2E latency.
- The deterministic candidate-claim verifier is conservative and semantic technical validity still depends on one blinded Gemini 2.5 Pro judge configuration.
- The 16-case M5 lexical-miss/vector-hit slice is a development diagnostic; no matching cases landed in the frozen M6 holdout.
