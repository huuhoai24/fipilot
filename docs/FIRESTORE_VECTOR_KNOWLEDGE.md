# Firestore Vector Interview Knowledge

FiPilot has an opt-in Firestore Vector Search adapter behind the existing
`KnowledgeRetriever` interface. The local lexical adapter remains the default,
so creating or refreshing the vector collection does not change interview
behavior until `INTERVIEW_KNOWLEDGE_BACKEND=firestore_vector` is configured.

## Configuration

| Setting | Value |
| --- | --- |
| Embedding model | Vertex AI `gemini-embedding-001` |
| Embedding task types | `RETRIEVAL_DOCUMENT` for catalog chunks; `RETRIEVAL_QUERY` for interview queries |
| Output dimensions | `768` |
| Firestore database | `(default)` |
| Collection | `interview_knowledge_chunks` |
| Vector field | `embedding` |
| Index type | `flat` |
| Distance measure | `COSINE` |
| Top-K | `5` |

The full Gemini embedding is 3,072 dimensions, while Firestore accepts at most
2,048 dimensions. FiPilot requests 768 dimensions to fit the index and reduce
storage. Query text deliberately excludes the candidate name and contains only
the target role, level, language, specialization, skills, and objective.

Primary references:

- [Firestore vector search](https://firebase.google.com/docs/firestore/vector-search)
- [Vertex AI text embeddings](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/get-text-embeddings)
- [Vertex embedding task types](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings/task-types)

## Provision the index

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup_firestore_vector_index.ps1 `
  -ProjectId <google-cloud-project>
```

The index can take several minutes to become `READY`:

```powershell
gcloud firestore indexes composite list `
  --project=<google-cloud-project> `
  --database="(default)"
```

## Index the packaged catalog

Dry-run first, from `backend/`:

```powershell
.\.venv\Scripts\python.exe -m scripts.index_interview_knowledge_vectors `
  --project <google-cloud-project>
```

Apply:

```powershell
.\.venv\Scripts\python.exe -m scripts.index_interview_knowledge_vectors `
  --project <google-cloud-project> `
  --workers 8 `
  --apply
```

The sync is idempotent. It compares the catalog content hash, embedding model,
and dimensions, then embeds and writes only missing or changed chunks. Writes
commit in batches of 100, so rerunning after an interruption resumes safely.

## Enable the adapter

Add these variables to the backend deployment only after the index and catalog
have been verified:

```text
INTERVIEW_KNOWLEDGE_BACKEND=firestore_vector
INTERVIEW_KNOWLEDGE_COLLECTION=interview_knowledge_chunks
INTERVIEW_KNOWLEDGE_VECTOR_FIELD=embedding
INTERVIEW_KNOWLEDGE_EMBEDDING_MODEL=gemini-embedding-001
INTERVIEW_KNOWLEDGE_EMBEDDING_LOCATION=global
INTERVIEW_KNOWLEDGE_EMBEDDING_DIMENSIONS=768
INTERVIEW_KNOWLEDGE_TOP_K=5
```

Rollback is configuration-only: set `INTERVIEW_KNOWLEDGE_BACKEND=local` and
redeploy. The Firestore collection can remain populated without affecting the
local retriever.

## Provisioning evidence — 2026-08-15

- Project: `project-7dffc340-f73f-4e62-aec`
- Database: `(default)`, Firestore Native, `us-central1`
- Vector index ID: `CICAgOjXh4EK`, state `READY`
- Indexed documents: `4,379`
- Model/dimensions confirmed from a stored document:
  `gemini-embedding-001` / `768`
- Vietnamese Backend/JWT/OAuth smoke query: 5 results
- Measured end-to-end query latency: approximately `5.6 s`, including the
  online query-embedding request and Firestore KNN search

This provisioning record proves the collection and index existed at the stated
time. It is not a retrieval-quality benchmark and does not prove the deployed
Cloud Run service has enabled the vector adapter.
