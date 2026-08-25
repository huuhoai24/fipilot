# RAGAS Reference Evaluation

RAGAS `0.4.3` ran through the current Google GenAI Vertex client with judge `gemini-2.5-pro` at temperature `0` and `gemini-embedding-001` in `global`.

| Intended tier | DEVELOPMENT Answer Correctness | HOLDOUT Answer Correctness | HOLDOUT rubric | Concept coverage |
| --- | ---: | ---: | ---: | ---: |
| WEAK | 0.2091 | 0.2227 | 1.000 | 0% |
| PARTIAL | 0.5247 | 0.5384 | 2.750 | 50% |
| GOOD | 0.7130 | 0.7118 | 4.125 | 75% |
| STRONG | 0.7963 | 0.7501 | 4.875 | 100% |

DEVELOPMENT and HOLDOUT pairwise ordering were both 1.00; strict monotonic group rate was 1.00 for both. Critical-error labels were internally consistent; HOLDOUT RAGAS/dataset critical-error agreement was 96.875%. Source provenance was 100%.

No expert human ground truth was used. These are automated reference-based results, not expert-labelled results. Gemini-family judge/evaluator correlation remains a limitation.
