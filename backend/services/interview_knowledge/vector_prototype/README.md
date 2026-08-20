# FAKE Vector Retrieval Prototype — throwaway only

This folder answers one question: **would a semantic Top-K retrieval result be
easy to inspect before FiPilot replaces its current lexical retriever?**

It is intentionally fake and is not imported by the production application.
The terminal demo uses a tiny deterministic in-memory embedding so it runs
without credentials, network access, a model download, or persisted data.

## Proposed production-shaped configuration

| Setting | Choice |
| --- | --- |
| Embedding model | Vertex AI `gemini-embedding-001` |
| Output dimensionality | `768` |
| Vector database | Cloud Firestore Vector Search |
| Collection | `interview_knowledge_chunks` |
| Vector field | `embedding` |
| Top-K | `5` |
| Similarity metric | `COSINE` |
| Displayed score | `1 - cosine_distance` |

Why this shape:

- FiPilot already uses Google Cloud and Firestore, so this does not propose a
  second database service.
- `gemini-embedding-001` is the target multilingual/code embedding model; the
  768-dimensional output keeps the vector below Firestore's index limit and
  reduces storage compared with the model's full 3072 dimensions.
- Top-K 5 provides a small context window for question generation. It is an
  initial retrieval setting, not a measured optimum.
- Cosine distance is explicit and safe even if vector normalization changes.

## Run

From `backend/`:

```powershell
.\.venv\Scripts\python.exe -m services.interview_knowledge.fake_vector_prototype
```

Enter a free-form query or press `1`, `2`, or `3` for a sample. The complete
configuration and ranked retrieval state are redrawn after every query.

## Important boundary

Production FiPilot still defaults to `LocalKnowledgeRetriever`, which performs
deterministic lexical overlap. A real opt-in Firestore adapter and indexing tool
now live outside this throwaway prototype; see
[`docs/FIRESTORE_VECTOR_KNOWLEDGE.md`](../../../../docs/FIRESTORE_VECTOR_KNOWLEDGE.md).
The deployed application must not be described as using vector retrieval until
its environment explicitly enables that adapter. Before broad production use,
evaluate Top-K and retrieval quality on an approved, labelled Vietnamese and
English interview dataset.
