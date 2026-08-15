# FiPilot Presentation System Truth Map

Prepared on 2026-08-14 from repository commit `51fc3b5` on branch
`restore/first-deploy-frontend`. The source deck is
`FiPilot_Capstone_Presentation (1).pptx.pptx` (28 slides). This document records
what may and may not be claimed in the revised presentation.

## Evidence rules

- **Implemented** means the active `gateway`, `services`, `orchestrator`,
  `infrastructure`, `shared`, or production frontend path contains the behavior.
- **Deployment-confirmed** means `DEPLOYMENT_REPORT.md` records a successful
  production check on 2026-07-23.
- **Designed/target** means documentation or an ADR specifies the behavior, but
  the active route does not yet implement it completely.
- The active application does **not** use LangGraph. Compatibility modules under
  `backend/app/` and `shared/schemas/graph_state.py` are not a second runtime.

## Final slide-editing claim gate

These statements are the safe summary for ChatGPT slide editing. The detailed
file-and-line evidence and search limitations are in
`docs/presentation/EVALUATION_EVIDENCE_AUDIT.md`.

| Topic | Slide-safe claim | Required boundary |
| --- | --- | --- |
| Orchestration | In-process multi-agent orchestration; no LangGraph in the active application. | Do not draw a LangGraph graph or name LangChain/LangGraph as an implemented runtime. |
| Retrieval | Packaged-catalog lexical retrieval using token overlap and deterministic top-8 selection. | No embedding model, vector database, semantic search, or semantic reranker is implemented in the audited source. |
| Text deployment | The text workflow was remotely verified in production on 2026-07-23. | This is a dated first-party deployment attestation, not proof that current HEAD is deployed or an accuracy/latency benchmark. |
| Voice deployment | Voice is implemented in current source and documented for local/private-service operation. | Production voice is unconfirmed because no later deployment report proves the speech worker or end-to-end speech path. |
| Evaluation | Methodology exists, but the available manifest is empty and the checked-in aggregate result is `no_data`. | Quantitative AI performance is N/A. Do not reuse deck numbers, test constants, UI demo scores, or anecdotal timings as metrics. |

The source deck remains unchanged. This truth map describes what a later editor
may claim; it does not assert that the proposed slide edits have been applied.

## Real runtime architecture

| Layer | Real implementation | Responsibility |
| --- | --- | --- |
| Frontend | React 18, TypeScript, Vite, React Router, TanStack Query, Zustand | Authentication UI, Resume upload, Candidate Profile view, text/voice interview rooms, history, report UI |
| Authentication | Firebase Web SDK + Firebase Admin | Google sign-in in the browser; bearer ID-token verification in FastAPI; resource ownership by Firebase `uid` |
| Backend/API | FastAPI + Uvicorn, Python 3.12 | REST/WebSocket boundary, validation, ownership checks, dependency composition |
| AI orchestration | In-process `InterviewOrchestrator` | Plan creation, question generation, answer evaluation, deterministic adaptive branching, bounded memory, follow-up selection |
| AI agents | Resume, planner, question, evaluator, report agents | One task-specific prompt and Pydantic output schema per agent |
| Retrieval | `LocalKnowledgeRetriever` | Lexical domain/topic selection from the packaged catalog; context is passed to the planner only |
| Persistence | SQLite adapter locally; Firestore adapter in production | Candidate Profiles, raw Resume text, extraction artifacts, plan blueprints, session state, turns/evaluations, reports |
| External AI | Vertex AI Gemini through `google-genai` | Structured Resume extraction, planning, question generation, answer evaluation, final report, streamed voice questions |
| Speech | Separate FastAPI speech process or embedded local runtime | Silero VAD, faster-whisper STT, VieNeu-TTS, bounded in-memory PCM streaming |
| Deployment | Firebase Hosting + Cloud Run + Firestore + Vertex AI | Confirmed for the text path; the separate production speech worker remains target architecture in the latest deployment report |

Primary evidence:

- `frontend/src/App.tsx`, `frontend/src/lib/api.ts`
- `backend/gateway/main.py`, `backend/core/dependencies.py`
- `backend/orchestrator/interview_orchestrator.py`
- `backend/infrastructure/repositories/{sqlite,firestore}.py`
- `backend/speech_service/main.py`
- `DEPLOYMENT_REPORT.md`, `docs/SYSTEM_DESIGN_VI.md`

## Active modules

### Frontend

- Public landing route: `/`.
- Protected Candidate Profile, text interview, speech interview, history,
  settings, and report routes are declared in `frontend/src/App.tsx`.
- `frontend/src/lib/api.ts` centralizes bearer-authenticated REST requests and
  voice WebSocket URL construction.
- `SpeechInterviewPage.tsx`, `useSpeechInput.ts`, `useInterviewerAudio.ts`, and
  `pcmAudioPlayer.ts` implement microphone capture, transcript events, and PCM
  playback.

### Gateway and domain services

- `backend/gateway/api/resume.py`: initial PDF/DOCX upload and extraction.
- `backend/gateway/api/candidate_profile.py`: owned Candidate Profile GET and
  strong `ETag` response.
- `backend/gateway/api/interview.py`: prepare, start, answer, and restore a
  session.
- `backend/gateway/api/voice.py`: authenticated public voice WebSocket.
- `backend/gateway/api/report.py`: report generation/read and history.
- `backend/services/candidate_profile/readiness.py`: shared readiness evaluator,
  currently exposed by profile GET.
- `backend/services/interview_preparation/service.py`: profile-version/config
  keyed plan cache and in-flight request deduplication.

### Agents and orchestration

| Module | Input | Output | Method |
| --- | --- | --- | --- |
| `ResumeAgent` | Extracted Resume text | `CandidateProfile` | Gemini structured JSON; document classification threshold `0.7`; caps 30 skills, 8 evidence items, 6 projects, 6 experiences |
| `InterviewPlannerAgent` | Candidate Profile, config, retrieved catalog context | `InterviewPlan` | Gemini structured JSON; candidate evidence remains authoritative |
| `QuestionGeneratorAgent` | Candidate Profile, one plan round, config | `InterviewQuestion` | Gemini structured JSON; one evidence-grounded question plus expected points and follow-up probes |
| `EvaluatorAgent` | Profile, question/rubric, answer, config | `AnswerEvaluation` | Gemini structured JSON; 0–10 scoring plus strengths, weaknesses, missing concepts, feedback, follow-up signal |
| `InterviewDecisionService` | Evaluation, current question, session | `InterviewDecision` | Deterministic rules: follow-up first; otherwise score >= 8 increases difficulty; otherwise next planned round |
| `InterviewMemoryService` | Voice turn evaluation | Bounded memory | Stores previous topics, covered skills, weaknesses, and unresolved follow-up points; applied to later voice rounds |
| `FollowUpSelectionService` | Existing follow-up probes + evaluation | One probe | Lexical overlap ranking against evaluation gaps |
| `ReportGeneratorAgent` | Candidate Profile + completed session evidence | `InterviewReport` | Gemini structured JSON; coaching report generated only after completion |

The orchestrator is ordinary asynchronous Python. `backend/orchestrator/workflow.py`
explicitly says LangGraph is not used.

## AI model and method selection

Defaults are configurable through environment variables; the table shows the
checked-in defaults and routing behavior.

| Module | Model/method | Repository-supported reason |
| --- | --- | --- |
| Resume extraction | `gemini-2.5-flash-lite`, Vertex location `global`, structured JSON, temperature `0.1`, thinking budget `0`, one attempt | Low-latency structured extraction; isolated routing lets Resume extraction use a separate endpoint/model |
| Interview planning | `gemini-2.5-flash`, structured JSON, temperature `0.1`, thinking budget `0` | Fast “simple” planning task; Pydantic validates the plan |
| Question generation | `gemini-2.5-flash`, structured JSON, temperature `0.2`, thinking budget `0` | Fast per-turn generation while preserving a typed question/rubric contract |
| Text answer evaluation | `gemini-2.5-pro` by default, structured JSON, temperature `0.1` | The configured complex route prioritizes evaluation quality |
| Voice answer evaluation | `gemini-2.5-flash`, structured JSON, thinking budget `0` | The evaluator is on the spoken critical path, so the code selects the lower-latency route |
| Final report | `gemini-2.5-pro`, structured JSON, temperature `0.1` | Holistic synthesis is routed as a complex task |
| Voice question streaming | `gemini-2.5-flash`, streamed JSON text, thinking budget `0` | Starts TTS from the streamed `question` field; the completed object is still validated and has a typed fallback |
| STT | faster-whisper, default model `large-v3-turbo`; default CPU/int8, configurable CUDA compute | Code comments select the distilled model for Vietnamese mixed with English technical terms and manageable memory use |
| Voice activity detection | Silero VAD | Speech start/end and endpointing before final STT submission |
| TTS | VieNeu `v3turbo`, default 24 kHz PCM | Streaming Vietnamese speech with bounded chunks/queues |
| Retrieval | Local lexical token overlap; no embedding model | Deterministic, packaged, dependency-free retrieval over the checked-in catalog |

Evidence: `backend/core/settings.py`, `backend/core/dependencies.py`,
`backend/infrastructure/llm/vertex_gemini.py`, and the agent implementations
under `backend/services/`.

## Actual data flow

### Authentication and Resume-to-Profile

1. The browser signs in with Firebase and obtains an ID token.
2. The frontend sends `POST /api/v2/resume/upload` with a bearer token and one
   multipart PDF or DOCX.
3. The gateway checks extension and the 10 MB size limit, copies the upload to a
   temporary file, computes SHA-256, and extracts text with `pypdf` or
   `python-docx`.
4. Extraction output is reused from an in-memory cache or an owned persistent
   extraction artifact when the `(uid, content hash, extraction version)` key
   matches.
5. On a cache miss, `ResumeAgent` asks Gemini for `ResumeExtractionResult`,
   rejects a non-Resume classification below the required threshold, and
   converts the result to `CandidateProfile`.
6. The repository creates an owned candidate, stores raw Resume text and the
   profile, and stores the reusable extraction artifact.
7. The temporary file is deleted in `finally`.

Current implementation caveat: the active upload route does not yet implement
the ADR-specified `Idempotency-Key` state machine, replacement upload, upload
status resource, or file magic-byte validation.

### Interview preparation and start

1. `POST /api/v2/interview/prepare` or `/start` reloads the owned persisted
   Candidate Profile; it does not accept profile data in the start body.
2. The plan key includes owner, candidate, `profile_version`, interview config,
   and blueprint version. The service checks memory and the persistent blueprint
   store before generating a new plan.
3. `LocalKnowledgeRetriever` selects a domain, level guidance, and up to eight
   candidate-aligned catalog topics.
4. `InterviewPlannerAgent` creates typed rounds and coverage/risk goals.
5. `QuestionGeneratorAgent` creates the first typed question.
6. For text mode, a persisted opening introduction precedes the planned first
   technical question.
7. The complete `InterviewSessionState` is stored, including the profile value,
   config, plan, phase, current/completed turns, memory, and voice analytics.

Current implementation caveat: `start_interview` does not call the readiness
evaluator before creating a session, even though the ADR/spec requires backend
readiness enforcement.

### Adaptive answer loop

1. The gateway reloads the owned session state.
2. The evaluator scores the answer against candidate context and the question's
   `expected_answer_points`.
3. The deterministic decision service chooses:
   - `follow_up` when the evaluator requests one;
   - `increase_difficulty` when score is at least 8;
   - otherwise the next planned round;
   - completion when the configured question count or plan is exhausted.
4. Follow-up selection first reuses unused generated probes; voice mode ranks
   probes against identified gaps. If no probe remains, a new non-duplicate
   question is generated.
5. Voice mode updates bounded structured memory and applies unresolved gaps to
   later rounds. Text mode speculatively prefetches the next normal question to
   reduce latency but discards it if the adaptive branch changes.
6. Updated state and turns are persisted before the response returns.

### Voice path

1. A voice session is created through the same REST start endpoint with
   `interview_config.mode = "voice"`.
2. The browser opens `WS /api/v2/voice/interview/{session_id}`. The gateway
   verifies Firebase identity, allowed origin, ownership, mode, and one active
   connection per owned session.
3. Browser microphone PCM16 frames enter bounded queues in the gateway and are
   either processed locally or forwarded to the private speech service at
   `/internal/v1/inference`.
4. Silero VAD emits speech boundaries; faster-whisper emits partial/final
   transcripts. The final transcript is submitted through the same orchestrator
   and evaluator used by text interviews.
5. The next question is streamed from Gemini. Text deltas are sent to the UI and
   chunked for VieNeu-TTS; 24 kHz PCM returns to the browser.
6. VAD can interrupt active playback (barge-in). Audio remains in bounded memory
   and is not intentionally persisted or logged.

### Report and history

1. Reports can be generated only after the session is completed.
2. An existing report is returned instead of regenerating it.
3. Gemini creates a typed coaching report from the completed evidence and the
   repository embeds it in the session record/document.
4. History is paginated and owner-scoped.

Current implementation caveat: `ReportService` reloads the latest Candidate
Profile as well as the stored session state. Therefore the deck must not claim
that reports are proven to use only an immutable profile snapshot after later
profile changes.

## Retrieval and knowledge truth

- The packaged `catalog.json` contains **4,379 topic entries across 10 IT
  domains**. Each domain also has level guidance for Intern, Junior, Middle, and
  Senior.
- The source catalog is generated from `Knowledge/Domains` and
  `Knowledge/Levels` by `backend/scripts/build_interview_knowledge_catalog.py`.
- Domain selection combines exact domain-label detection and token overlap with
  domain terms.
- Topic ranking uses normalized lexical token overlap, a larger weight for
  longer matching tokens, and an exact-title bonus. The default limit is eight
  topics.
- Retrieved strings contain the selected domain, level guidance, topic path,
  and up to five anchors. They augment the planner prompt only.
- There is no embedding model, vector database, semantic reranker, external
  document index, or online retrieval call in the active implementation.
- Retrieved knowledge does not directly enter the evaluator or report prompt;
  therefore the current deck sentence claiming it grounds both questions and
  feedback is too broad.

## Storage truth

### Firestore production adapter

```text
users/{uid}
  candidates/{candidateId}
  interviews/{sessionId}
  interview_blueprints/{artifactKey}
  resume_extractions/{artifactKey}
```

Candidate documents contain the profile, version, and raw Resume text. Interview
documents contain the state payload plus arrays for turns/evaluations and an
embedded final report. Every adapter path begins below the authenticated user
document.

### SQLite local adapter

SQLite uses `users`, `sessions`, `messages`, `evaluations`,
`interview_blueprint_artifacts`, and `resume_extraction_artifacts`. Complex
profile, plan, session, and report objects are serialized as JSON in compatible
columns.

## Active API surface

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/v2/auth/me` | Current Firebase identity |
| `POST` | `/api/v2/resume/upload` | Initial Resume upload and Candidate Profile extraction |
| `GET` | `/api/v2/candidates/{candidate_id}/profile` | Owned profile + readiness + strong ETag |
| `POST` | `/api/v2/interview/prepare` | Generate/cache a plan blueprint before start |
| `POST` | `/api/v2/interview/start` | Create session and first/opening question |
| `POST` | `/api/v2/interview/{session_id}/answer` | Evaluate answer and advance adaptive state |
| `GET` | `/api/v2/interview/{session_id}` | Restore session state |
| `WS` | `/api/v2/voice/interview/{session_id}` | Voice interview, speech input, or interviewer playback |
| `POST` | `/api/v2/interview/{session_id}/report` | Generate an idempotent final report |
| `GET` | `/api/v2/interview/{session_id}/report` | Read a report |
| `GET` | `/api/v2/interviews` | Paginated history |
| `GET` | `/health`, `/ready` | Liveness and dependency readiness |

The active gateway currently has no Candidate Profile PATCH, Replacement Upload,
or upload-status endpoints.

## Deployment truth

The 2026-07-23 deployment report confirms:

- React SPA on Firebase Hosting.
- FastAPI backend on Cloud Run in `us-central1`.
- Firestore Native mode for persistence.
- Firebase Authentication and ownership isolation.
- Vertex AI Gemini through the Cloud Run service identity.
- Text Resume-to-interview-to-report E2E behavior.

The same report explicitly says the production release exposed speech mode only
as a Phase 2 boundary and did not deploy microphone/WebSocket/STT/TTS behavior.
The repository has since added the end-to-end speech source and local three-
process architecture, but there is no newer checked-in deployment report proving
the speech worker is running in production. Slides must label it **implemented
in source/local; target for production**, not production-deployed.

## Evaluation truth

The repository contains a real privacy-safe evaluation framework under
`backend/services/system_evaluation`:

| Evaluation slice | Dataset input | Implemented metrics |
| --- | --- | --- |
| Resume extraction | Resume path, expected skills, selected expected fields | Skill precision/recall/F1, field accuracy, processing latency, failures |
| STT | Mono PCM16 16 kHz WAV + reference text + `vi`/`en`/`mixed_technical` category | WER, CER, latency, failures, per-category values |
| TTS | Text prompts | First-audio latency, total generation duration, generated-audio duration ratio, failures |
| Question generation | Synthetic profile + round + config | Gemini-judge relevance, difficulty alignment, CV alignment, latency, failures |
| Answer evaluation | Synthetic labelled answer + human 0–10 score | Repeated-score consistency/MAD, MAE against human label, latency, failures |
| Voice turn | Content-free success flag + total latency | Average, p50, p95, failure rate |

Privacy design: manifests may point to private Resume/audio/transcript fixtures;
the generated reports contain aggregate values only and intentionally omit raw
content, prompts, answers, tokens, and audio.

**Current checked-in result status:** `backend/evaluation_dataset.example.json`
contains zero cases in every category, and `backend/evaluation_report.json` is
`status: "no_data"` with all quality/latency metrics null. The large numerical
claims on current slide 22 (235 CVs, 200 WAVs, accuracy and latency values) do not
appear in source, documentation, the dataset manifest, or the generated report
and must be removed unless the team supplies reproducible evidence.

An additional workspace-and-history evidence pass on 2026-08-14 found no valid
substitute dataset. Candidate artifacts included a personal Resume with direct
identifiers, unlabelled demo MP3s, mutable local SQLite session data, a single
ad hoc speech trace, four referenced but missing code-switch WAV fixtures, and
historical YOLO/DocLayout plots whose source data and run files are absent and
whose pipeline is no longer active. None is eligible for empirical claims. See
`docs/presentation/EVALUATION_EVIDENCE_AUDIT.md` for the complete disposition.

The framework's focused unit suite passes (`4 passed`), proving the aggregation
and privacy-reporting mechanics. A safe rerun of the empty example manifest
reproduced `status=no_data` with exit code `2`; this is readiness evidence, not
model-performance evidence.

> **Evaluation Readiness / Remaining Evidence Gap:** FiPilot has an implemented,
> privacy-aware evaluation methodology and synthetic unit coverage, but no
> approved, versioned labelled benchmark is available. Quantitative evaluation
> remains N/A until consented/sanitized fixtures, reference transcripts,
> independently reviewed human scores, frozen model/config versions, and
> aggregate framework outputs are produced.

The 2026-07-23 deployment report provides qualitative E2E PASS evidence, not an
AI accuracy or latency benchmark.

## Product UI evidence

On 2026-08-14, the real React frontend and FastAPI backend were run locally with
an isolated SQLite database containing only sanitized demonstration records.
Playwright captured the Candidate Profile, active text interview, saved coaching
report, and interview history routes at 1440 × 900. The assets and capture
provenance are recorded in
`docs/presentation/PRODUCT_SCREENSHOT_EVIDENCE.md`.

The captures prove that these source-backed UI surfaces render against the real
HTTP contracts. They do not prove a production deployment or model quality.
Any visible report score is synthetic demo state and must not be reused as an
evaluation metric.

## Current PPTX technical-slide audit

| Current slide | Finding | Required treatment |
| ---: | --- | --- |
| 13 System Architecture | Diagram shows level classification, template matching, admin import, separate RAG data and Q&A stores; these are not the active architecture | Replace completely with a layered source-backed diagram |
| 14 AI Interview Workflow | Directionally correct but merges evaluator/report and omits retrieval scope, adaptive decision, memory, persistence, and speech boundary | Replace with explicit multi-agent/orchestrator architecture |
| 15 RAG & Knowledge | Lexical retrieval and 10-domain catalog are real; retrieval only augments planning, not feedback directly | Retitle and redraw as lexical retrieval with “no vector DB” disclosure |
| 17 Data Sources | Core entities are real; “target role” is not a canonical Candidate Profile field | Replace labels with canonical fields and owner-scoped storage |
| 18 Resume Extraction | Parser and Gemini flow are real; model and cache/artifact behavior are missing; “Firestore” is only the production adapter | Correct model, validation, cache, owner scope, and SQLite/Firestore split |
| 20 Integrated AI Modules | Mostly accurate but duplicates slide 14 and names methods too vaguely | Replace with the model-selection matrix and separate methodology slides |
| 22 Evaluations | All displayed sample counts and numerical results are unsupported by checked-in evidence | Remove all numbers; split into dataset, method, current result status, and analysis |
| 23 Deployment Architecture | The image is not a deployment diagram and invents LangGraph, embeddings, vector DB, moderation, and PDF/JSON downloads | Move to Architecture section and replace completely |
| 26 Contributions | 10 roles x 4 levels and shared text/voice orchestration are supported; production voice is not confirmed | Keep with precise deployment wording |
| 27 Limitations | Broadly supported | Add empty benchmark status and current deployment boundary |

## Uncertain, missing, or contradictory evidence

- No reproducible non-empty evaluation dataset or aggregate AI result is checked
  in. The current deck's metrics are unsupported.
- No current production deployment report confirms the speech service, GPU
  worker, or end-to-end voice latency.
- No embeddings, vector DB, LangGraph, semantic reranking, moderation service,
  admin knowledge importer, template matcher, or report download implementation
  exists in the active source.
- The ADRs specify Candidate Profile PATCH, replacement upload, idempotency,
  atomic versioned mutation, readiness enforcement, and immutable session/report
  semantics. Several of those contracts are not yet present in the active
  gateway routes and must not be shown as completed features.
- The profile GET returns readiness and an ETag, but the frontend/API currently
  do not provide the full durable correction workflow described by the Resume
  Review specifications.
- `docs/BAO_CAO_TONG_QUAN_DU_AN.md` predates the wired lexical knowledge
  retriever and says Knowledge/Template is not connected. The current code and
  tests show that `InterviewPlannerAgent` now receives `LocalKnowledgeRetriever`;
  code is authoritative for the revised slide.
- The repository varies between “Fipilot” and “FiPilot.” The revised deck will
  use the user-requested capitalization **FiPilot** consistently.
