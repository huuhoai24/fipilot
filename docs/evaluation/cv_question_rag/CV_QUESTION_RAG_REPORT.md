# Public Resume-derived Question Generation and Retrieval Evaluation

Status: **PARTIAL_PENDING_HUMAN_REVIEW**

## Evaluation scope

- Resume subset scanned: 500 / 2372 public PDFs from `CHON_LOC_CV`.
- Pseudonymized selected cases: 300 (150 development, 150 holdout).
- Retrieval cases: 300 using the current production lexical retriever.
- Question cases: 150 holdout cases using Gemini Question Generator plus a separate LLM-as-judge pass.
- Human-review template: 60 stratified questions; scores remain blank and pending.

No filename, raw Resume text, name, email, phone number, or other direct personal field is retained in the dataset, raw logs, prompts, or reports. IDs are deterministic truncated SHA-256 pseudonyms, so this is pseudonymization rather than irreversible anonymization.

## Retrieval results

- HitRate@1/3/5/8: 0.9167 / 0.9967 / 1.0000 / 1.0000
- Recall@5/8: 0.5928 / 0.8721
- MRR@8: 0.9564
- Latency mean/P95: 8.60 / 13.26 ms

The retrieval labels come from exact knowledge-catalog titles detected in each Resume. This is a source-derived coverage test, not a human-labelled relevance or semantic-search benchmark.

## Question Generation results

- Technical validity: 1.0000
- Role relevance: 1.0000
- CV-derived skill alignment: 1.0000
- Mean clarity: 5.0000 / 5
- Mean specificity: 1.5400 / 2
- Mean retrieval grounding: 1.4200 / 2
- Deterministic grounding overlap: 0.3049
- Retrieval utilization rate: 0.9067
- Target-topic mention rate: 0.8533
- Language match rate: 1.0000
- Difficulty-label exact match: 0.8333
- Normalized exact duplicate rate: 0.0067
- Opening-phrase repetition rate: 0.8067
- Unsupported experience-assumption rate: 0.7067
- False-premise rate: 0.0000
- Pattern audit counts: 1 exact-duplicate excess, 121 repeated-opening excess, 106 unsupported-experience flags.

Quality scores are LLM-as-judge measurements; overlap, utilization, duplication, repetition, language, difficulty, and unsupported-assumption values are deterministic rule-based audits. Neither group must be presented as human agreement until at least two independent technical reviewers complete the frozen template and disagreements are adjudicated.

## Claim boundary and limitations

- Resume exact-title matching selects eligible cases and therefore favors lexical retrieval; high HitRate is expected and must not be generalized to paraphrases.
- The redacted Candidate Profile retains detected catalog skills but removes real project/experience prose, so this evaluates skill alignment rather than deep personal-experience grounding.
- The deterministic unsupported-experience check is conservative and pattern-based; flagged questions require human review rather than automatic rejection.
- The source corpus is public per project-owner confirmation, but public availability is not a substitute for a documented consent, retention, and research-ethics protocol.
- Domain/category slices with fewer than 30 cases are descriptive only.
- Human review is pending; overall status remains partial.
