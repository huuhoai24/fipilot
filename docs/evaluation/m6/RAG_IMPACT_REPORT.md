# M6 RAG Impact

| Metric | No RAG | Lexical | Vector | Hybrid |
|---|---:|---:|---:|---:|
| Technical validity | 1.0000 | 1.0000 | 0.9688 | 0.9688 |
| Role relevance | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| CV alignment | 1.0000 | 1.0000 | 1.0000 | 0.9688 |
| Difficulty exact | 0.8750 | 0.9375 | 0.9062 | 0.9062 |
| Specificity (0–2) | 1.8750 | 1.8750 | 1.9375 | 1.8750 |
| Hallucination | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Grounding (0–2) | N/A | 1.6562 | 1.8750 | 1.6875 |
| Retrieval utilization | N/A | 1.0000 | 1.0000 | 0.9688 |

Retrieval→question matrix: `{"A": 93, "B": 3, "C": 0, "D": 0, "n": 96}`.

Lexical-miss/vector-hit n=16. Vector recommendation: **INSUFFICIENT_EVIDENCE**. Correlations are directional because n=32.
