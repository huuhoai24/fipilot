# M0 Retrieval, RAG, and Knowledge Base Audit

## Verdict

The configured local baseline performs **retrieval-augmented interview
planning with deterministic lexical/token-overlap retrieval**. It is not
semantic vector retrieval.

The dirty working tree also contains a real, opt-in Firestore vector adapter
using Vertex embeddings. It is wired through dependency injection but remains
disabled because `backend/.env.local` does not set
`INTERVIEW_KNOWLEDGE_BACKEND=firestore_vector`. The presence or population of
the remote collection was not inferred from source and was not queried.

Question generation does not receive retrieved records directly. Retrieved
strings influence the `InterviewPlan`; one resulting round is then passed to
the Question Generator. Answer evaluation and report generation do not perform
knowledge retrieval.

## Active local retrieval

| Property | Actual implementation |
| --- | --- |
| Source | `backend/services/interview_knowledge/catalog.json` |
| Entry point | `LocalKnowledgeRetriever.retrieve_topics` in `local.py:78` |
| Query construction | Recursively collect every string value from `CandidateProfile.model_dump`; join into one profile string |
| Tokenizer | Regex `[a-z0-9+#.]+`, lowercase; remove configured stop words and tokens shorter than 2 |
| Domain selection | +20 for exact domain label occurrence; +3 per overlap with static domain terms; sort by score descending then domain key |
| Candidate filter | Only records under the one selected domain |
| Topic score | 3 per overlapping token of length ≥5, otherwise 1; +12 when the complete title occurs in profile text |
| Threshold | Score must be greater than 0 |
| Top-K | `topic_limit=8` topics by default |
| Output | Domain string; optional level-guidance string; then up to 8 path/title/anchor strings |
| Similarity | No vector similarity. The internal value is a weighted lexical score |
| Embedding | **NOT USED** |
| Vector DB | **NOT USED** |
| Metadata filtering | Selected domain acts as a hard in-memory partition; experience level selects separate guidance |
| Reranking | **NOT IMPLEMENTED** beyond the initial deterministic score sort |
| Hybrid search | **NOT IMPLEMENTED** |
| External call | None |
| Determinism | Yes for identical profile, config, catalog, and code |

Tie-breaking is deterministic by lowercased title for topics and domain key for
domains. If there is no positive domain evidence, alphabetical tie-breaking
still selects one available domain rather than returning no domain. Topic
results can be empty, but the domain context is always returned if the catalog
contains a domain.

Although the runtime settings object contains `interview_knowledge_top_k=5`,
that setting is used only by the Firestore adapter. The active local retriever
uses its constructor default of 8.

## Optional Firestore vector retrieval

| Property | Implemented configuration |
| --- | --- |
| Adapter | `FirestoreVectorKnowledgeRetriever` in `infrastructure/interview_knowledge/firestore_vector.py:116` |
| Vector database | Cloud Firestore Vector Search |
| Collection | `interview_knowledge_chunks` by default |
| Vector field | `embedding` by default |
| Schema version | `1` in indexed documents |
| Embedding provider/model | Vertex AI `gemini-embedding-001` |
| Dimension | 768 by default, configurable 1–2048 |
| Document task type | `RETRIEVAL_DOCUMENT`, with title |
| Query task type | `RETRIEVAL_QUERY` |
| Distance metric | Firestore `COSINE` |
| Displayed similarity | Clamped `1 - vector_distance` |
| Top-K | 5 by default/configured setting |
| Query fields | recent role or specialization fallback, experience level, language, specialization, skills, objective; name/candidate ID omitted |
| Metadata filter | **NOT IMPLEMENTED** |
| Similarity threshold | **NOT IMPLEMENTED** |
| Reranking | **NOT IMPLEMENTED** |
| Hybrid/lexical fallback | **NOT IMPLEMENTED** |
| Query timeout | No application-level timeout |
| Embedding retry | 3 attempts with blocking exponential backoff; all exceptions retried |
| Retrieval failure | Propagates; no automatic switch to local lexical retrieval |

Firestore documents contain:

- `schema_version`
- `topic_id`
- `domain_key`
- `domain_label`
- `path`
- `title`
- `anchors`
- `content`
- `content_sha256`
- `embedding_model`
- `embedding_dimensions`
- configured vector field
- server `updated_at`

The indexer skips unchanged documents when content hash, model, and dimensions
match. It does not delete remote documents that were removed from the local
catalog. Indexing is a manual CLI/PowerShell operation and requires `--apply`.

## Chunking strategy

### Local catalog

There is no runtime text chunker. Each source Markdown file becomes one catalog
topic record. The catalog builder retains only:

- the first `# ` heading (or filename as title);
- cleaned directory path components;
- at most the first 8 bullet lines, each truncated to 240 characters.

All other Markdown content is omitted. No token count, token-aware size,
overlap, paragraph splitting, or tokenizer is used.

### Vector adapter

`build_catalog_chunks` maps exactly one catalog topic to exactly one vector
document. Content is a short synthesized string containing role, topic path,
and all retained anchors. There is no overlap and no token-based chunk size.
`document_id` is the first 32 hex characters of SHA-256(topic ID), while the
full content receives a SHA-256 hash.

## Knowledge base inventory

| Property | Audit result |
| --- | --- |
| Authoring source | `Knowledge/Domains/**/*.md` and `Knowledge/Levels/**/*.md` |
| Packaged runtime source | `backend/services/interview_knowledge/catalog.json` |
| Domains | 10 |
| Topic records / domain Markdown files | 4,379 |
| Level files | 40: Intern, Junior, Middle, Senior for 10 domains |
| Record schema | `title: str`, `path: list[str]`, `anchors: list[str]` |
| Catalog version | Integer `1` |
| Expected concepts | No formal field. `anchors` are guidance, not labelled expected-answer concepts |
| Answer rubric | **NOT IMPLEMENTED** |
| Per-record source/reference | **NOT IMPLEMENTED** |
| Per-record content hash | Not in base catalog; derived only for optional vector documents |
| Duplicate detection | **NOT IMPLEMENTED** |
| Automatic update pipeline | **NOT IMPLEMENTED** |
| Ingestion pipeline | Manual `build_interview_knowledge_catalog.py`; optional manual vector indexer |

Domain record counts:

| Domain | Records |
| --- | ---: |
| AI Engineer | 531 |
| Backend Developer | 728 |
| Business Analyst | 260 |
| Data Engineer | 384 |
| Data Scientist | 434 |
| DevOps Engineer | 509 |
| Full Stack Developer | 394 |
| Software Engineer | 642 |
| Tester / QA / QC | 124 |
| Web Developer | 373 |
| **Total** | **4,379** |

## Knowledge update behavior

1. Edit Markdown under `Knowledge/`.
2. Manually run `backend/scripts/build_interview_knowledge_catalog.py` to
   replace the packaged catalog.
3. For local retrieval, restart the application or clear/reconstruct the cached
   retriever because the JSON is loaded in `LocalKnowledgeRetriever.__init__`.
4. For vector retrieval, manually run
   `backend/scripts/index_interview_knowledge_vectors.py --apply` and ensure the
   Firestore vector index exists. Running application processes need no restart
   after collection updates because each query reads Firestore, but removed
   local records require separate remote cleanup that the current indexer does
   not perform.

## Evaluation status

- The 2026-08-15 RAGAS-style pilot ran the local lexical retriever on 10
  synthetic controlled cases and preserved sample-level JSONL.
- It reported controlled HitRate/Recall/MRR@8 of 1.0 and deterministic latency,
  but these cases were constructed from catalog metadata and are not a
  human-labelled production retrieval benchmark.
- Its reference-free context judgments use an LLM judge. Reference-based
  context recall was explicitly not evaluated.
- The pilot targets commit `1249cc50…`, not the audited dirty filesystem.
- The Firestore vector adapter has contract/unit tests, but no checked-in
  labelled Top-K quality result or proof of a populated remote index.

Therefore the active retrieval algorithm is reproducible as code, while its
production relevance/accuracy is **NOT EVALUATED** with verified ground truth.
