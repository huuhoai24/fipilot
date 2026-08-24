# FiPilot Evaluation Master Sheet (M1–M7)

> Purpose: single source of truth for capstone/defense evaluation metrics.
>
> Scope: M1–M7 only. M7.1/M7.2 are optimization experiments and are not part of the primary defense metrics. M8 is excluded from the primary defense evaluation scope.
>
> Evidence labels:
> - Synthetic-controlled / controlled fixtures
> - Deterministic corpus audit
> - LLM-as-judge / automated reference-based
> - NOT expert-human ground truth unless explicitly stated

---

## 1. Executive Summary

| Area | Metric | Result | Evidence Type |
|---|---:|---:|---|
| Resume Extraction | Overall micro F1 | **98.53%** | Controlled fixtures |
| Resume Extraction | Experience F1 | **100%** | Controlled fixtures |
| OCR | Scan CV success | **6/6 = 100%** | Controlled fixtures |
| Knowledge Corpus | Documents | **4,419** | Deterministic corpus audit |
| Chunking | Chunks | **4,492** | Deterministic corpus audit |
| Corpus Preservation | Content preservation | **100%** | Deterministic corpus audit |
| Embedding | Model | `gemini-embedding-001` | Implementation audit |
| Embedding | Dimension | **768D** | Implementation audit |
| Retrieval | Vector paraphrase Hit@5 | **98%** | Paraphrase stress benchmark |
| Retrieval | Vector holdout MRR | **0.9531** | Synthetic-controlled holdout |
| Retrieval | Hybrid holdout MRR | **0.9688** | Synthetic-controlled holdout |
| Question Generation | Technical validity | **96.88–100%** | LLM-as-judge |
| Question Generation | Candidate hallucination | **0%** | LLM-as-judge |
| Question Generation | Vector grounding | **1.875 / 2** | LLM-as-judge |
| Answer Evaluation Text | Spearman | **0.954** | Automated reference-based |
| Answer Evaluation Voice | Spearman | **0.889** | Automated reference-based |
| Answer Evaluation Text | MAE | **1.298 / 10** | Automated reference-based |
| Answer Evaluation Voice | MAE | **1.244 / 10** | Automated reference-based |
| Critical Error Detection | Text / Voice | **87.5% / 87.5%** | Automated reference-based |

---

# 2. M1 — Reproducible Baseline

## 2.1 Resume Extraction

Dataset: **30 synthetic-controlled resumes (PDF + DOCX)**

| Field | TP | FP | FN | F1 |
|---|---:|---:|---:|---:|
| Skills | 150 | 2 | 6 | **0.9740** |
| Education | 30 | 0 | 0 | **1.0000** |
| Experience | 22 | 9 | 8 | **0.7213** |
| Projects | 25 | 0 | 0 | **1.0000** |
| Overall micro | 227 | 11 | 14 | **0.9478** |

Additional metrics:

| Metric | Result |
|---|---:|
| Parse/schema success | **100%** |
| Empty extraction | **0%** |
| Long-CV truncation exposure | **3.33%** |
| Mean latency | **4,340 ms** |
| P95 latency | **17,084 ms** |
| Certifications | **NOT EVALUATED** |

Key baseline issue: **Experience F1 = 72.13%**

## 2.2 Retrieval Baseline

Dataset: **50 controlled catalog-backed queries**

Production retrieval:
- Weighted lexical overlap
- Top-K = 8
- No embedding
- No vector DB

| Metric | Result |
|---|---:|
| HitRate@1 | **0.84** |
| HitRate@3 | **0.98** |
| HitRate@5 | **1.00** |
| HitRate@8 | **1.00** |
| Recall@1 | **0.76** |
| Recall@3 | **0.98** |
| Recall@5 | **1.00** |
| Recall@8 | **1.00** |
| Precision@5 | **0.24** |
| Precision@8 | **0.15** |
| MRR@8 | **0.9117** |
| Zero-result rate | **0%** |
| Mean latency | **6.96 ms** |
| Median latency | **6.56 ms** |
| P95 latency | **10.13 ms** |

## 2.3 Question Generation Baseline

Dataset: **30 controlled production-pipeline cases**

| Metric | Result |
|---|---:|
| Role relevance | **100%** |
| CV alignment | **100%** |
| Technical validity | **100%** |
| Difficulty alignment | **4.2 / 5** |
| Clarity | **5.0 / 5** |
| RAG grounding | **2.0 / 2** |
| Hallucinated candidate claim | **0%** |

> Evidence type: LLM-as-judge / synthetic-controlled. Not human accuracy.

## 2.4 Answer Evaluation Baseline

Dataset: **10 groups × 4 answer tiers**

| Metric | Result |
|---|---:|
| Allowed-range agreement | **70%** |
| Pairwise ordering | **78.33%** |
| Strict monotonicity | **30%** |
| Mean Spearman | **0.7224** |
| Feedback grounding | **100%** |
| Unsupported feedback | **0%** |
| Feedback actionability | **4.025 / 5** |
| Score-feedback consistency | **4.925 / 5** |
| Repeatability score variance | **0.3494** |

Text vs Voice:

| Metric | Result |
|---|---:|
| Mean absolute score difference | **1.5** |
| Tier agreement | **50%** |
| Feedback Jaccard similarity | **0.1868** |

Human evaluation: **NOT EVALUATED**

---

# 3. M2 — Resume Processing Upgrade

Pipeline:
`File validation → native PDF/DOCX extraction → OCR fallback → section-aware context → Gemini extraction → source verification`

OCR:
- RapidOCR / ONNX
- PyMuPDF
- 20-page limit

| Metric | M1 | M2 |
|---|---:|---:|
| Experience F1 | 0.7213 | **1.0000** |
| Skills F1 | 0.9740 | **0.9772** |
| Overall micro F1 | 0.9478 | **0.9853** |
| Mean latency | 4,340 ms | **3,742 ms** |
| P95 latency | 17,084 ms | **14,716 ms** |

Additional:

| Metric | Result |
|---|---:|
| Scan CV OCR success | **6/6 = 100%** |
| Long-CV marker recovery | **6/6 = 100%** |
| Invalid-document rejection | **4/4** |
| Context bound | **16k chars** |
| Estimated evaluation cost | **~$0.0213** |

Headline:
- Overall Resume micro F1: **94.78% → 98.53%**
- Experience F1: **72.13% → 100%**

---

# 4. M3 — Knowledge Corpus Normalization & Chunking

| Statistic | Result |
|---|---:|
| Markdown documents | **4,419** |
| Topic documents | **4,379** |
| Level guides | **40** |
| Domains | **10** |
| Topic records | **4,419** |
| Chunks | **4,492** |

Chunking:
- Target ≈ 400 tokens
- Maximum ≈ 600 tokens
- Minimum ≈ 30 tokens
- Approximate regex token counting
- 50-token overlap only intended for oversized sections
- Actual production overlap = 0

Preservation:

| Metric | Result |
|---|---:|
| Meaningful blocks | **18,697** |
| Approx-token coverage | **128,263 / 128,263** |
| Content preservation | **100%** |

Chunk distribution:
- Tiny chunks: **3,446 / 4,492 = 76.71%**

Duplicate analysis:

| Type | Groups | Members | Rate |
|---|---:|---:|---:|
| Exact duplicates | 673 | 1,533 | **34.13%** |
| Near duplicates | 6 | 15 | **0.33%** |

Duplicates were labelled, not removed.

Corpus version:
`m3.v1.d84a13e2ae63`

Canonical corpus hash:
`66e0ad89af04207d0a21ead62d35d9143197b162ecdf5d8e0b3b41928e3ec665`

Incremental simulations:
- modify: PASS
- add: PASS
- delete: PASS

---

# 5. M4 — Embedding & Vector Retrieval

Embedding:
- Vertex AI
- `gemini-embedding-001`
- 768 dimensions
- Documents: `RETRIEVAL_DOCUMENT`
- Queries: `RETRIEVAL_QUERY`

Vector corpus:

| Data | Count |
|---|---:|
| Enriched vectors | **4,492** |
| Content-only vectors | **4,492** |

Storage:
- Firestore
- Collection: `fipilot_m4_knowledge_vectors`
- Similarity: COSINE
- Index: 768D flat cosine
- Firestore records: **4,492**

M1 controlled retrieval with vector:
- Vector MRR = **0.8967**
- Lexical MRR = **0.9117**

Paraphrase stress dataset: **50 queries**

| Metric | Lexical | Vector |
|---|---:|---:|
| Hit@5 | **0.44** | **0.98** |
| MRR | **0.2467** | **0.8087** |

Firestore/local parity: **1.0**

Latency:

| Stage | Latency |
|---|---:|
| Local vector search | **~2 ms** |
| Firestore vector search | **~717 ms** |
| One cold-ish E2E sample | **~19.98 s** |
| Embedding portion in that sample | **~19.3 s** |

M4 Vertex cost: **~$0.0623**

Production remained lexical; vector remained shadow-only.

---

# 6. M5 — Retrieval Benchmark & Hybrid Decision

Datasets:
- Development = **72**
- Holdout = **48**

Retrieval modes:
- Lexical
- Vector
- Hybrid

Hybrid:
- RRF
- k = 60
- lexical weight = 0.75
- vector weight = 1.0

## 6.1 Development

| Metric | Lexical | Vector | Hybrid |
|---|---:|---:|---:|
| Hit@1 | 0.5694 | 0.9028 | **0.9306** |
| Hit@5 | 0.6667 | 0.9722 | **1.0000** |
| Recall@5 | 0.6528 | 0.9583 | **0.9861** |
| Precision@5 | 0.1389 | 0.2000 | **0.2056** |
| MRR | 0.6181 | 0.9357 | **0.9630** |

## 6.2 Holdout

| Metric | Lexical | Vector | Hybrid |
|---|---:|---:|---:|
| Hit@1 | 0.6458 | 0.9167 | **0.9375** |
| Hit@5 | 0.6667 | **1.0000** | **1.0000** |
| Recall@5 | 0.6667 | **1.0000** | **1.0000** |
| Precision@5 | 0.1417 | **0.2083** | **0.2083** |
| MRR | 0.6563 | 0.9531 | **0.9688** |

Headline:
- Lexical MRR = **0.6563**
- Vector MRR = **0.9531**
- Hybrid MRR = **0.9688**
- Hybrid improvement over Vector ≈ **+0.0157 MRR**

## 6.3 Paraphrase Stress Preservation

| Method | MRR |
|---|---:|
| Lexical | **0.2607** |
| Vector | **0.8087** |
| Hybrid | **0.7537** |

## 6.4 Compatibility Regression

| Method | MRR |
|---|---:|
| Original lexical | **0.9117** |
| Strict Vector | **0.0000** |
| Strict Hybrid | **0.4690** |

Root cause: foundational records with `level = unspecified` were excluded by strict level filtering.

Decision:
`INSUFFICIENT_EVIDENCE`

Production lexical remained unchanged.

## 6.5 Latency & Cost

| Component | Latency |
|---|---:|
| Lexical | **5.91 ms** |
| Local vector search | **1.99 ms** |
| Query embedding | **~496 ms** |
| Firestore | **~635 ms** |
| Vector E2E warm | **~1,132 ms** |
| Hybrid parallel | **~1,120 ms** |
| Cold E2E | **~2,267 ms** |

Warm samples: **40**, failures = **0**

Cost: **~$0.001518**

---

# 7. M6 — Question Generation Quality & RAG Impact

Dataset:
- 80 cases
- Development = 48
- Holdout = 32
- 10 domains
- 4 levels
- English = 60
- Vietnamese = 20
- Holdout = English-only

Conditions:
- No RAG
- Lexical
- Vector
- Hybrid

Question model:
- `gemini-2.5-flash`
- temperature = 0.2

Judge:
- `gemini-2.5-pro`
- temperature = 0

## 7.1 Development

Technical validity: **97.92%** for all conditions.

Specificity:

| Condition | Score |
|---|---:|
| No RAG | 1.8750 |
| Lexical | 1.9375 |
| Vector | 1.9375 |
| Hybrid | **1.9792** |

Grounding:

| Retrieval | Score |
|---|---:|
| Lexical | 0.4375 |
| Vector | **1.5000** |
| Hybrid | 1.4375 |

Knowledge utilization:

| Retrieval | Result |
|---|---:|
| Lexical | **25.00%** |
| Vector | **91.67%** |
| Hybrid | **89.58%** |

## 7.2 Holdout

| Metric | No RAG | Lexical | Vector | Hybrid |
|---|---:|---:|---:|---:|
| Technical validity | 1.0000 | 1.0000 | 0.9688 | 0.9688 |
| Role relevance | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| CV alignment | 1.0000 | 1.0000 | 1.0000 | 0.9688 |
| Difficulty exact | 0.8750 | **0.9375** | 0.9062 | 0.9062 |
| Specificity | 1.875 | 1.875 | **1.9375** | 1.875 |
| Candidate hallucination | 0% | 0% | 0% | 0% |
| Grounding | N/A | 1.6562 | **1.8750** | 1.6875 |
| Utilization | N/A | **1.0000** | **1.0000** | 0.9688 |

Headline:
- Vector grounding = **1.875 / 2**
- Candidate hallucination = **0%**
- Technical validity = **96.88%**

## 7.3 Lexical → Vector Effect

- Grounding: **+0.2188**
  - 95% CI ≈ `[+0.0938, +0.375]`
- Technical validity: **-0.0312**
  - CI includes 0
- Specificity: **+0.0625**
  - CI crosses 0

Interpretation: vector improves grounding clearly, but does not prove an overall downstream question-quality win.

## 7.4 Lexical-Miss / Vector-Hit Slice

Development subset: **N = 16**

- Grounding: **0.125 → 1.250**
- Utilization: **0.125 → 0.8125**

## 7.5 Pairwise Preference

| Comparison | First | Second | Tie |
|---|---:|---:|---:|
| NoRAG vs Lexical | 7 | 10 | 15 |
| NoRAG vs Vector | 7 | 10 | 15 |
| NoRAG vs Hybrid | 11 | 8 | 13 |
| Lexical vs Vector | 7 | 7 | 18 |
| Lexical vs Hybrid | 13 | 9 | 10 |
| Vector vs Hybrid | 12 | 8 | 12 |

Decision:
- Question Generation: **ACCEPTABLE**
- RAG activation: **INSUFFICIENT_EVIDENCE**

Production remained Lexical Top-K8.

## 7.6 Latency & Cost

| Condition | Mean total latency |
|---|---:|
| No RAG | **3,046 ms** |
| Lexical | **3,346 ms** |
| Vector | **3,554 ms** |
| Hybrid | **3,562 ms** |

M6 evaluation cost: **$2.4959**

---

# 8. M7 — Answer Evaluation Quality & RAGAS-Based Validation

Dataset:
- 20 question groups
- 80 answers
- Development = 12 groups / 48 answers
- Holdout = 8 groups / 32 answers
- 10 domains
- 4 levels

Reference construction:
`M3 provenance + expected concepts + canonical reference answer + critical errors`

Framework:
- RAGAS 0.4.3
- AnswerCorrectness
- InstanceSpecificRubrics
- Faithfulness
- FactualCorrectness
- AspectCritic

Judge:
- `gemini-2.5-pro`

Embedding:
- `gemini-embedding-001`

## 8.1 Reference Quality

| Metric | Result |
|---|---:|
| Pairwise ordering | **1.00** |
| Strict monotonicity | **1.00** |

## 8.2 Text Evaluator

Production:
- `gemini-2.5-pro`
- temperature = 0.1

| Metric | Result |
|---|---:|
| MAE | **1.298** |
| Spearman | **0.954** |
| Pairwise ordering | **95.83%** |
| Strict monotonicity | **75.00%** |
| Critical-error detection | **87.50%** |
| Unsupported feedback | **9.38%** |

Interpretation:
- Ranking/correlation is strong.
- Absolute calibration and critical-error handling still have limitations.

## 8.3 Voice Evaluator

Production:
- `gemini-2.5-flash`
- temperature = 0.1

| Metric | Result |
|---|---:|
| MAE | **1.244** |
| Spearman | **0.889** |
| Pairwise ordering | **89.58%** |
| Strict monotonicity | **37.50%** |
| Critical-error detection | **87.50%** |
| Unsupported feedback | **12.50%** |

## 8.4 Text vs Voice

| Metric | Result |
|---|---:|
| Mean score difference | **0.959** |
| Material disagreement | **12.50%** |

## 8.5 M7 Decision

Do NOT state:
`Answer Evaluator accuracy = 95%`

Safe statement:
`Text evaluator achieved Spearman correlation 0.954 against the automated reference benchmark.`

Production score trust:
**LOW**

Known limitations:
- critical error handling
- strict monotonicity
- feedback support
- Text/Voice consistency
- no expert human ground truth

## 8.6 Cost

- Dry estimate: **$3.1738**
- Conservative execution estimate: **$4.594866**
- Budget: **< $6**
- Exact provider invoice: **unavailable**

---

# 9. Evidence Classification

| Milestone | Evidence Type |
|---|---|
| M1 Resume | Synthetic-controlled |
| M1 Retrieval | Controlled catalog-backed |
| M1 Question | LLM-as-judge / synthetic |
| M1 Answer | Synthetic-controlled |
| M2 Resume | Controlled fixtures |
| M3 Corpus | Deterministic corpus audit |
| M4 Retrieval | Controlled + paraphrase stress |
| M5 Retrieval | Synthetic-controlled Dev/Holdout |
| M6 Question | LLM-as-judge + controlled |
| M7 Answer | Automated reference-based / RAGAS |

Expert-human ground truth:
**NOT AVAILABLE**

Do not convert these metrics into:
- human accuracy
- expert accuracy
- production accuracy

---

# 10. Defense Slide Metrics — Recommended 10

| # | Metric | Value |
|---|---|---:|
| 1 | Resume overall F1 | **98.53%** |
| 2 | Experience F1 | **100%** |
| 3 | OCR scan success | **100% (6/6)** |
| 4 | Corpus preservation | **100%** |
| 5 | Vector paraphrase Hit@5 | **98%** |
| 6 | Vector holdout MRR | **0.9531** |
| 7 | Question technical validity | **96.88–100%** |
| 8 | Candidate hallucination | **0%** |
| 9 | Text evaluator Spearman | **0.954** |
| 10 | Voice evaluator Spearman | **0.889** |

Optional if space:
- Vector grounding = **1.875 / 2**
- Text MAE = **1.298**
- Voice MAE = **1.244**

---

# 11. Evaluation Story for Defense

```text
M1
Baseline established
    ↓
M2
Resume F1 94.78% → 98.53%
    ↓
M3
4,419 docs → 4,492 deterministic chunks
100% preserved
    ↓
M4
Semantic vector retrieval introduced
Paraphrase Hit@5 44% → 98%
    ↓
M5
Vector holdout MRR 0.9531
but production activation intentionally withheld
    ↓
M6
Vector improves question grounding
without clear overall downstream-quality win
    ↓
M7
Answer evaluator correlation measured
Text ρ=.954
Voice ρ=.889
remaining calibration limitations documented
```

---

# 12. Primary Evaluation Scope / Status

```text
M1 CLOSED
M2 CLOSED
M3 CLOSED
M4 CLOSED
M5 CLOSED
M6 CLOSED
M7 CLOSED
```

Optimization experiments:
```text
M7.1 PARTIAL — not activated
M7.2 PARTIAL — not activated
```

Primary defense scope:
```text
M1–M7
```

M8:
```text
excluded from primary defense evaluation scope
```

---

# 13. Production Model / Retrieval Snapshot

| Component | Production / Evaluation Configuration |
|---|---|
| Resume extraction | `gemini-2.5-flash-lite`, temp 0.1 |
| Production retrieval | Weighted lexical, Top-K 8 |
| Question generation | `gemini-2.5-flash`, temp 0.2 |
| Text answer evaluation | `gemini-2.5-pro`, temp 0.1 |
| Voice answer evaluation | `gemini-2.5-flash`, temp 0.1 |
| Final report | `gemini-2.5-pro`, temp 0.1 |
| Shadow embedding evaluation | `gemini-embedding-001`, 768D |
| Vector store (shadow) | Firestore cosine index |

---

# 14. Defense Safety Notes

Use:
- "controlled evaluation"
- "automated reference-based evaluation"
- "LLM-as-judge"
- "synthetic-controlled dataset"

Avoid:
- "95% AI accuracy"
- "human-level accuracy"
- "expert validated"
- "production accuracy"

unless such evidence is actually available.
