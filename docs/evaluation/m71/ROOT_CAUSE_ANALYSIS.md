# M7.1 Root Cause Analysis

## Scope and evidence discipline

This analysis uses the frozen M7 DEVELOPMENT identities and DEVELOPMENT raw outputs only. It does not inspect M7 HOLDOUT samples individually. M7 datasets, references, raw evidence, reports, and lock remain unchanged.

No expert human ground truth was used. Results remain automated reference-based evidence.

## DEVELOPMENT failure inventory

Twenty of 48 DEVELOPMENT answers triggered at least one predeclared failure category. The machine-readable records are in `evaluation/m71/experiments/DEVELOPMENT_FAILURES.jsonl` and retain sample/question/answer IDs, reference tier, applicable critical-error definition, Text/Voice scores and feedback, and all assigned categories.

| Category | Count |
| --- | ---: |
| Text middle-tier score compression | 13 |
| Voice middle-tier score compression | 13 |
| Material Text/Voice rubric mismatch | 4 |
| Voice critical error not recognized | 2 |
| Voice critical error recognized but insufficient penalty | 2 |
| Voice weak answer over-scored | 2 |
| Voice feedback misses main weakness | 2 |

Text had no adjacent-pair reversal but only 8/12 strictly monotonic groups because four GOOD/STRONG pairs tied at 10. Voice had no adjacent-pair reversal but only 7/12 strictly monotonic groups because six adjacent pairs tied, principally at 9. Four answers differed by at least two points across modes.

## Root causes

1. **Critical-error policy absent.** The production prompt lists generic correctness/depth criteria but does not require the evaluator to decide whether a core misconception exists, name it, cap the tier/score, or explain a correction. Voice therefore sometimes described an answer as incorrect without a material score penalty.
2. **Critical-error state absent from the schema.** `AnswerEvaluation` has weaknesses and feedback but no explicit `critical_error_detected` or explanation field. Detection is therefore lost during structured parsing even when prose suggests recognition.
3. **M7 detection was a lexical proxy.** The M7 harness considered a critical error mentioned only when feedback/weakness text contained the first expected concept. It did not compare against the frozen critical-error definition. This can produce false negatives and is not a sufficient production contract. M7 evidence remains immutable; M7.1 will use an explicit general-purpose decision plus an independent automated-reference check.
4. **Score anchors absent.** Although the schema confirms a 0–10 range, the prompt does not define what score bands mean. Both models compress GOOD/STRONG answers near the top; Text saturates at 10 and Voice at 9. This creates ties and weak strict monotonicity.
5. **Text and Voice are not the same evaluator configuration.** They share the base schema and most prompt content, but Voice adds brevity wording, includes a different mode value in context, routes to Flash, and disables thinking. Text routes to Pro with default thinking. Four material DEVELOPMENT differences demonstrate that these differences are behaviorally relevant.
6. **Voice feedback capacity is constrained twice.** Flash/no-thinking and a two-sentence limit reduce explanation depth. This is consistent with M7 aggregate Voice feedback faithfulness, grounding, and actionability being weaker than Text.
7. **Parser/post-processing is not the primary score discrepancy.** Both modes use the same Pydantic schema, JSON generation path, retry policy, and no production score post-processing. The schema omission matters for critical-error observability, but mode score differences occur before parsing.

## Answer to the M7.1 root-cause questions

- Text missed the production-trust critical gate because the prompt/schema had no explicit critical-error contract and the M7 lexical proxy could not reliably observe semantic recognition.
- Voice has the same contract gap plus a lower-capability/no-thinking route and brevity constraint; two detected DEVELOPMENT misconceptions also received insufficient penalty.
- Material same-text differences arise from model, thinking, prompt wording, and mode-context differences—not from a single isolated cause.
- The dominant causes are rubric/prompt design and missing schema state, followed by model/route heterogeneity. Fixed tier mapping exposes compression but does not cause raw score differences.
- General score anchors, critical-error policy, and one shared evaluation prompt/core are the minimum-complexity calibration hypothesis. Same-model Voice is reserved only if the bounded budget permits and aligned prompts fail.

