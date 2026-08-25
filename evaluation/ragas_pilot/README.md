# FiPilot RAGAS-Style Pilot Evaluation

This directory evaluates the current FiPilot retrieval, question-generation,
and Answer Evaluator seams without changing production behavior or model
routing.

The dataset is a **synthetic controlled evaluation set** derived from actual
catalog metadata. It is not a human benchmark, expert-labelled benchmark, or
real-user benchmark. No historical presentation metric is used as a target.

## What is evaluated

### Retrieval

- Actual `LocalKnowledgeRetriever`
- RAGAS-inspired context precision without reference
- Per-context relevant / partially relevant / irrelevant judgment
- Mean context relevance, Relevant@K, Irrelevant@K
- Empty retrieval rate and latency
- Separate deterministic controlled HitRate@8, Recall@8, and MRR@8

True reference-based Context Recall remains `null` because no human-reviewed
reference contexts or reference answers exist.

### Question Generation

- Actual `InterviewPlannerAgent`
- Actual `QuestionGeneratorAgent`
- Role relevance, CV alignment, RAG grounding, difficulty alignment,
  technical validity, clarity, and hallucinated candidate claims

Retrieved contexts reach Question Generation through the production mediation
path: retriever -> planner -> selected InterviewRound -> question generator.

### Answer Evaluation

- Actual text-mode `EvaluatorAgent`
- Four controlled ordinal answer tiers per generated question
- Strict score monotonicity
- Rubric adherence, evidence grounding, unsupported feedback,
  actionability, and score-feedback consistency
- Three-run repeatability on the `good` answer in each smoke group

No human score is assigned. Human MAE, agreement, and correlation are not
evaluated.

## Run

From the repository root, with Google Application Default Credentials and
Vertex AI access configured:

```powershell
.\backend\.venv\Scripts\python.exe evaluation\ragas_pilot\run_pilot.py `
  --smoke-size 10 `
  --target-size 30 `
  --robustness-subset 2
```

The runner intentionally stops after the 10-case smoke pilot. Review runtime,
failures, logical call count, and estimated visible-token cost in
`run_manifest.json` before authorizing a 30-case run.

## Evidence structure

```text
evaluation/ragas_pilot/
|-- README.md
|-- IMPLEMENTATION_AUDIT.md
|-- run_manifest.json
|-- model_calls.jsonl
|-- rag/
|   |-- samples.jsonl
|   |-- summary.json
|   `-- summary.md
|-- question_generation/
|   |-- samples.jsonl
|   |-- summary.json
|   `-- summary.md
|-- answer_evaluation/
|   |-- samples.jsonl
|   |-- summary.json
|   `-- summary.md
`-- overall_summary.md
```

Every successful or failed sample is checkpointed to JSONL. Provider raw text
is not exposed by the production public LLM seam; the exact Pydantic-validated
application output is preserved and this limitation is explicit in each
record. Model-call logs contain counts, model names, latency, and approximate
character-derived token counts, but never prompts, secrets, or tokens.

## Evidence classes

- A: deterministic/code-computed
- B: LLM-as-judge
- C: synthetic controlled evaluation
- D: human-labelled benchmark

This pilot uses A, B, and C only. Nothing is classified D.

## Ragas package

`ragas` was not installed during audit. No official Ragas metric is claimed.
Custom metrics are always named RAGAS-inspired or FiPilot-specific.

## Tests

```powershell
.\backend\.venv\Scripts\python.exe -m pytest evaluation\ragas_pilot\tests -q
```
