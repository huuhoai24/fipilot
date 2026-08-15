# FiPilot RAGAS-Style Pilot Evaluation

## Run Metadata

- Git commit: `1249cc50a6995ac0a72465fdfb2d708d2cde5c1c`
- Evaluator/judge: `gemini-2.5-flash` on Vertex AI, temperature 0
- Ragas version: not installed
- Pilot size: 10 smoke case groups; target 30 pending review
- Date: 2026-08-15T00:48:05.880129+00:00
- Logical model calls: 122
- Approximate runtime: 1215.5681462000066 seconds
- Estimated visible-token cost: $0.423725 USD

## RAG Retrieval

- Samples: 10
- RAGAS-inspired reference-free context precision: 0.8150387377173092
- Mean context relevance: 0.435
- Empty retrieval rate: 0.0
- Median latency: 10.989250004058704 ms
- P95 latency: 14.780350006185468 ms
- Controlled HitRate@8: 1.0
- Controlled MRR@8: 1.0
- Reference-based Context Recall: **NOT EVALUATED**

Reason: No human-reviewed reference contexts or reference answers are available in this pilot.

## Question Generation

- Samples: 10
- Role relevance: 1.0
- CV alignment: 1.0
- Technical validity: 1.0
- RAG grounding: 2.0 / 2
- Difficulty alignment: 4.2 / 5
- Clarity: 4.3 / 5
- Unsupported candidate claim rate: 0.0

## Answer Evaluation

- Samples: 40 across 10 controlled groups
- Controlled monotonicity: **NOT EVALUATED**
- Raw observed ordering rate: 0.0 (audit only; invalid controlled-answer ladder)
- Rubric adherence: 4.6 / 5
- Evidence grounding: 1.0
- Unsupported feedback rate: 0.0
- Feedback actionability: 4.1 / 5
- Score-feedback consistency: 4.8 / 5
- Repeatability range <= 1: 1.0
- Mean score standard deviation: 0.1414213562373095
- Human MAE: **NOT EVALUATED**
- Human correlation: **NOT EVALUATED**

Reason: No verified human-labelled benchmark is available.

Controlled-answer limitation: the deterministic `good` and `strong` templates
described expected points rather than supplying validated stronger technical
answers. The raw run is retained, but its ordering rate is not slide-safe and
must not be attributed to the production Evaluator.

## Defense Classification

- A: deterministic retrieval latency, empty rate, controlled HitRate/Recall/MRR, repeatability arithmetic
- B: LLM-as-judge relevance and rubric scores
- C: all Candidate Profiles and answer quality tiers are synthetic controlled
- D: none; no human-labelled benchmark was used

## Scale Decision

The run intentionally stopped after the 10-case smoke pilot. Scaling to 30
requires review of the measured logical call count, runtime, failures, and
estimated cost in `run_manifest.json`.

Pilot status: **PARTIAL** because the retrieval and question-generation smoke
sets are valid, while the answer monotonicity ladder requires redesign and a
new approved run.
