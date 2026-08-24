# Architecture research evidence

## Scope and status rules

This note is a primary-source audit for architecture documentation. Runtime code is authoritative for current behavior; specifications describe intended behavior. It deliberately contains no diagrams.

- **IMPLEMENTED**: reachable active runtime code, an executable repository/evaluation tool, or checked-in deployment configuration confirms the behavior.
- **PARTIAL**: a runtime seam exists but does not satisfy the complete documented contract, or operational activation is not proven.
- **SPEC-PENDING**: the behavior is required by a checked-in specification/ADR but no active implementation was found.
- **UNKNOWN**: source/config exists, but current deployment or execution state cannot be established from the repository.

The active backend composition root is `backend/gateway/main.py`; `backend/main.py` only re-exports its `app` for deployment compatibility. The folders under `backend/app/` contain compatibility/older modules and tests and must not be used to infer a second active runtime. This is also not a LangGraph runtime: `backend/shared/schemas/graph_state.py` explicitly describes its graph-shaped contracts as compatibility-only, while `backend/orchestrator/` contains the active ordinary Python orchestration.

Workspace note: the audit includes currently visible worktree source. At audit time, substantial `evaluation/m1`-`m8`, `evaluation/defense_extension`, and corresponding `docs/evaluation` trees were untracked according to `git status`; treat them as workspace research evidence, not as proof that they belong to the committed production baseline.

## Executive runtime finding

| Area | Status | Current runtime truth | Primary evidence |
| --- | --- | --- | --- |
| Browser application | IMPLEMENTED | React/Vite SPA, protected interview/profile/report/history routes, centralized API client, Firebase client auth | `frontend/src/App.tsx` (`App`); `frontend/src/lib/api.ts` (`requestJsonResponse`, `uploadResume`); `frontend/src/lib/firebase.ts` |
| HTTP gateway | IMPLEMENTED | One FastAPI gateway includes resume, candidate profile, interview, report, auth, voice, health routers | `backend/gateway/main.py` (`app`, `lifespan`, router registration) |
| Resume document extraction | IMPLEMENTED | Synchronous PDF/DOCX validation and extraction; sparse/image PDF pages can use local RapidOCR | `backend/gateway/api/resume.py` (`upload_resume`); `backend/infrastructure/documents/pdf_service.py` (`DocumentService`); `backend/infrastructure/documents/ocr.py` (`RapidOCREngine`) |
| Candidate Profile extraction | IMPLEMENTED | Section-bounded Resume context is classified/extracted by Gemini into Pydantic output, then narrowly reconciled against source text | `backend/services/profile_scanner/agent.py` (`ResumeAgent.extract_profile_result`); `context.py` (`build_resume_context`); `verification.py` (`verify_and_reconcile_profile`) |
| Candidate Profile provenance | PARTIAL | Verification produces provenance records, but upload persists only the profile and does not return or persist those records | `backend/services/profile_scanner/agent.py` (`ResumeProcessingResult.provenance`); `backend/gateway/api/resume.py` (`upload_resume`) |
| Profile readiness | PARTIAL | Shared validator and GET response exist; `/interview/start` does not call the validator | `backend/services/candidate_profile/readiness.py` (`evaluate_interview_readiness`); `backend/gateway/api/candidate_profile.py`; absence in `backend/gateway/api/interview.py` |
| Interview planning | IMPLEMENTED | Planner uses persisted profile, config, and retrieved curated topic strings to generate a typed plan with Gemini | `backend/services/interview_planner/agent.py` (`InterviewPlannerAgent.create_plan`); `prompts.py` (`build_interview_planner_prompt`) |
| Question generation | IMPLEMENTED | Typed Gemini question generation from Candidate Profile + selected round + config; voice supports streamed JSON with reconstruction fallback | `backend/services/question_generator/agent.py`; `prompts.py`; `streaming_service.py` (`QuestionStreamingService.generate_question`) |
| Answer evaluation | IMPLEMENTED | Gemini produces a typed per-answer evaluation; deterministic decision logic chooses follow-up, harder question, or next planned topic | `backend/services/answer_evaluator/agent.py`; `backend/orchestrator/decision_service.py` (`InterviewDecisionService.decide`) |
| Interview report | PARTIAL | Completed sessions can generate and persist a typed Gemini report and sequential calls reuse it; report generation reloads the latest Candidate Profile instead of using only the session snapshot | `backend/services/report_generator/service.py` (`ReportService.generate_for_session`); `agent.py`; `prompts.py` |
| Local lexical knowledge retrieval | IMPLEMENTED | Default retriever uses deterministic token overlap, domain scoring, exact-title bonus, level guidance, and a packaged catalog; it is not BM25/TF-IDF | `backend/services/interview_knowledge/local.py` (`LocalKnowledgeRetriever`); `backend/core/settings.py` (`InterviewKnowledgeSettings.backend="local"`) |
| Firestore vector retrieval | PARTIAL | Opt-in source path embeds queries with Vertex and runs Firestore cosine KNN; a dated provisioning record exists, but the currently deployed adapter selection is not proven | `backend/infrastructure/interview_knowledge/firestore_vector.py`; `backend/core/dependencies.py` (`build_interview_knowledge_retriever`); `docs/FIRESTORE_VECTOR_KNOWLEDGE.md` |
| Production hybrid retrieval | SPEC-PENDING | No active hybrid retriever or runtime hybrid mode is wired. Hybrid/RRF code and comparisons belong to the offline research harness | `evaluation/m4/`; `evaluation/m5/`; no hybrid branch in `backend/core/dependencies.py` |
| A/B/C retrieval ablation | IMPLEMENTED (offline only) | Offline scripts reconstruct Profile Only, Lexical, and Vector conditions from frozen evaluation artifacts; this is not a production feature flag | `evaluation/defense_extension/e3_ablation_analysis.py` (`CONDITIONS`, `build_outputs`); `docs/evaluation/defense_extension/e3_ablation/` |
| Persistence | IMPLEMENTED | Config-selected SQLite or Firestore repositories implement a common interface for profiles, extraction artifacts, plans, sessions, answer claims, turns, and reports | `backend/infrastructure/repositories/base.py`; `sqlite.py`; `firestore.py`; `backend/core/dependencies.py` (`build_interview_repository`) |
| Upload idempotency/replacement workflow | SPEC-PENDING | Upload hashes content for extraction reuse, but has no `Idempotency-Key`, upload-operation/status resource, processing lease, replacement endpoint, or fenced generation | `backend/gateway/api/resume.py`; ADRs `0005`, `0007`, `0009`; `docs/RESUME_REVIEW_TESTING_SEAMS.md` |
| Deployment | IMPLEMENTED configuration; UNKNOWN live state | Backend image and Cloud Run deploy scripts exist; Firebase Hosting config exists; local Compose has frontend, gateway, and optional GPU speech service. Repository state cannot prove the current live revision/config | `backend/Dockerfile`; `backend/scripts/deploy-cloud-run.ps1`; `backend/scripts/deploy-cloud-run.sh`; `frontend/firebase.json`; `docker-compose.local.yml` |
| CI/CD automation | SPEC-PENDING | No checked-in `.github/workflows` were found. Deployment is script-driven and validation is local/manual | repository file inventory; `AGENTS.md`; deploy scripts above |

## Runtime composition and trust boundaries

### Entry points

| Entry point | Status | Behavior and dependencies | Evidence |
| --- | --- | --- | --- |
| `gateway.main:app` | IMPLEMENTED | Development entry point used by `scripts/run_backend.ps1` and local Compose | `scripts/run_backend.ps1`; `docker-compose.local.yml`; `backend/gateway/main.py` |
| `main:app` | IMPLEMENTED | Cloud/container compatibility alias to the same gateway app | `backend/main.py`; `backend/Dockerfile` (`CMD`) |
| Vite SPA | IMPLEMENTED | Development command `npm run dev`; production output generated by `npm run build:production` | `frontend/package.json`; `frontend/scripts/build-production.mjs`; `frontend/firebase.json` |
| Speech inference service | IMPLEMENTED, optional | Separate FastAPI process exposes health/readiness and a WebSocket inference endpoint; gateway can alternatively run speech models in-process | `backend/speech_service/main.py`; `backend/core/dependencies.py` (`get_audio_pipeline_factory`, `get_streaming_tts_service`); `backend/Dockerfile.speech` |
| Knowledge catalog builder/indexer | IMPLEMENTED tooling | Offline catalog builder scans `Knowledge/`; vector indexer embeds and upserts changed chunks only | `backend/scripts/build_interview_knowledge_catalog.py` (`build_catalog`); `backend/scripts/index_interview_knowledge_vectors.py` (`main`); `CatalogVectorIndexer.sync` |
| System evaluation runners | IMPLEMENTED tooling | The tracked backend runner covers CV, speech, question, evaluator, and voice seams; additional visible worktree runners cover retrieval and end-to-end research outside request-time business logic | `backend/scripts/run_system_evaluation.py`; `backend/services/system_evaluation/runner.py`; `evaluation/m1/` through `evaluation/m8/` |

### Authentication and ownership

- **IMPLEMENTED** — REST routes obtain `CurrentUser` from `get_current_user`; Firebase ID tokens are verified by `FirebaseAuthService` when auth is enabled. Local auth-off mode supplies `AUTH_DEV_USER_ID`. Evidence: `backend/core/dependencies.py` (`get_current_user`, `get_auth_service`), `backend/infrastructure/auth/firebase.py` (`FirebaseAuthService.verify_id_token`).
- **IMPLEMENTED** — repository operations accept `user_id` and ownership-scope candidate/session reads. Missing and foreign resources collapse to `None`/404 at the route boundary. Evidence: `backend/infrastructure/repositories/base.py`; `sqlite.py`; `firestore.py`; `backend/gateway/api/interview.py`, `report.py`, `candidate_profile.py`.
- **IMPLEMENTED** — voice WebSocket auth uses subprotocols (`firebase-auth`, token), origin allowlist, ownership/mode checks, and close codes. Evidence: `backend/gateway/api/voice.py` (`_firebase_token`, `_origin_is_allowed`, `voice_interview`).
- **PARTIAL** — sensitive resume/profile/answer data crosses the trust boundary to Vertex Gemini in Resume extraction, planning, question generation, evaluation, and reporting. Structured logs avoid directly logging prompts, but there is no repository evidence of data-loss-prevention, residency enforcement beyond configured locations, or a formal retention/deletion workflow. Evidence: agent prompt builders and `backend/infrastructure/llm/vertex_gemini.py`; `backend/core/logging.py`.

## Resume-to-profile evidence

### Upload and file lifecycle

1. **IMPLEMENTED** — `POST /api/v2/resume/upload` accepts one FastAPI `UploadFile`, performs an extension precheck (`pdf`, `docx`), copies to an OS temporary file, enforces a hardcoded 10 MiB maximum, hashes the bytes, and always deletes the temporary file in `finally`. Evidence: `backend/gateway/api/resume.py` (`upload_resume`, `MAX_RESUME_BYTES`, `ALLOWED_RESUME_EXTENSIONS`).
2. **IMPLEMENTED** — actual content is checked: PDF header, DOCX ZIP header and required members, declared MIME allowlist, encrypted PDF rejection, malformed container rejection, and a 50-character post-extraction minimum. Evidence: `backend/infrastructure/documents/pdf_service.py` (`DocumentService._validate_document`, `_extract_pdf`, `_extract_docx`).
3. **IMPLEMENTED** — PDF native extraction uses `pypdf`; sparse/image-only classification uses alphanumeric count/nonblank-page heuristics; low-text pages up to 20 are rendered with PyMuPDF and sent to lazy local RapidOCR with a document deadline. Partial warnings include parse/OCR failures, timeout, empty OCR, and page limit. Evidence: `backend/infrastructure/documents/quality.py` (`classify_text_quality`); `pdf_service.py` (`MAX_OCR_PAGES`, `_extract_pdf`, `_recognize_with_timeout`); `ocr.py`.
4. **IMPLEMENTED** — DOCX extraction uses `python-docx` paragraphs and table rows and caps expanded ZIP content at 50 MiB. Evidence: `DocumentService._extract_docx`, `MAX_DOCX_UNCOMPRESSED_BYTES`.
5. **PARTIAL** — the runtime OCR behavior contradicts ADR 0004/testing seams, which state OCR is not invoked and image-only PDF is rejected. For diagrams, show runtime OCR as implemented and annotate the spec mismatch; do not show the ADR behavior as current. Evidence: runtime sources above; `docs/adr/0004-resume-upload-and-partial-extraction-contract.md`; `docs/RESUME_REVIEW_TESTING_SEAMS.md`.
6. **SPEC-PENDING** — multipart cardinality is not explicitly parsed/rejected as `multiple_files_not_allowed`; there is no asynchronous worker/queue or upload-status endpoint. Extraction is in the request path. Evidence: the single `file: UploadFile = File(...)` signature and complete route body in `backend/gateway/api/resume.py`.

### Structured AI extraction

- **IMPLEMENTED** — `build_resume_context` splits recognized headings, retains complete text up to 16,000 characters, otherwise allocates section budgets with higher weight for experience/projects/skills and marks `content_omitted`. This is truncation-aware context selection, not embedding retrieval. Evidence: `backend/services/profile_scanner/context.py` (`DEFAULT_MAX_CONTEXT_CHARACTERS`, `split_resume_sections`, `build_resume_context`).
- **IMPLEMENTED** — `ResumeAgent.extract_raw` calls the resume-specific Gemini service with `ResumeExtractionResult`, temperature 0.1, no thinking, and `task_type="simple"`. The system prompt treats uploaded content as untrusted and rejects non-resume/unsupported-domain classifications below 0.7 confidence. Evidence: `backend/services/profile_scanner/agent.py`; `prompts.py`; `schemas.py`.
- **IMPLEMENTED** — `ResumeExtractionResult.to_candidate_profile` normalizes/limits the result into canonical Candidate Profile fields: name, years experience, recent role, specialization, skills, skill evidence, projects, experiences, and education. Evidence: `backend/services/profile_scanner/schemas.py`; canonical types in `backend/shared/schemas/candidate.py`.
- **PARTIAL** — post-LLM verification can repair/reject a narrow experience pattern and label identity/skill/experience support. It is not general claim verification, and the produced provenance is discarded at the upload boundary. Evidence: `backend/services/profile_scanner/verification.py` (`_EXPERIENCE_LINE`, `verify_and_reconcile_profile`); `backend/gateway/api/resume.py`.
- **IMPLEMENTED reuse, not upload idempotency** — in-process `ProcessedResumeCache` is owner/content/version keyed with one-hour TTL and 256-entry LRU behavior; the repository also stores an extraction artifact under the same hashed key. Every accepted request still creates a new candidate/profile even on an extraction cache hit. Evidence: `backend/services/profile_scanner/cache.py`; `upload_resume`; repository `get/save_resume_extraction_artifact`.

### Profile contract gaps

- **IMPLEMENTED** — `GET /api/v2/candidates/{candidate_id}/profile` returns the persisted profile, computed readiness, and a strong ETag containing `profile_version`. Evidence: `backend/gateway/api/candidate_profile.py` (`get_candidate_profile`).
- **IMPLEMENTED** — readiness uses NFKC normalization and requires a nonfallback name, skills, interviewable evidence, and no validity issue. Evidence: `backend/services/candidate_profile/normalization.py`; `readiness.py`.
- **SPEC-PENDING** — no active Profile PATCH route, strict correction allowlist, `If-Match` mutation, stale `412`, evidence IDs, audit events, replacement Resume route, or partial-extraction acknowledgement was found. Evidence: only GET is registered in `candidate_profile.py`; target contracts in ADRs `0001`, `0002`, `0007`, `0008`, `0009` and `docs/RESUME_REVIEW_TESTING_SEAMS.md`.
- **PARTIAL** — repositories expose `profile_version`, but current `save_candidate_profile` does not implement the target conditional compare-and-increment correction transaction. Evidence: `backend/models.py` (`User.profile_version`); `backend/infrastructure/repositories/sqlite.py` and `firestore.py` profile methods.

## Interview runtime evidence

### Preparation and planning

- **IMPLEMENTED** — `/api/v2/interview/prepare` reloads the owned persisted profile, keys a blueprint by owner/candidate/profile version/config, deduplicates same-process work in `InterviewPreparationCache`, checks persistent blueprint storage, and otherwise calls the planner. Evidence: `backend/gateway/api/interview.py` (`prepare_interview`, `_get_or_create_blueprint`); `backend/services/interview_preparation/service.py` (`InterviewPreparationCache`).
- **IMPLEMENTED** — default in-process preparation cache settings are 300 seconds and 128 entries; the persistent plan artifact survives process restart. Evidence: `backend/core/settings.py` (`DevelopmentSettings`); SQLite `InterviewBlueprintArtifact`; Firestore `interview_blueprints` subcollection.
- **IMPLEMENTED** — planner inputs are Candidate Profile, InterviewConfig, and curated topic strings. Output is `InterviewPlan` with duration, rounds, coverage goals, risk areas, and summary; each round has topic, objective, difficulty, reasoning, question areas, weight, target skills, and budget. Evidence: `backend/services/interview_planner/agent.py`; `backend/services/interview_planner/prompts.py`; `backend/shared/schemas/interview.py`.
- **PARTIAL** — `question_budget` and round `weight` are model fields, but runtime completion is governed primarily by `InterviewConfig.question_count` and plan index; do not imply a separate allocator/scheduler exists. Evidence: `backend/orchestrator/interview_orchestrator.py` (`submit_answer`); `backend/shared/schemas/interview.py`.

### Start and session snapshot

- **IMPLEMENTED** — `/api/v2/interview/start` accepts only `candidate_id` and `interview_config`, reloads the owned profile, obtains/creates a plan, generates the first planned question, and creates a session. Text mode then wraps the first planned question behind a deterministic introduction turn. Evidence: `backend/gateway/api/interview.py` (`InterviewStartRequest`, `start_interview`); `backend/orchestrator/interview_orchestrator.py` (`start_interview`); `conversation_flow.py` (`begin_text_conversation`).
- **PARTIAL** — profile content is embedded in `InterviewSessionState`, but session creation and state save are separate operations, and there is no explicit immutable `candidate_profile_version` field/transaction satisfying ADR 0007. The field is typed as base `CandidateProfile`, so the `PersistedCandidateProfile.profile_version` supplied at start is not a durable field of the serialized state contract. Evidence: `start_interview`, `_save_state`; `InterviewSessionState` in `backend/shared/schemas/interview.py`; ADR 0007.
- **SPEC-PENDING** — start does not enforce `evaluate_interview_readiness`; a direct caller can start an incomplete profile. Evidence: `backend/gateway/api/interview.py`; no readiness call in the route; ADR 0003.

### Turn lifecycle and adaptive logic

- **IMPLEMENTED** — text answer submission is idempotent per `(session_id, turn_id, SHA-256(answer))`: repository claim outcomes are claimed/replay/in-progress/conflict; successful state transition and claim completion share repository operations. Evidence: `backend/services/interview_answer_service.py` (`InterviewAnswerSubmissionService.submit_answer`); repository claim/complete methods.
- **IMPLEMENTED** — the evaluator prompt receives profile, question including expected points, answer, and config. It returns scores, strengths/weaknesses, missing topics/concepts, feedback, and follow-up decision. Voice uses the simple model/no thinking; text uses configured `EVALUATOR_TASK_TYPE` (default complex). Evidence: `backend/services/answer_evaluator/agent.py`; `prompts.py`; `backend/shared/schemas/evaluation.py`.
- **IMPLEMENTED** — decision order is follow-up first, then increase difficulty for score >= 8, else next planned topic. Follow-up selection ranks existing model-generated probe candidates by token overlap with evaluator feedback; it does not call a separate model. Evidence: `backend/orchestrator/decision_service.py`; `follow_up_service.py`.
- **IMPLEMENTED** — text mode can prefetch the next ordinary question while evaluation runs; failed evaluation discards the task. Voice mode maintains bounded structured memory and uses a streamed question provider. Evidence: `backend/orchestrator/interview_orchestrator.py` (`_prefetch_text_next_question`, `submit_answer`); `memory_service.py`; `backend/gateway/api/voice.py` (`stream_question`).
- **IMPLEMENTED** — completion occurs when completed turns reach `question_count`, decision says finish, or the plan has no next round. There is no separate durable workflow engine/queue. Evidence: `InterviewOrchestrator.submit_answer`.
- **PARTIAL** — enum values retain historical states, while active persistence writes `in_progress`/`completed` plus internal strings `INTERVIEWING`/`ENDED`; diagrams must not treat all enum members as active state transitions. Evidence: `backend/shared/schemas/interview.py` (`InterviewStatus`); `backend/gateway/api/interview.py` (`_save_state`); `InterviewAnswerSubmissionService`.

### Voice path

- **IMPLEMENTED** — voice shares `InterviewAnswerSubmissionService` through `VoiceAnswerSubmissionService`, so evaluation/decision/persistence are not a second interview engine. Evidence: `backend/services/voice_session/answer_service.py`.
- **IMPLEMENTED** — gateway manages WebSocket state, binary audio, VAD/STT transcripts, confirmation, streamed questions, TTS, barge-in, and latency events. Local adapters use Silero VAD, faster-whisper STT, and VieNeu TTS; remote adapters connect to the optional speech service. Evidence: `backend/gateway/api/voice.py`; `backend/services/voice_session/`; `backend/infrastructure/speech/`; `backend/core/dependencies.py`.
- **UNKNOWN** — source and tests prove the path exists, but this audit cannot prove GPU/model availability, current remote service health, real concurrent capacity, or currently deployed speech mode. Evidence: environment-selected `SPEECH_SERVICE_URL` and device/model settings in `backend/core/settings.py`.

### Report generation

- **IMPLEMENTED** — report generation requires session status completed/report_generated and no current turn; existing stored report is returned before another model call. Evidence: `backend/services/report_generator/service.py` (`generate_for_session`).
- **IMPLEMENTED** — Gemini receives profile, interview config, plan, and completed turns and returns a typed report with scores, narrative feedback, skills, recommendations, learning plan, recommendation enum, and confidence. Evidence: `backend/services/report_generator/prompts.py`; `schemas.py`; `agent.py`.
- **PARTIAL correctness risk** — `ReportService` reloads the candidate's latest profile even though completed session state contains its own profile snapshot. A later profile update could therefore influence the report prompt. Evidence: `ReportService.generate_for_session` calls `repository.get_candidate_profile` and then `agent.generate_report(profile, state)`.
- **PARTIAL concurrency** — sequential reuse is implemented, but the read-generate-save sequence has no explicit report-generation claim/lease; two simultaneous first requests may both call Gemini. Evidence: `ReportService.generate_for_session`; repository report methods.

## LLM, prompts, routing, and structured output

### Provider and model routing

| Operation | Status | Runtime model route | Prompt/output evidence |
| --- | --- | --- | --- |
| Resume classification/extraction | IMPLEMENTED | Separate Vertex client/settings: `GEMINI_RESUME_MODEL` default `gemini-2.5-flash-lite`, `GEMINI_RESUME_LOCATION` default `global`; one attempt | `core.dependencies.get_resume_llm_service`; `ResumeAgent.extract_raw`; `ResumeExtractionResult` |
| Interview planning | IMPLEMENTED | simple route, default `gemini-2.5-flash`; temperature 0.1, thinking 0 | `InterviewPlannerAgent.create_plan`; `InterviewPlan` |
| Question generation | IMPLEMENTED | simple route, default `gemini-2.5-flash`; temperature 0.2, thinking 0 | `QuestionGeneratorAgent.generate_question`; `InterviewQuestion` |
| Voice streamed question | IMPLEMENTED | simple route, thinking 0; streamed JSON then typed validation or metadata reconstruction | `QuestionStreamingService.generate_question` |
| Text answer evaluation | IMPLEMENTED | `EVALUATOR_TASK_TYPE`, default complex -> `gemini-2.5-pro` | `EvaluatorAgent.evaluate_answer`; `AnswerEvaluation` |
| Voice answer evaluation | IMPLEMENTED | forced simple route, thinking 0 | `EvaluatorAgent.evaluate_answer` |
| Final report | IMPLEMENTED | complex route, default `gemini-2.5-pro` | `ReportGeneratorAgent.generate_report`; `InterviewReport` |
| Embeddings | PARTIAL operationally | `gemini-embedding-001`, 768 dimensions by default, only when vector adapter/indexer is selected | `VertexTextEmbedder`; `InterviewKnowledgeSettings` |

- **IMPLEMENTED static routing** — `VertexGeminiService.route_model` maps `simple` and `complex` to configured names or uses an explicit model. There is no dynamic quality/cost/provider router and no non-Google LLM provider adapter in active code. Evidence: `backend/infrastructure/llm/vertex_gemini.py`; `backend/infrastructure/llm/base.py`.
- **IMPLEMENTED** — JSON operations use Vertex response schema, parse either `response.parsed` or extracted JSON text, validate with Pydantic, retry validation failures, and raise typed service errors. Default retry is three attempts with exponential backoff/jitter and 60-second timeout; Resume overrides to one attempt. Evidence: `VertexGeminiService.generate_json`, `_validate_json_text`, `_is_retryable_error`, `RetryConfig`; `get_resume_llm_service`.
- **PARTIAL repair behavior** — standard JSON calls retry invalid output but do not run a separate repair prompt. Voice streaming reconstructs metadata after the already-spoken question if tail validation fails. Evidence: `VertexGeminiService.generate_json`; `QuestionStreamingService._question_from_stream`.
- **IMPLEMENTED** — centralized `build_agent_prompt` assembles system instruction, language instruction, task, agent task, and JSON context. Major prompt builders live beside each agent: profile scanner, planner, question generator, evaluator, and report generator. Evidence: `backend/services/prompt_builder.py`; each `services/*/prompts.py` file.

## Retrieval and RAG evidence

### Production/default path

1. **IMPLEMENTED** — `INTERVIEW_KNOWLEDGE_BACKEND=local` is the default. `LocalKnowledgeRetriever.retrieve_topics` flattens the Candidate Profile, tokenizes it, selects one supported domain, adds level guidance, scores catalog topics by token overlap plus exact-title bonus, and returns at most eight topic strings. It does not return chunk IDs/scores and is not BM25. Evidence: `backend/services/interview_knowledge/local.py`.
   - **PARTIAL multilingual behavior** — local tokenization uses `[a-z0-9+#.]+`; Vietnamese diacritics are not normalized into equivalent ASCII tokens, so the lexical path's bilingual recall is not guaranteed. Evidence: `local.py` (`_tokens`).
2. **IMPLEMENTED** — planner calls retrieval synchronously, passes the resulting strings as `curated_knowledge`, and Gemini incorporates them into plan direction. Question generation receives the resulting `InterviewRound`, not raw retrieved documents. Evidence: `InterviewPlannerAgent.create_plan`; `build_interview_planner_prompt`; `QuestionGeneratorAgent.generate_question`.
3. **PARTIAL RAG traceability** — runtime plan/question schemas do not store retrieved chunk IDs, rank, query, or provenance. A question can be traced to a round and Candidate Profile, but not reliably to a knowledge chunk. Evidence: `backend/shared/schemas/interview.py`; local/vector retriever return type `list[str]`.
4. **SPEC-PENDING direct evaluator/report grounding** — answer evaluation and report prompts contain no retrieved knowledge/context input. They are grounded in profile/question/answer/evaluations only. Evidence: `build_evaluator_prompt`; `build_report_prompt`.
5. **PARTIAL failure handling** — no result simply gives the planner an empty list, but retriever exceptions are not caught to fall back from vector to local/profile-only. Evidence: `InterviewPlannerAgent.create_plan`; `build_interview_knowledge_retriever`.

### Knowledge ingestion

- **IMPLEMENTED** — source markdown under `Knowledge/Domains` and `Knowledge/Levels` is converted offline to `backend/services/interview_knowledge/catalog.json` containing domain topic path/title/anchors and level guidance. Evidence: `backend/scripts/build_interview_knowledge_catalog.py` (`build_catalog`).
- **IMPLEMENTED** — vector chunking is one deterministic topic record per catalog entry with SHA-256-derived document ID and content hash. This is not free-form document splitting or recursive semantic chunking. Evidence: `backend/services/interview_knowledge/chunks.py` (`KnowledgeChunk`, `build_catalog_chunks`).
- **IMPLEMENTED source** — vector indexing embeds documents as `RETRIEVAL_DOCUMENT`, skips unchanged hash/model/dimension records, and batch-upserts Firestore vectors and metadata. Evidence: `CatalogVectorIndexer.sync`; `backend/scripts/index_interview_knowledge_vectors.py`.
- **UNKNOWN operational freshness** — `docs/FIRESTORE_VECTOR_KNOWLEDGE.md` records a ready index and 4,379 documents on 2026-08-15, but repository evidence does not prove current index freshness or that the deployed gateway selects it.

### Vector request path

- **IMPLEMENTED source** — `build_vector_query_text` includes recent role/specialization, experience level, language, skills, and objective while omitting candidate identity. `VertexTextEmbedder.embed_query` uses `RETRIEVAL_QUERY`; Firestore `find_nearest` uses cosine distance and configured top-k (default 5). Evidence: `backend/infrastructure/interview_knowledge/firestore_vector.py`.
- **PARTIAL deployment confidence** — enabling the path requires Google project, Vertex access, Firestore collection, and a compatible vector index. Dependency construction fails rather than silently degrading when configuration/resources are absent. Evidence: `backend/core/dependencies.py` (`build_interview_knowledge_retriever`); `backend/core/startup.py`; `docs/FIRESTORE_VECTOR_KNOWLEDGE.md`.
- **SPEC-PENDING production hybrid/reranker/filtering** — no production lexical+vector fusion, cross-encoder reranker, minimum similarity threshold, or metadata filter is wired. Evidence: active retriever interface and composition root.

### Offline retrieval/evaluation boundary

- **IMPLEMENTED offline in the current worktree** — advanced research code under `evaluation/m3` builds/normalizes/deduplicates a corpus; `evaluation/m4` creates embeddings/vector stores; `evaluation/m5` benchmarks lexical, vector, and hybrid/RRF behavior. These modules are not imported by gateway/business code and were untracked at audit time. Evidence: `evaluation/m3/`, `evaluation/m4/`, `evaluation/m5/`; import search against `backend/gateway`, `backend/services`, `backend/orchestrator`; `git status --short`.
- **IMPLEMENTED offline** — E3 ablation declares `NO_RAG`, `LEXICAL`, and `VECTOR`, computes common quality, retrieval, grounding, utilization, latency, paired differences, and failure taxonomy from frozen M6 outputs. Evidence: `evaluation/defense_extension/e3_ablation_analysis.py` (`CONDITIONS`, `common_metrics`, `rag_metrics`, `paired_metric`, `failure_taxonomy`, `build_outputs`).
- **PARTIAL evidence quality** — workspace reports explicitly bound claims to synthetic/frozen slices and say human review is not evaluated. Vector research uses a research representation/index that does not by itself validate the opt-in production vector adapter. These report trees were untracked at audit time. Evidence: `docs/evaluation/defense_final/EVALUATION_MASTER_FINAL.md`; `LIMITATIONS.md`; `CLAIM_MATRIX.md`; `git status --short`.
- **IMPLEMENTED offline distinction** — grounding and knowledge utilization are separate: relevance checks whether expected knowledge was retrieved, while utilization/grounding checks whether the generated question used that context. Profile-only has RAG metrics marked not applicable. Evidence: `e3_ablation_analysis.py` (`rag_metrics`, `audit_case`, `failure_taxonomy`).

## Evaluation and observability evidence

### Evaluation frameworks visible in the audit

| Framework | Status | What it measures | Evidence |
| --- | --- | --- | --- |
| Backend system evaluation | IMPLEMENTED | CV skill/field accuracy and latency; STT WER/CER; TTS first-audio/generation ratios; question relevance/difficulty/CV alignment via Gemini judge; evaluator repeatability/MAE; voice latency P50/P95/failure | `backend/services/system_evaluation/runner.py`; `evaluators.py`; `judges.py`; `schemas.py`; `backend/scripts/run_system_evaluation.py` |
| M1-M6 Resume/RAG/question research | IMPLEMENTED offline in worktree | Datasets, corpus construction, retrieval quality/latency, vector shadow/parity, question-quality and A/B/C retrieval comparisons; trees were untracked at audit time | `evaluation/m1/` through `evaluation/m6/`; `docs/evaluation/m1/` through `m6/`; `git status --short` |
| M7/M7.1/M7.2 evaluator research | IMPLEMENTED offline in worktree | Reference signals, RAGAS-family metrics, score/feedback quality, calibration and gates; trees were untracked at audit time | `evaluation/m7/`, `m71/`, `m72/`; corresponding `docs/evaluation/` reports |
| M8 end-to-end harness | IMPLEMENTED offline in worktree; PARTIAL live proof | Scenario contracts, traces, invariants, provider cache/cost, offline and authorized-live evidence; explicit limitations still bound product-wide claims; tree was untracked at audit time | `evaluation/m8/`; `docs/evaluation/m8/`; `docs/evaluation/defense_final/LIMITATIONS.md` |

- **IMPLEMENTED** — `GeminiQuestionQualityJudge` is benchmark-only and is not in interview business logic. Evidence: `backend/services/system_evaluation/judges.py` class docstring and dependency use only in evaluation runner.
- **PARTIAL** — evaluation artifacts contain latency/cost/quality evidence for their frozen configurations, not continuously collected production SLOs. No always-on experiment assignment service or online A/B/C telemetry path was found.
- **IMPLEMENTED basic observability** — request correlation middleware, JSON stdout logging, redaction, stage timers, provider attempt records, token-usage capture when Vertex reports it, and voice latency registry exist. Evidence: `backend/core/middleware.py`; `core/logging.py`; `core/performance.py`; `VertexGeminiService`; `backend/services/voice_session/metrics.py`.
- **PARTIAL observability** — no OpenTelemetry exporter, distributed trace backend, metrics scrape endpoint, durable LLM trace store, or alert policy is configured in active source. Deployment docs rely on stdout/Cloud Logging. Evidence: dependency/config inventory; `backend/DEPLOYMENT.md`.

## Persistence and data ownership evidence

### Repository abstraction

- **IMPLEMENTED** — `InterviewRepository` combines candidate, session, turn, evaluation, and report contracts. Runtime chooses `sqlite` or `firestore` through `REPOSITORY_BACKEND`. Evidence: `backend/infrastructure/repositories/base.py`; `backend/core/dependencies.py` (`build_interview_repository`).
- **IMPLEMENTED SQLite** — SQLAlchemy tables include users/candidates, sessions, answer submissions, messages, evaluations, interview blueprint artifacts, and resume extraction artifacts. Candidate Profile and session state/report are JSON text fields. Evidence: `backend/models.py`; `backend/database.py`; `backend/infrastructure/repositories/sqlite.py`.
- **IMPLEMENTED Firestore** — owned documents live under user-scoped collections/subcollections for candidates, interviews, answer submissions, interview blueprints, and resume extractions; report data is stored with the interview. Evidence: `backend/infrastructure/repositories/firestore.py` (`_user_document`, collection helpers, report/profile/session methods).
- **IMPLEMENTED** — SQLite and Firestore both implement answer-submission claims and atomic completion of the claim plus session-state update at their repository boundary. Evidence: `claim_answer_submission` and `complete_answer_submission` in both repositories.
- **PARTIAL schema semantics** — SQLite legacy names (`User`, `Session`, `Message`) do not map one-to-one to current domain vocabulary; diagrams should name domain concepts and annotate physical tables rather than treating `User` as Firebase user identity. Evidence: `backend/models.py`; repository conversions.
- **PARTIAL schema evolution** — SQLite repository startup contains runtime schema-patching compatibility logic; no checked-in Alembic or equivalent migration system was found. Evidence: `backend/infrastructure/repositories/sqlite.py` schema compatibility methods; dependency inventory.

### Stored and transient data

| Data | Status | Storage/lifecycle evidence |
| --- | --- | --- |
| Uploaded file bytes | IMPLEMENTED transient | OS temp file in `upload_resume`, deleted in `finally`; no object storage implementation found |
| Raw extracted Resume text | IMPLEMENTED persistent | `save_candidate_resume_text`; SQLite `users.raw_resume_text`; Firestore candidate field |
| Candidate Profile/version | IMPLEMENTED persistent | SQLite `profile_json`/`profile_version`; Firestore candidate document |
| Extraction reuse artifact | IMPLEMENTED persistent + memory cache | SQLite `resume_extraction_artifacts`; Firestore `resume_extractions`; `ProcessedResumeCache` |
| Interview blueprint | IMPLEMENTED persistent + memory cache | SQLite `interview_blueprint_artifacts`; Firestore `interview_blueprints`; `InterviewPreparationCache` |
| Session snapshot/state | PARTIAL | JSON state includes profile/plan/turns; exact version/atomic snapshot contract missing |
| Answer claim | IMPLEMENTED persistent | unique SQLite `(session_id, turn_id)` row; Firestore answer-submission document/transaction |
| Turns/evaluations | IMPLEMENTED, denormalized | Current evaluated turns are in session state; repositories also expose turn/evaluation seams and legacy physical tables |
| Final report | IMPLEMENTED persistent | SQLite session `report_data`; Firestore interview `report` |
| Knowledge catalog | IMPLEMENTED packaged | `backend/services/interview_knowledge/catalog.json` generated from repository markdown |
| Knowledge vectors | PARTIAL operationally | External Firestore collection when provisioned; no local production vector database |
| Redis/cache server | SPEC-PENDING | No Redis dependency/config/runtime implementation found; caches are in-process or repository artifacts |
| Queue/background upload worker | SPEC-PENDING | No message broker/worker path found; upload and LLM extraction are synchronous request work |

## Configuration flow

- **IMPLEMENTED** — `Settings` maps environment variables into nested application, Google Cloud, LLM routing, database, development, speech, auth, CORS, repository, and interview-knowledge settings. Evidence: `backend/core/settings.py` (`Settings`, nested settings models, `get_settings`).
- **IMPLEMENTED** — `scripts/run_backend.ps1` explicitly loads `BACKEND_ENV_FILE` or `backend/.env.local` into the process and starts `gateway.main:app` with working directory `backend/`. Local Compose uses `backend/.env.local`; Cloud deploy scripts pass production env variables.
- **IMPORTANT / IMPLEMENTED config fact** — `backend/app/.env` is not referenced by the active repository helper, active Settings default (`.env` relative to the backend working directory), local Compose, or Cloud deploy scripts. It affects the active gateway only if another launcher explicitly loads it. Evidence: `scripts/run_backend.ps1`; `backend/core/settings.py` (`model_config`); `docker-compose.local.yml`.
- **IMPLEMENTED** — key routing flags are `GEMINI_SIMPLE_MODEL`, `GEMINI_COMPLEX_MODEL`, `GEMINI_RESUME_MODEL`, `GEMINI_RESUME_LOCATION`, `EVALUATOR_TASK_TYPE`, `REPOSITORY_BACKEND`, and `INTERVIEW_KNOWLEDGE_BACKEND`. Speech uses `SPEECH_SERVICE_URL` to select remote versus in-process adapters. Evidence: `backend/core/settings.py`; `backend/core/dependencies.py`.
- **PARTIAL** — settings comments still include future/temporary wording even though the active gateway uses them; architecture should follow imports/runtime, not those stale comments. Evidence: top-level docstrings in `backend/core/settings.py` and `backend/infrastructure/llm/base.py` versus `backend/gateway/main.py` and `core/dependencies.py`.
- **UNKNOWN** — do not record values from developer `.env` files in architecture docs. Repository examples define defaults, but secrets and the currently selected deployed values are not evidence suitable for checked-in documentation.

## Deployment evidence

### Local development

- **IMPLEMENTED** — PowerShell helper starts one Uvicorn gateway on configurable host/port after loading `backend/.env.local`. Frontend runs Vite separately. Evidence: `scripts/run_backend.ps1`; `frontend/package.json`.
- **IMPLEMENTED** — `docker-compose.local.yml` defines frontend (5173), backend gateway (8000), and GPU speech service (9000), with source volumes, health checks, and gateway `SPEECH_SERVICE_URL` pointing at speech service.
- **UNKNOWN capacity** — Compose topology does not prove production scaling, durability, or GPU availability.

### Cloud/production

- **IMPLEMENTED configuration** — `backend/Dockerfile` builds Python 3.12, installs app/speech dependencies, pre-caches faster-whisper, runs as a non-root user, and starts `main:app` on Cloud Run `PORT`. Evidence: `backend/Dockerfile`; `backend/main.py`.
- **IMPLEMENTED tooling** — deploy scripts enable Google APIs, prepare Artifact Registry/service accounts/Firestore, use Cloud Build, deploy Cloud Run gen2, configure timeout/concurrency/scaling, assign environment variables, and smoke test. Evidence: `backend/scripts/deploy-cloud-run.ps1`; `deploy-cloud-run.sh`; `backend/scripts/smoke_test.py`.
- **PARTIAL speech deployment** — the Cloud Run scripts deploy the main backend service only; no equivalent checked-in script deploys and wires `Dockerfile.speech` as a separate production speech service. The separate speech topology is proven for local Compose, not for current production. Evidence: deploy scripts; `backend/Dockerfile.speech`; `docker-compose.local.yml`.
- **IMPLEMENTED configuration** — frontend Firebase Hosting serves `dist`, rewrites SPA routes, disables caching for shell files, and caches hashed assets. Evidence: `frontend/firebase.json`; `frontend/scripts/build-production.mjs`.
- **UNKNOWN live deployment** — `DEPLOYMENT_REPORT.md` and vector provisioning notes are point-in-time evidence. They do not prove that current source, speech service, vector adapter, environment variables, or latest image are deployed now.
- **SPEC-PENDING CI/CD** — no checked-in GitHub Actions workflow was found; builds/tests/deployments are local/script-driven.

## Specification-versus-runtime gap ledger

| Expected capability | Current evidence | Status | Architecture documentation rule |
| --- | --- | --- | --- |
| OCR prohibited for Resume acceptance | Runtime performs RapidOCR on sparse/image PDF pages | PARTIAL mismatch | Show OCR in **current** flow; annotate ADR/testing-seam conflict |
| Initial upload idempotency key and status resource | Only content-hash extraction reuse exists | SPEC-PENDING | Do not label cache as upload idempotency |
| Atomic Replacement Upload | No replacement route/service found | SPEC-PENDING | Target-only node/path |
| Strict Profile PATCH with `If-Match` | Profile route exposes GET only | SPEC-PENDING | Target-only node/path |
| Durable evidence IDs/provenance/audit | Temporary provenance exists; IDs/audit persistence absent | PARTIAL | Separate temporary verification from durable provenance |
| Shared readiness enforcement at text/voice start | Validator exists only in profile GET | PARTIAL | Show current bypass and target gate separately |
| Atomic session snapshot with exact Profile Version | State copies profile content; explicit version/transaction missing | PARTIAL | Never claim full immutable-version contract |
| Report uses immutable session evidence only | Service reloads latest profile | PARTIAL | Mark latest-profile dependency/risk |
| Request-time RAG for every question/evaluation | Retrieval only feeds planner; round indirectly feeds question | PARTIAL | Do not draw retriever directly into evaluator/report |
| Production vector quality proven | Adapter/index evidence exists; research benchmark uses different representation | UNKNOWN/PARTIAL | Separate implementation, provisioning, deployment selection, and quality evidence |
| Production hybrid retrieval | Offline research only | SPEC-PENDING | Never place hybrid in active gateway container |
| Online A/B/C assignment | Offline reconstruction/evaluation only | SPEC-PENDING | Keep evaluation control plane outside production data path |
| Queue/workers/Redis/object storage | None found | SPEC-PENDING | Omit from current topology |
| Concurrent report-generation claim | Existing-report check only | PARTIAL | Show duplicate-call race possibility |
| Full distributed observability/SLO alerts | Structured logs and stage timing only | PARTIAL | Do not invent tracing/metrics backends |
| Checked-in CI workflow | None found | SPEC-PENDING | Show manual/local validation and script deployment |

## High-confidence source map for downstream diagrams

Use these symbols as the canonical evidence anchors:

- Gateway/container: `backend/gateway/main.py::app`, `lifespan`.
- Composition root: `backend/core/dependencies.py::build_interview_repository`, `get_llm_service`, `get_resume_llm_service`, `build_interview_knowledge_retriever`, `get_interview_orchestrator`.
- Resume HTTP/file lifecycle: `backend/gateway/api/resume.py::upload_resume`.
- Document extraction/OCR: `backend/infrastructure/documents/pdf_service.py::DocumentService`; `quality.py::classify_text_quality`; `ocr.py::RapidOCREngine`.
- Resume AI: `backend/services/profile_scanner/agent.py::ResumeAgent`; `context.py::build_resume_context`; `verification.py::verify_and_reconcile_profile`; `schemas.py::ResumeExtractionResult`.
- Candidate Profile/readiness: `backend/shared/schemas/candidate.py::CandidateProfile`, `PersistedCandidateProfile`; `backend/services/candidate_profile/readiness.py::evaluate_interview_readiness`.
- Interview API: `backend/gateway/api/interview.py::prepare_interview`, `start_interview`, `submit_answer`.
- Orchestration: `backend/orchestrator/interview_orchestrator.py::InterviewOrchestrator`; `decision_service.py::InterviewDecisionService`; `conversation_flow.py`.
- Planner/question/evaluator/report: corresponding `backend/services/*/agent.py`, `prompts.py`, and schemas.
- LLM provider: `backend/infrastructure/llm/vertex_gemini.py::VertexGeminiService`.
- Local retrieval: `backend/services/interview_knowledge/local.py::LocalKnowledgeRetriever`.
- Vector retrieval/indexing: `backend/infrastructure/interview_knowledge/firestore_vector.py::VertexTextEmbedder`, `FirestoreVectorKnowledgeRetriever`, `CatalogVectorIndexer`.
- Runtime schemas/state: `backend/shared/schemas/interview.py`, `evaluation.py`; report schema at `backend/services/report_generator/schemas.py`.
- Persistence contract/adapters: `backend/infrastructure/repositories/base.py::InterviewRepository`; `sqlite.py::SQLiteInterviewRepository`; `firestore.py::FirestoreRepository`; physical SQLite tables in `backend/models.py`.
- Voice runtime: `backend/gateway/api/voice.py::voice_interview`; `backend/services/voice_session/`; `backend/infrastructure/speech/`; `backend/speech_service/main.py`.
- Offline evaluation: `backend/services/system_evaluation/`; `evaluation/m1/` through `evaluation/m8/`; A/B/C/grounding at `evaluation/defense_extension/e3_ablation_analysis.py` and `e3_grounding_analysis.py`.
- Deployment: `scripts/run_backend.ps1`; `docker-compose.local.yml`; `backend/Dockerfile`; `backend/Dockerfile.speech`; Cloud Run deploy scripts; `frontend/firebase.json`.
- Intended contracts: `docs/PIPELINE_CV_TO_INTERVIEW_DEEP_DIVE_VI.md`; `docs/RESUME_REVIEW_UI_SPEC.md`; `docs/RESUME_REVIEW_TESTING_SEAMS.md`; ADRs `0001`-`0012`.

## Evidence gaps that remain unknown

1. The repository cannot prove the currently deployed Cloud Run/Firebase Hosting revisions or their active environment values.
2. It cannot prove whether the production gateway currently selects local lexical or Firestore vector retrieval.
3. It cannot prove the current Firestore vector index/catalog freshness beyond the dated provisioning record.
4. It has no checked-in live 20-30-session evidence establishing current end-to-end completion, latency, speech quality, concurrency, or cost for the deployed system.
5. It has no human-reviewed ground truth sufficient to generalize the frozen A/B/C question findings beyond their documented slice.
6. It has no queue/object-storage/Redis/online-experiment infrastructure; these should remain absent from current-runtime diagrams unless later source is added.
