# Error Analysis

The dominant error pattern is optimistic scoring: mean signed difference was +1.2006 Text and +0.9287 Voice. Text preserved pair ordering well (95.83%) but tied enough within groups to reduce strict monotonicity to 75%. Voice had no pair reversals, but five ties reduced pairwise accuracy to 89.58% and strict monotonicity to 37.5%.

Both modes missed one critical error. Feedback risk is larger in Voice: 12.5% unsupported-feedback rate, 31.25% grounding, and 40.625% actionability. Domain and level slices contain only 4–8 answers and are directional only; the valid HOLDOUT raw metrics preserve them for inspection.

