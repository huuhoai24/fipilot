# M7 Answer Evaluation Quality

## Status

**CLOSED.** Vertex execution, DEVELOPMENT gate, locked HOLDOUT, reference, Text, Voice, cross-mode, feedback, repeatability, cost, and reproducible raw-evidence requirements completed.

This closes the evaluation milestone; it does not mean the evaluators passed every engineering threshold. Production score trust is **NOT ESTABLISHED** because both modes missed the 95% critical-error-detection target, Text strict monotonicity was 75%, and Voice pairwise/strict monotonicity were 89.58%/37.5%.

## Environment and benchmark

- Vertex project: `project-7dffc340-f73f-4e62-aec`; location: `global`; ADC available; connectivity PASS
- Frozen benchmark: 20 groups / 80 answers; DEVELOPMENT 12/48; HOLDOUT 8/32
- Coverage: 10 domains, all four levels, M3 provenance 100%
- DEVELOPMENT reference gate: PASS (pairwise 1.00, strict monotonic 1.00)
- HOLDOUT lock: `b44bc0394a880c2324745e063ae3a1d5bc7b04b1129a434238e712b9be783cd3`

## HOLDOUT results

| Metric | Text | Voice |
| --- | ---: | ---: |
| Automated-reference MAE | 1.2982 | 1.2443 |
| Spearman | 0.9540 | 0.8894 |
| Exact / adjacent tier agreement | 68.75% / 100% | 56.25% / 100% |
| Pairwise ordering | 95.83% | 89.58% |
| Strict monotonic groups | 75.0% | 37.5% |
| Dangerous over-score | 0% | 0% |
| Critical-error detection | 87.5% | 87.5% |

## Methodology limitation

No expert human ground truth was used. Results are automated reference-based evidence. Human sanity check remains **NOT COMPLETED** and was optional. RAGAS judge and production evaluators use the Gemini model family, creating correlated-model-family bias.

## Production isolation

Production remained unchanged: Text `gemini-2.5-pro` at temperature `0.1`; Voice `gemini-2.5-flash` at temperature `0.1`. No benchmark, HOLDOUT, production prompt, model, score scale, retrieval, or M3 corpus was tuned after results.

