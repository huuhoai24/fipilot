# M6 RAG Impact (150 Holdout Sample Evaluation)

| Metric | No RAG | Lexical | Vector (`pgvector`) | Hybrid |
|---|---:|---:|---:|---:|
| Sample Size | 150 | 150 | 150 | 150 |
| Technical validity | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Role relevance | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| CV alignment | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Difficulty exact | 0.8200 | 0.9133 | 1.0000 | 1.0000 |
| Specificity (0–2) | 1.4800 | 1.8500 | 2.0000 | 2.0000 |
| Hallucination | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Grounding (0–2) | N/A | 1.7200 | 2.0000 | 2.0000 |
| Retrieval utilization | N/A | 0.9067 | 0.9400 | 0.9400 |

* Chi tiết báo cáo đầy đủ: [`docs/evaluation/cv_question_rag/RAG_ABLATION_BENCHMARK_150.md`](../cv_question_rag/RAG_ABLATION_BENCHMARK_150.md)
