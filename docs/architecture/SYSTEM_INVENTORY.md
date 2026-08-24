# System Inventory

## Audit boundary

This inventory describes the checked-out repository on 2026-08-20. Runtime source takes precedence where it conflicts with prose. Dated deployment reports establish only point-in-time evidence; they do not prove current live state. The untracked `evaluation/m1` through `evaluation/m8`, `evaluation/defense_extension`, and related generated documentation are labeled as worktree/offline evidence rather than committed production baseline.

The active HTTP application is `backend/gateway/main.py`; `backend/main.py` re-exports that application. Files under `backend/app` are compatibility modules and tests, not a second active gateway. The repository helper loads `backend/.env.local` or `BACKEND_ENV_FILE`; it does not load `backend/app/.env`.

## Canonical component dictionary

| # | Component | Scope | Status | Responsibility | Primary evidence |
|---:|---|---|---|---|---|
| 1 | React SPA | Runtime | IMPLEMENTED | Routes, authenticated pages, profile review, text and voice interview UX | `frontend/src/App.tsx`, `frontend/src/pages` |
| 2 | Firebase client authentication | Runtime | IMPLEMENTED | Browser sign-in state and ID-token acquisition | `frontend/src/contexts/AuthContext.tsx`, `frontend/src/lib/firebase.ts` |
| 3 | FastAPI gateway | Runtime | IMPLEMENTED | Active HTTP and WebSocket boundary | `backend/gateway/main.py`, `backend/gateway/api` |
| 4 | Firebase token and ownership boundary | Runtime | IMPLEMENTED | Verifies tokens and resolves trusted `CurrentUser` | `backend/core/dependencies.py`, `backend/infrastructure/auth/firebase.py` |
| 5 | Resume upload route | Runtime | PARTIAL | Validates and processes one PDF/DOCX up to 10 MiB | `backend/gateway/api/resume.py` |
| 6 | Document service | Runtime | IMPLEMENTED | File signature/type checks and PDF/DOCX extraction | `backend/infrastructure/documents` |
| 7 | RapidOCR fallback | Runtime | IMPLEMENTED | OCR for sparse or image-only PDF pages | `backend/infrastructure/documents/pdf_service.py`, `backend/infrastructure/documents/ocr.py` |
| 8 | Resume context builder | Runtime | IMPLEMENTED | Section-aware prompt context capped at 16,000 characters | `backend/services/profile_scanner/context.py` |
| 9 | Resume extraction agent | Runtime | IMPLEMENTED | Gemini structured classification and profile extraction | `backend/services/profile_scanner/agent.py`, `backend/services/profile_scanner/prompts.py` |
| 10 | Resume provenance | Runtime | PARTIAL | Computes field evidence in memory | `backend/services/profile_scanner/verification.py`, `backend/services/profile_scanner/service.py` |
| 11 | Candidate Profile schema and repository | Runtime | IMPLEMENTED | Canonical profile storage and owned reads | `backend/shared/schemas/candidate.py`, `backend/infrastructure/repositories` |
| 12 | Interview readiness evaluator | Runtime | PARTIAL | Computes structured readiness issues on profile reads | `backend/services/candidate_profile/readiness.py`, `backend/gateway/api/candidate_profile.py` |
| 13 | Candidate Profile Review UI | Runtime | PARTIAL | Displays and edits local profile review state | `frontend/src/pages`, `frontend/src/components` |
| 14 | Conditional Profile Correction | Target contract | SPEC-PENDING | Strict PATCH with strong `If-Match` | `docs/RESUME_REVIEW_UI_SPEC.md`, `docs/RESUME_REVIEW_TESTING_SEAMS.md` |
| 15 | Replacement Upload | Target contract | SPEC-PENDING | Atomic replacement guarded by Profile Version | `docs/RESUME_REVIEW_UI_SPEC.md`, `docs/adr` |
| 16 | Upload operation store | Target contract | SPEC-PENDING | Durable idempotency, processing lease, replay, fencing | `docs/RESUME_REVIEW_TESTING_SEAMS.md` |
| 17 | Preparation cache | Runtime | IMPLEMENTED | In-process TTL/LRU plan preparation and task coalescing | `backend/services/interview_preparation/service.py` |
| 18 | Blueprint artifact store | Runtime | IMPLEMENTED | Persists reusable Interview Plans | `backend/services/interview_preparation/service.py`, repository adapters |
| 19 | Local knowledge retriever | Runtime default | IMPLEMENTED | Custom lexical domain/topic ranking and level guidance | `backend/services/interview_knowledge/local.py` |
| 20 | Firestore vector retriever | Runtime optional | PARTIAL | Embedding query and cosine KNN retrieval | `backend/infrastructure/interview_knowledge/firestore_vector.py` |
| 21 | Production hybrid retriever | Target/experiment | SPEC-PENDING | Would combine retrieval methods in the request path | No production implementation; offline M6 evidence only |
| 22 | Planner agent | Runtime | IMPLEMENTED | Builds typed Interview Plan from profile, config, and retrieved context | `backend/services/interview_planner/agent.py` |
| 23 | Question generator agent | Runtime | IMPLEMENTED | Generates typed questions from a selected round | `backend/services/question_generator/agent.py` |
| 24 | Question streaming service | Runtime | IMPLEMENTED | Streams text question events and reconstructs typed output | `backend/services/question_generator/streaming_service.py` |
| 25 | Evaluator agent | Runtime | IMPLEMENTED | Scores an answer against the current question | `backend/services/answer_evaluator/agent.py` |
| 26 | Decision service | Runtime | IMPLEMENTED | Chooses follow-up, higher difficulty, next round, or completion | `backend/orchestrator/decision_service.py` |
| 27 | Interview orchestrator | Runtime | PARTIAL | Drives session transitions and stores profile content snapshot | `backend/orchestrator/interview_orchestrator.py`, `backend/gateway/api/interview.py` |
| 28 | Answer submission service | Runtime | IMPLEMENTED | Claims `(session, turn)` and atomically completes answer state | `backend/services/interview_answer_service.py`, repository adapters |
| 29 | Voice session manager | Runtime | IMPLEMENTED | Owns one live voice session, queues, event flow, and metrics | `backend/gateway/api/voice.py`, `backend/services/voice` |
| 30 | Speech inference service | Runtime optional | PARTIAL | VAD, STT, and TTS locally or through a separate service | `backend/speech_service`, `scripts/run_speech_service.ps1` |
| 31 | Report service | Runtime | PARTIAL | Generates, persists, and reuses completed-session reports | `backend/services/report_generator/service.py` |
| 32 | Vertex Gemini integration | Runtime | IMPLEMENTED | Static task-to-model routing, structured output, retry, usage timing | `backend/infrastructure/llm/vertex_gemini.py`, `backend/core/settings.py` |
| 33 | SQLite repository | Runtime default | IMPLEMENTED | Local relational persistence | `backend/infrastructure/repositories/sqlite.py`, `backend/models.py` |
| 34 | Firestore repository | Runtime optional | IMPLEMENTED | User-scoped cloud document persistence | `backend/infrastructure/repositories/firestore.py` |
| 35 | Structured logging and timing | Runtime | PARTIAL | Request IDs, JSON logs, redaction, stage and provider timing | `backend/core/logging.py`, `backend/gateway/main.py` |
| 36 | System evaluation runner | Offline | IMPLEMENTED | Runs scenario-based system evaluation | `backend/services/system_evaluation`, `docs/SYSTEM_EVALUATION.md` |
| 37 | M1-M8 and E3 evaluation harnesses | Offline worktree | IMPLEMENTED | Frozen benchmarks, RAG ablation, quality and latency analysis | `evaluation/m1` through `evaluation/m8`, `evaluation/defense_extension` |
| 38 | Checked-in CI workflow | Delivery | SPEC-PENDING | Automated test/build/deploy gate | No `.github/workflows` in the repository |
| 39 | Current production deployment | Operations | UNKNOWN | Live backend/frontend revision and configuration | Repository has scripts and dated reports only |
| 40 | Current vector index freshness | Operations | UNKNOWN | Live collection population, model/dimension consistency | No live control-plane evidence in repository |
| 41 | Current speech deployment | Operations | UNKNOWN | Whether remote speech service is deployed and healthy | Source and local scripts exist; live state is not recorded |
| 42 | Profile audit event store | Target contract | SPEC-PENDING | Immutable mutation audit and legacy education preservation | `docs/RESUME_REVIEW_UI_SPEC.md`, ADRs |
| 43 | Versioned atomic session snapshot | Target contract | SPEC-PENDING | Stores exact Profile Version with immutable session snapshot | `docs/RESUME_REVIEW_TESTING_SEAMS.md` |
| 44 | Uniform API error envelope | Runtime | PARTIAL | Structured errors exist on some routes; other paths use generic detail | `backend/gateway/api`, API tests |

Inventory totals: **24 IMPLEMENTED**, **10 PARTIAL**, **7 SPEC-PENDING**, and **3 UNKNOWN** components.

## Runtime entry points

| Surface | Entry point | Notes |
|---|---|---|
| Backend HTTP/WebSocket | `backend/gateway/main.py` | Canonical FastAPI application |
| Backend compatibility import | `backend/main.py` | Re-exports the gateway application |
| Frontend | `frontend/src/main.tsx` -> `frontend/src/App.tsx` | Vite React SPA |
| Local backend helper | `scripts/run_backend.ps1` | Loads `backend/.env.local` unless overridden |
| Optional speech service | `backend/speech_service/main.py` | Started by `scripts/run_speech_service.ps1` |
| Knowledge catalog build | `backend/scripts/build_interview_knowledge_catalog.py` | Operator CLI |
| Vector indexing | `backend/scripts/index_interview_knowledge_vectors.py` | Operator CLI; no background indexer |
| Offline system evaluation | `backend/services/system_evaluation` and `evaluation/**` | Not a production request path |

## Stores, caches, and queues

| Mechanism | Durability | Content | Important boundary |
|---|---|---|---|
| SQLite | Durable local | Profiles, versions, sessions, messages, evaluations, answer claims, plans, resume artifacts | Default repository |
| Firestore | Durable cloud | Equivalent owned aggregates, plan artifacts, vector chunks | Configuration-selected |
| `catalog.json` | Packaged file | Lexical topics and level guidance | Default retrieval corpus |
| Preparation cache | Process memory | Prepared plan results and in-flight tasks | TTL 300 seconds, capacity 128; not cross-instance |
| Voice queues | Process memory | Audio/events/TTS coordination | Bounded and transient; raw audio is not persisted |
| Browser/query state | Browser memory | Auth, query cache, local UI/session state | Not authoritative persistence |

There is no runtime Redis dependency, durable job queue, resume object store, upload worker fleet, or automatic vector-indexing worker in the audited source.

## External dependencies

| Dependency | Use | Failure effect |
|---|---|---|
| Firebase Authentication/Admin | Identity verification | Protected requests fail closed |
| Vertex AI Gemini | Resume extraction, planning, generation, evaluation, reporting | AI stage retries then fails; no provider fallback |
| Vertex text embeddings | Optional vector query/document embeddings | Vector retrieval/indexing fails; runtime has no automatic lexical fallback |
| Firestore vector search | Optional cosine KNN | Vector mode fails if unavailable or misconfigured |
| RapidOCR / ONNX runtime | PDF OCR fallback | Sparse/image-only extraction may fail |
| PyPDF, PyMuPDF, python-docx | Document extraction | Invalid or unsupported documents are rejected |
| Silero VAD, faster-whisper, VieNeu TTS | Optional speech pipeline | Voice path degrades/fails independently of text interview |
