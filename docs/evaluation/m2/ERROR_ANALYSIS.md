# M2 Experience Error Analysis

## M1 reproduced failure taxonomy

- 8 paired FP/FN errors: the model dropped the two-digit suffix from `Synthetic Systems NN` while preserving the title.
- 1 FP: the unusual section order in `resume_021` caused the identity pair (`candidate name`, `recent role`) to be emitted as an Experience.

## Fix and outcome

The section parser extracts title/company/date evidence only inside recognized English/Vietnamese Experience sections. The verifier reconciles a model claim when title and normalized company prefix agree, restores the exact source value, and rejects an employing organization equal to the candidate name. Claims without a confident match remain `uncertain`; they are not deleted merely because an exact substring is absent.

| Metric | M1 | M2 |
|---|---:|---:|
| TP | 22 | 30 |
| FP | 9 | 0 |
| FN | 8 | 0 |
| F1 | 0.7213 | 1.0000 |
