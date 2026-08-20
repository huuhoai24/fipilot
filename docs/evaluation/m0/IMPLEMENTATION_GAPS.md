# M0 Architecture Mismatches and Implementation Gaps

M0 records these gaps only. No production fix is included.

## GAP-001 — Actual document type is not validated

**Claim:** Resume Review ADR 0004 requires one genuine PDF or DOCX, detected
from content, with structured rejection codes.

**Actual implementation:** Upload accepts files by filename suffix only.

**Evidence:** `docs/adr/0004-resume-upload-and-partial-extraction-contract.md:3-7`;
`backend/gateway/api/resume.py:51-62`.

**Impact:** Renamed, malformed, encrypted, or mismatched files can reach the
parser and failures do not conform to the documented API contract.

**Required milestone:** M1 — Resume input integrity.

## GAP-002 — No OCR or image-aware Resume path

**Claim:** Some broad documentation describes modern Resume processing; scanned
Resume behavior must be explicit.

**Actual implementation:** pypdf text-layer extraction only; images, portraits,
logos, layout, and OCR are ignored. Image-only/short text returns a generic 422.

**Evidence:** `backend/infrastructure/documents/pdf_service.py:22-32`;
`backend/gateway/api/resume.py:68-79`.

**Impact:** Scanned/image Resume content cannot create a profile and rejection
does not identify the precise reason.

**Required milestone:** M1 — Document extraction coverage.

## GAP-003 — Silent 12,000-character truncation

**Claim:** ADR 0004 requires complete processing or an explicit
`partial_extraction` warning.

**Actual implementation:** The prompt uses `resume_text[:12000]`; upload returns
success without a partial warning even when the persisted Resume is longer.

**Evidence:** `docs/adr/0004-resume-upload-and-partial-extraction-contract.md:5`;
`backend/services/profile_scanner/prompts.py:15-61`.

**Impact:** Later Resume sections can be omitted while the profile is represented
as complete.

**Required milestone:** M1 — Complete/declared-partial extraction.

## GAP-004 — No programmatic hallucination/provenance verification

**Claim:** Candidate Profile facts and evidence should be traceable to Resume
source material.

**Actual implementation:** Prompt-only grounding, schema validation, and
evidence-to-skill internal matching; no validated source span or evidence ID.

**Evidence:** `backend/services/profile_scanner/prompts.py:6-61`;
`backend/services/profile_scanner/schemas.py:37-81`;
`docs/adr/0008-preserve-profile-provenance-through-explicit-identities.md:3-5`.

**Impact:** Schema-valid unsupported facts can be persisted, and later audits
cannot reliably trace them to source.

**Required milestone:** M1 — Extraction provenance contract.

## GAP-005 — Upload idempotency/status/replacement are absent

**Claim:** ADRs 0005/0009 require opaque idempotency keys, leased operation
states, replay, status URLs, and atomic Replacement Upload.

**Actual implementation:** A SHA-256 extraction cache reuses a profile, but each
request may create a new Candidate; no upload operation/status/replacement route
exists.

**Evidence:** `backend/gateway/api/resume.py:64-162`;
`backend/services/profile_scanner/cache.py:10-67`;
`docs/adr/0005-idempotent-atomic-resume-upload-retries.md:3-7`.

**Impact:** Concurrent retries can duplicate work/resources and documented
recovery/atomic replacement guarantees are unavailable.

**Required milestone:** M2 — Versioned Profile lifecycle.

## GAP-006 — Candidate Profile correction contract is absent

**Claim:** Profile PATCH must use a strict editable allowlist, normalization,
strong `If-Match`, audit events, and stable evidence identities.

**Actual implementation:** Only profile GET is registered; repositories expose
simple save/read methods. No PATCH route, correction schema, evidence ID, audit
event, or conditional mutation exists.

**Evidence:** `backend/gateway/api/candidate_profile.py:15-48`;
`backend/shared/schemas/candidate.py:7-82`;
`docs/adr/0002-strict-candidate-profile-correction-contract.md:3-5`.

**Impact:** The documented durable Profile Review cannot save corrections and
cannot provide concurrency/provenance guarantees.

**Required milestone:** M2 — Versioned Profile lifecycle.

## GAP-007 — Readiness is computed but not enforced at interview start

**Claim:** ADR 0003 requires the same authoritative readiness validator for text
and speech starts.

**Actual implementation:** Profile GET calls `evaluate_interview_readiness`, but
`prepare_interview` and `start_interview` load the profile and continue without
calling it.

**Evidence:** `backend/gateway/api/candidate_profile.py:44-48`;
`backend/gateway/api/interview.py:62-175`;
`docs/adr/0003-separate-profile-validity-from-interview-readiness.md:5`.

**Impact:** Invalid or incomplete persisted profiles can enter both interview
modes despite backend readiness issues.

**Required milestone:** M2 — Profile/start contract enforcement.

## GAP-008 — Session snapshot selection is not atomic/versioned

**Claim:** ADR 0007 requires atomic read/create and stored
`candidate_profile_version` with an immutable profile snapshot.

**Actual implementation:** The route reads the profile, awaits plan/question
model calls, then creates and updates a session. State contains a profile copy,
but no dedicated selected-version field or atomic repository operation exists.

**Evidence:** `backend/gateway/api/interview.py:117-163`;
`backend/shared/schemas/interview.py:100-111`;
`docs/adr/0007-use-owned-versioned-candidate-profile-resources.md:5`.

**Impact:** A future concurrent profile mutation can race session creation, and
the exact selected Profile Version is not auditable.

**Required milestone:** M2 — Immutable session snapshots.

## GAP-009 — Reports reload the live Candidate Profile

**Claim:** Existing sessions/reports must remain derived from the session
snapshot after later Profile Corrections.

**Actual implementation:** `ReportService` parses stored state but separately
reloads the current profile by candidate ID and passes it to the report model.

**Evidence:** `backend/services/report_generator/service.py:27-47`;
`docs/adr/0001-reviewed-candidate-profile-source-of-truth.md:3`.

**Impact:** Once profile editing exists, a historical report may incorporate
facts that were not in the interview snapshot.

**Required milestone:** M2 — Immutable session/report evidence.

## GAP-010 — Active retrieval is lexical, not semantic vector RAG

**Claim:** Slides/older architecture material can be read as describing RAG,
embeddings, vector DB, or LangGraph.

**Actual implementation:** The configured baseline is in-process lexical
overlap over packaged JSON and no LangGraph. Vector code is optional and
disabled.

**Evidence:** `backend/services/interview_knowledge/local.py:78-137`;
`backend/orchestrator/workflow.py:1-9`; active `.env.local` setting;
`docs/presentation/SYSTEM_TRUTH_MAP.md:367-374`.

**Impact:** “semantic/vector RAG” or “LangGraph orchestration” claims would
misstate the running baseline.

**Required milestone:** M3 — Retrieval decision and evaluation.

## GAP-011 — Optional vector path lacks quality gate and resilient fallback

**Claim:** A production vector path should have measured retrieval quality and
defined failure behavior.

**Actual implementation:** Firestore cosine KNN top-5 exists without threshold,
metadata filter, hybrid search, reranking, application timeout, or fallback to
the local retriever. No labelled vector result is checked in.

**Evidence:** `backend/infrastructure/interview_knowledge/firestore_vector.py:96-167`;
`backend/core/dependencies.py:288-331`.

**Impact:** Enabling it can change planning relevance and availability without a
measured acceptance baseline.

**Required milestone:** M3 — Evaluated retrieval rollout.

## GAP-012 — Knowledge records lack answer/evidence governance

**Claim:** A defensible interview knowledge base should expose concepts/rubrics,
sources, versions/hashes, and duplicate/update governance.

**Actual implementation:** Runtime records contain only title, path, anchors;
catalog version is global integer 1. Base catalog has no source/reference,
rubric, record hash, or duplicate detection. Updates are manual.

**Evidence:** `backend/scripts/build_interview_knowledge_catalog.py:23-79`;
`backend/services/interview_knowledge/catalog.json`.

**Impact:** Planner context quality, provenance, duplicate content, and changes
cannot be reviewed at record granularity.

**Required milestone:** M3 — Knowledge governance.

## GAP-013 — No verified production ground-truth evaluation

**Claim:** Historical slides/evidence contain high accuracy aggregates.

**Actual implementation:** The public manifest is empty; supporting labels and
sample outputs are absent; Resume aggregates conflict; the separate pilot is
synthetic and tied to an older commit.

**Evidence:** `backend/evaluation_dataset.example.json`;
`evaluation/evidence/evaluation_manifest.json`;
`evaluation/ragas_pilot/run_manifest.json`.

**Impact:** Production accuracy, WER/CER, question quality, evaluator agreement,
and report quality cannot be verified or reproduced.

**Required milestone:** M4 — Approved labelled evaluation baseline.

## GAP-014 — Model/prompt/knowledge versions are not persisted with outputs

**Claim:** AI outputs should be reproducible and attributable to exact runtime
inputs/configuration.

**Actual implementation:** Logs record operation/model/latency, but Candidate
Profiles, sessions, and reports do not persist prompt version, model name,
knowledge catalog version/hash, or retrieval backend.

**Evidence:** `backend/infrastructure/llm/vertex_gemini.py:178-304`;
`backend/shared/schemas/candidate.py`;
`backend/shared/schemas/interview.py`;
`backend/services/report_generator/schemas.py`.

**Impact:** Historical AI behavior cannot be reconstructed after environment,
prompt, model, or catalog changes.

**Required milestone:** M4 — Evaluation/reproducibility metadata.

## GAP-015 — Speech remote calls have no explicit timeout/retry/fallback

**Claim:** Speech is an optional separate service or embedded runtime.

**Actual implementation:** Construction chooses one path from configuration.
Remote WebSocket receive/finish waits have no application timeout or retry and
do not switch to embedded speech on failure.

**Evidence:** `backend/core/dependencies.py:131-165,214-250`;
`backend/infrastructure/speech/remote.py:29-223`.

**Impact:** A stalled/unavailable speech service can stall or fail a voice turn;
the phrase “local fallback” can be misread as automatic failover.

**Required milestone:** M5 — Speech resilience/SLOs.

## GAP-016 — Documentation contains obsolete provider/runtime descriptions

**Claim:** `docs/AI_Interview_Platform_Documentation_VI.md` describes
OpenAI-compatible Ollama Gemma, Groq STT fallback, and PhoWhisper/Transformers.

**Actual implementation:** Active gateway dependency construction uses only
Vertex Gemini for LLM tasks and faster-whisper/VieNeu/Silero for speech.

**Evidence:** `docs/AI_Interview_Platform_Documentation_VI.md:85-89,265`;
`backend/core/dependencies.py:94-128,214-250`.

**Impact:** Operators/reviewers can configure, diagram, or claim a runtime that
does not exist in current production source.

**Required milestone:** M1 — Documentation truth alignment.

## GAP-017 — Retrieval documentation is stale relative to dirty source

**Claim:** Presentation truth docs state there is no embedding model/vector DB
implementation in audited source.

**Actual implementation:** That remains true for the configured local runtime,
but the current dirty filesystem contains a wired opt-in Vertex embedding and
Firestore vector adapter/indexer.

**Evidence:** `docs/presentation/SYSTEM_TRUTH_MAP.md:28,233-234`;
`backend/infrastructure/interview_knowledge/firestore_vector.py`;
`backend/core/dependencies.py:288-331`.

**Impact:** “implemented,” “enabled,” and “deployed” are currently conflated.

**Required milestone:** M1 — Configuration/deployment truth manifest.

## Priority summary

| Milestone | Scope |
| --- | --- |
| M1 | Align documentation/config truth; make Resume parsing complete or explicitly partial; validate actual document type and provenance |
| M2 | Deliver versioned Candidate Profile corrections, readiness enforcement, idempotent replacement, and immutable versioned session/report snapshots |
| M3 | Govern and evaluate knowledge/retrieval before enabling vector search |
| M4 | Build approved labelled datasets and persist reproducibility metadata |
| M5 | Define and implement speech timeouts, retry/failover policy, and SLO evidence |
