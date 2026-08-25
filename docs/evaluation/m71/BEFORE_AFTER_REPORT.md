# M7 to M7.1 Before/After

M7 is the immutable HOLDOUT baseline. M7.1 A2 is DEVELOPMENT-only diagnostic evidence: it was not frozen, was not run on HOLDOUT, and was not activated.

| Metric | M7 Text HOLDOUT | M7 Voice HOLDOUT | M7.1 Text HOLDOUT | M7.1 Voice HOLDOUT |
| --- | ---: | ---: | ---: | ---: |
| MAE | 1.298 | 1.244 | NOT RUN | NOT RUN |
| Spearman | .954 | .889 | NOT RUN | NOT RUN |
| Pairwise ordering | 95.83% | 89.58% | NOT RUN | NOT RUN |
| Strict monotonic | 75.0% | 37.5% | NOT RUN | NOT RUN |
| Critical detection | 87.5% | 87.5% | NOT RUN | NOT RUN |
| Dangerous overscore | 0.0% | 0.0% | NOT RUN | NOT RUN |

All M7.1 HOLDOUT cells mean **NOT RUN — NO SAFE DEVELOPMENT WINNER**.

| Cross-mode metric | M7 HOLDOUT | M7.1 HOLDOUT |
| --- | ---: | ---: |
| Mean absolute difference | .959 | NOT RUN |
| P95 absolute difference | 2.5 | NOT RUN |
| Exact tier agreement | 81.25% | NOT RUN |
| Material disagreement | 12.5% | NOT RUN |

For diagnostic context only, A2 DEVELOPMENT reached 100% critical-error detection and 0% dangerous over-score in both modes, but failed Text monotonicity (75%), cross-mode disagreement (16.67%), and unsupported-feedback gates (Text 16.67%, Voice 12.5%). These DEVELOPMENT numbers are not an M7.1 HOLDOUT after-result.

No expert human ground truth was used. Results remain automated reference-based evidence.
