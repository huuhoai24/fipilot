# M4 Vector Record Schema

The shadow record stores `chunk_id`, `topic_id`, canonical `content`, deterministic `embedding_text`, 768D `embedding`, `embedding_model`, `embedding_dimension`, `embedding_task_type`, `domain`, `level`, `topic`, `subtopic`, `content_type`, `title`, `source_path`, `source_heading`, inclusive line range, `content_hash`, `embedding_input_hash`, `corpus_version`, `schema_version`, `embedding_version`, `embedding_text_version`, and `cache_key`.

Firestore stores full content and embedding text because the M3 corpus is small and this makes live parity/provenance evidence independently inspectable. The collection contains knowledge only and no candidate PII.

Official provider evidence used for M4:

- `gemini-embedding-001` defaults to 3,072 dimensions and supports explicit output dimensionality.
- Retrieval uses `RETRIEVAL_DOCUMENT` and `RETRIEVAL_QUERY`; `SEMANTIC_SIMILARITY` is not intended for retrieval.
- The SDK supports a document title parameter, but it is disabled for correctly batched mixed-title inputs.
- Firestore supports flat vector indexes up to 2,048 dimensions and pre-filtered vector queries through composite indexes.
