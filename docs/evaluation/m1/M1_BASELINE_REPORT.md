# M1 Ground Truth Evaluation & Reproducible Baseline

Status: **CLOSED**  
Run timestamp: `2026-08-18T12:41:23.591491+00:00`  
Git commit: `3a38b4818a0bb4d2c9e51efd013c295a4f039894` (dirty tree: `true`)

## Dataset

- Resume: 30 synthetic-controlled PDF/DOCX cases; no real PII.
- Retrieval: 50 synthetic-controlled, catalog-backed queries; not human-labelled.
- Question: 30 synthetic-controlled cases through Planner → active lexical retrieval → Question Generator.
- Answer: 40 actual technical answers in 10 ordered weak/partial/good/strong groups; not human exact-scored.

## Resume Baseline

| Field | TP | FP | FN | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| skills | 150 | 2 | 6 | 0.9868 | 0.9615 | 0.9740 |
| education | 30 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| experiences | 22 | 9 | 8 | 0.7097 | 0.7333 | 0.7213 |
| projects | 25 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |

- Parse success: 1.0
- Schema validation: 1.0
- Empty extraction: 0.0
- Truncation exposure: 0.03333333333333333
- Latency mean/P95 ms: 4340.200409999427 / 17084.214614986508
- Boundary skill recall before/near/after 12k: {'before': 0.0, 'near': 0.0, 'after': 0.0}
- Certifications: **NOT EVALUATED** (not a canonical CandidateProfile field).

Education is matched by normalized institution+degree+field, experience by
company+title, and projects by name. Descriptions remain raw evidence and are
not forced into brittle exact match.

## Retrieval Baseline

- HitRate@1/3/5/8: 0.84 / 0.98 / 1.0 / 1.0
- Recall@1/3/5/8: 0.76 / 0.98 / 1.0 / 1.0
- Precision@5/8: 0.24000000000000002 / 0.15
- MRR@8: 0.9116666666666666
- Zero-result rate: 0.0
- Irrelevant-result rate: **NOT EVALUATED**; labels are not exhaustive judgments for all catalog topics.
- Latency mean/median/P95 ms: 6.964352002833039 / 6.561499991221353 / 10.128685014205985
- Production numeric score: **NOT AVAILABLE**; the public seam returns strings, so raw `score` is `null`.

## Question Baseline

- Role relevance: 1.0
- CV alignment: 1.0
- Technical validity: 1.0
- Difficulty alignment (1–5): 4.2
- Clarity (1–5): 5.0
- Retrieved-context grounding (0–2): 2.0
- Hallucinated candidate claim rate: 0.0
- Human validation: **NOT EVALUATED**.

These are LLM-as-judge quality measurements at temperature 0, not accuracy.
The exact parsed judge response is retained; provider pre-parse text is not
exposed by the production LLM seam.

## Answer Evaluation Baseline

- Human MAE/RMSE/within-1/within-2: **NOT EVALUATED** (no verified human exact scores).
- Synthetic allowed-range agreement: 0.7
- Pairwise ordering accuracy: 0.7833333333333333
- Strict monotonic group rate: 0.3
- Mean Spearman tier correlation: 0.7224412872795758
- Feedback judge: {'method': 'LLM quality judgment, separate from deterministic tier metrics', 'feedback_grounding_rate': 1.0, 'unsupported_feedback_rate': 0.0, 'mean_actionability': 4.025, 'mean_score_feedback_consistency': 4.925}

## Text vs Voice Evaluator

{'sample_count': 4, 'mean_absolute_score_difference': 1.5, 'tier_agreement_rate': 0.5, 'mean_feedback_token_jaccard': 0.1867831461341891, 'semantic_feedback_consistency': 'NOT EVALUATED: no human semantic labels; raw feedback retained'}

## Repeatability

- Question: {'subset_size': 2, 'schema_success_rate': 1.0, 'clarity_variance': 0.0}
- Answer: {'subset_answer_count': 4, 'mean_score_variance': 0.34944444444444456, 'schema_success_rate': 1.0}
- Resume: {'subset_size': 2, 'runs_per_sample': 3, 'schema_success_rate': 1.0, 'exact_normalized_skill_agreement_rate': 1.0}

## Failure Analysis

- Retrieval miss buckets: {}
- Resume field errors (FP/FN): {'skills': (2, 6), 'education': (0, 0), 'experiences': (9, 8), 'projects': (0, 0)}
- Answer ordering/range failures: {'non_monotonic_groups': 7, 'answers_outside_synthetic_allowed_range': 12, 'tied_or_reversed_tier_pairs': 13}
- Per-sample failures remain in raw JSONL with error type/message.

## Limitations

- All M1 labels are synthetic controlled; none are human-labelled production ground truth.
- Question and feedback semantic metrics are LLM-as-judge quality scores, not accuracy.
- The question generator and judge use the same Gemini model family, so correlated judgment bias is possible.
- Catalog-derived retrieval queries contain catalog terminology and may overstate performance on real paraphrases.
- The production retrieval seam does not expose numeric scores.
- Retrieval labels are not exhaustive enough to classify every non-labelled result as irrelevant.
- Certifications are not a canonical CandidateProfile field and are not evaluated.
- Resume cases are synthetic English fixtures; image-only/OCR robustness and real-layout generalization are not evaluated.
- Provider pre-parse model text is unavailable at the production JSON seam; validated outputs are the retained raw seam.
- Text-versus-voice feedback overlap is lexical Jaccard, not human semantic agreement.

## Reproducibility

- Command: `python -m evaluation.m1.run_baseline --all --execute-paid --resume-from-raw m1-20260818-baseline`
- Dataset versions: `{'resume': 'm1-resume-synthetic-controlled-v1', 'retrieval': 'm1-retrieval-catalog-controlled-v1', 'questions': 'm1-question-synthetic-controlled-v1', 'answers': 'm1-answer-technical-tiers-v1'}`
- Knowledge SHA-256: `88be8d7de7fe57dca91fe694f46cddebd1ae503e86d2a5eab44637bf76eef03d`
- Random seed: `20260818`
- Raw evidence: `evaluation/m1/raw/m1-20260818-baseline/`
- Dirty status, diff stat, production hashes, retry policy, models, temperatures, and counts are in `RUN_MANIFEST.json`.

## Comparison With Historical Results

M0 found contradictory resume aggregates and an older synthetic RAGAS-style
pilot on a different commit. The historical-only claims were Resume skill
precision/recall 90.88%/85.67% (conflicting with 49.88%/51.37%), Question
relevance/CV alignment 99.33%/100%, and Answer MAE 0.7 with 97.34% consistency.
They have no supporting sample-level labels and are not merged with this
reproduced baseline. M1 metrics above are recomputed solely from this run's raw
JSONL.
