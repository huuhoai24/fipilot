# Full System Agent Robustness Report

Audit date: 2026-08-23 (Asia/Saigon)  
Runtime source of truth: `backend/gateway`, `backend/services`, `backend/orchestrator`, `backend/infrastructure`, `backend/shared`, and `frontend/src`  
Production implementation changed: **No**

## 1. Executive Summary

```text
Overall Status: FAIL
Agents Tested: 13 modules/seams discovered; all inspected, 8 exercised deterministically, 5 provider-backed quality paths blocked
Test Cases Designed: 70
Test Cases Executed: 40 primary robustness cases
PASS: 20
FAIL: 20
PARTIAL: 0 in the primary ledger
BLOCKED: 18
NOT TESTED: 12
Critical Bugs: 1
High Bugs: 8
```

Supporting regression evidence, kept separate from the 40-case robustness ledger:

- Backend: **286/286 PASS**.
- Frontend: **119/119 PASS**.
- CV/question/RAG evaluation tooling: **7/7 PASS**.
- TypeScript, ESLint, frontend production build, and Python compilation: **PASS**.
- Existing provider-backed artifact: 150 generated questions, 150 LLM-judge calls, and 300 lexical retrieval cases. Artifact hashes match its manifest, but human review is 0/60 and no source commit is recorded; it is supplemental **PARTIAL** evidence, not counted as a current rerun.

The current regression suite is healthy but does not protect several critical AI boundaries. The most serious executed failure is historical report contamination: `ReportService` validates the session snapshot but sends the latest mutable Candidate Profile to `ReportGeneratorAgent`. Other high-risk failures include bypassed Interview Readiness, non-idempotent Resume upload and interview start, acceptance of schema-valid but ungrounded/empty questions, and no score/feedback or score/recommendation consistency checks.

Runtime/documentation mismatches:

- Runtime invokes OCR for sparse or image-only PDFs; ADR 0004 and the testing seam say OCR is never invoked.
- Runtime has only initial Resume upload and Candidate Profile GET. Documented Replacement Upload, upload status/idempotency lifecycle, and Profile PATCH are absent.
- Candidate Profile Review is read-only, while the UI spec requires a durable structured editor and save flow.
- Interview start does not call the documented shared readiness validator.
- Session state stores a profile snapshot, but report generation reloads the current profile.

## 2. System Map

| Agent / Module | Input | Output | Dependencies | LLM/RAG | Status |
| -------------- | ----- | ------ | ------------ | ------- | ------ |
| `DocumentService` | PDF/DOCX path, filename, MIME | `DocumentExtractionResult` | pypdf, python-docx, optional RapidOCR | No LLM; OCR for sparse/image-only PDF | PARTIAL |
| `ResumeAgent` / profile scanner | Extracted Resume text | `ResumeProcessingResult` / `CandidateProfile` | section-aware context, verification | Gemini Flash Lite route; one attempt | PARTIAL |
| `ResumeExtractionResult.to_candidate_profile` | Structured extraction | Canonical `CandidateProfile` projection | Pydantic schemas | No | FAIL |
| `evaluate_interview_readiness` | Candidate Profile | all readiness/validity issues | NFKC normalizer | No | PASS in isolation; FAIL at start integration |
| `LocalKnowledgeRetriever` | Profile + Interview Config | bounded curated topic strings | packaged 4,379-topic catalog | Lexical RAG, default limit 8 | FAIL |
| `FirestoreVectorKnowledgeRetriever` | Profile + config | vector-ranked chunks | Firestore + Vertex embeddings | Vector RAG, default top-k 5 | NOT TESTED |
| `InterviewPlannerAgent` | Profile, config, retrieved topics | `InterviewPlan` | knowledge retriever | Gemini simple route | FAIL |
| `QuestionGeneratorAgent` | Profile, one round, config | one `InterviewQuestion` | prompt builder | Gemini simple route | FAIL |
| `QuestionStreamingService` | Profile, round, config | streamed question + validated/rebuilt metadata | TTS-facing delta publisher | Gemini streaming; metadata fallback | PASS for format fallback; AI quality BLOCKED |
| `EvaluatorAgent` | Profile, question, answer, config | `AnswerEvaluation` | score schemas | Gemini complex for text, simple for voice | FAIL |
| Decision, memory, follow-up services | evaluation + session state | next action, adapted round/memory | deterministic rules | No | PASS for covered branches |
| `InterviewOrchestrator` + preparation cache | persisted profile + config | session state and turns | planner, question generator, evaluator, repository | Agent coordinator | FAIL |
| `ReportGeneratorAgent` / `ReportService` | profile + completed session state | persisted `InterviewReport` | repository | Gemini complex route | FAIL |
| `VertexGeminiService` | prompt + Pydantic schema | validated model output | Vertex AI, retry/timeout layer | Flash/Pro routing | PASS for mocked failure handling; live calls BLOCKED |
| Frontend setup/profile/interview/report flows | user actions + HTTP responses | route and UI state | React, API adapter, Firebase token | No direct LLM | PARTIAL |
| Voice session, STT, TTS | WebSocket/audio/question text | transcript, audio, voice turn state | Faster Whisper/remote STT, Vieneu/remote TTS | Evaluator/question agents downstream | PASS in automated regression; hardware smoke NOT TESTED |

Actual call graph:

```text
POST Resume
  -> DocumentService
  -> ProcessedResumeCache / extraction artifact
  -> ResumeAgent -> VertexGeminiService
  -> verification -> CandidateProfile repository

POST Interview start
  -> repository CandidateProfile (readiness is currently skipped)
  -> InterviewPreparationCache
  -> Local/Firestore Knowledge Retriever
  -> InterviewPlannerAgent -> VertexGeminiService
  -> QuestionGeneratorAgent -> VertexGeminiService
  -> InterviewOrchestrator -> session state repository

POST Answer
  -> answer-submission claim/idempotency
  -> EvaluatorAgent -> VertexGeminiService
  -> decision/memory/follow-up
  -> QuestionGeneratorAgent
  -> updated session state

POST Report
  -> completed session state
  -> latest CandidateProfile (bug: not the stored snapshot)
  -> ReportGeneratorAgent -> VertexGeminiService
  -> report repository
```

Active runtime does not import the standalone `backend/ai_lab` or legacy `backend/app/agents` implementations. Those modules are laboratory/compatibility surfaces and are not counted as a second production pipeline.

## 3. Test Coverage

Primary robustness ledger:

| Area | Designed | Executed | PASS | FAIL | BLOCKED |
| ---- | -------: | -------: | ---: | ---: | ------: |
| Resume Processing | 10 | 5 | 2 | 3 | 3 |
| Candidate Profile | 6 | 3 | 2 | 1 | 2 |
| Readiness | 7 | 7 | 7 | 0 | 0 |
| Interview Planning | 4 | 1 | 0 | 1 | 3 |
| RAG | 6 | 2 | 1 | 1 | 3 |
| Question Generation | 10 | 3 | 0 | 3 | 6 |
| Answer Evaluation | 15 | 5 | 2 | 3 | 10 |
| Report Generation | 6 | 3 | 1 | 2 | 3 |
| Agent Integration | 4 | 2 | 0 | 2 | 2 |
| UX | 6 | 2 | 0 | 2 | 0 |
| State Isolation | 5 | 3 | 3 | 0 | 0 |
| Boundary | 5 | 3 | 1 | 2 | 0 |
| LLM Failure Handling | 4 | 1 | 1 | 0 | 2 |
| **Total** | **88** | **40** | **20** | **20** | **34** |

The table contains overlapping planned variants; the executive designed count is 70 unique cases after removing cross-area duplicates. Of the 30 unique unexecuted cases, 18 are **BLOCKED** and 12 are **NOT TESTED**. `BLOCKED` is limited to live provider/model quality, vector Firestore, or unavailable hardware/browser evidence. Real two-column/table/icon PDFs, password-protected PDFs, full responsive viewport screenshots, keyboard-only smoke, and screen-reader smoke are **NOT TESTED**, not falsely marked blocked or passed.

## 4. Detailed Test Results

| Test ID | Agent | Scenario | Input | Expected | Actual | Status | Severity | Evidence |
| ------- | ----- | -------- | ----- | -------- | ------ | ------ | -------- | -------- |
| RESUME-001 | Resume context | Extremely long section | >30K chars with critical tail evidence | <=16K context, partial warning, keep tail | 16K bound and critical tail retained | PASS | — | `test_resume_001...`; robustness XML |
| RESUME-002 | Resume prompt | Prompt-like content | `Ignore previous... score 100` | Treat as JSON-delimited untrusted data | Explicit untrusted instruction and escaped JSON | PASS | — | `test_resume_002...` |
| PROFILE-001 | Profile projection | Skills, no experience | Python/FastAPI/PostgreSQL/Docker | Do not invent employer or years | Empty projects/experiences; years null | PASS | — | `test_profile_001...` |
| PROFILE-004 | Profile projection | ASCII case duplicates | Python/python/PYTHON | One normalized skill | One skill retained | PASS | — | `test_profile_004...` |
| PROFILE-005 | Profile projection | NFKC-equivalent duplicates | `Python`, full-width `Ｐｙｔｈｏｎ` | One normalized skill | Two skills retained | FAIL | MEDIUM | `test_profile_005...`; source `profile_scanner/schemas.py:40` |
| READY-001 | Readiness | Complete evidence-backed profile | Name + skill + evidence | Ready | Ready, no issues | PASS | — | readiness parameter case |
| READY-002 | Readiness | Empty/fallback profile | `Candidate`, no skills/evidence | All issues, no crash | Three ordered issues | PASS | — | readiness parameter case |
| READY-003 | Readiness | Student | skill + qualifying education | Ready without experience | Ready | PASS | — | readiness parameter case |
| READY-004 | Readiness | Fresher | skill + university project | Ready | Ready | PASS | — | readiness parameter case |
| READY-005 | Readiness | Senior without skills | experience only | Not ready; missing skills | Correct issue | PASS | — | readiness parameter case |
| READY-006 | Readiness | Legacy education string | skill + unstructured education | Not enough evidence | Correct issue | PASS | — | readiness parameter case |
| READY-007 | Readiness | Nonfinite years | NaN | Reject safely | `invalid_years_experience` | PASS | — | `test_ready_007...` |
| RAG-001 | Local retriever | Exact profile terms | Backend Developer, FastAPI, PostgreSQL | Backend domain and API topics | Correct domain/topic family | PASS | — | `test_rag_001...` |
| RAG-005 | Local retriever | No profile evidence | default empty Candidate Profile | No claimed evidence/domain | Returns AI Engineer plus topics | FAIL | MEDIUM | `test_rag_005...`; `local.py:130-142` |
| PLAN-001 | Planner | Schema-valid empty plan | `InterviewPlan(rounds=[])` | Reject/fallback before QGen | Empty plan accepted; orchestrator later uses generic round | FAIL | MEDIUM | `test_plan_001...` |
| QGEN-001 | Question generator | Unsupported role/difficulty | React/easy round; model returns Kubernetes/hard | Reject mismatch | Output accepted unchanged | FAIL | HIGH | `test_qgen_001...` |
| QGEN-002 | Question generator | Semantic repetition history | DI question followed by paraphrase | Previous question available to generator/deduper | Second prompt contains no history | FAIL | MEDIUM | `test_qgen_002...`; prompt context lines 62-64 |
| QGEN-003 | Question generator | Empty question | valid schema object with `question=""` | Reject | Accepted | FAIL | HIGH | `test_qgen_003...`; schema `interview.py:79` |
| EVAL-001 | Evaluator | Empty answer isolation | empty answer; model returns 9/10 | Fail closed / low score | 9/10 accepted unchanged | FAIL | HIGH | `test_eval_001...` |
| EVAL-010 | Evaluator prompt | Mixed Vietnamese/English | Vietnamese sentence with English terms | Preserve content and VI instruction | Preserved | PASS | — | `test_eval_010...` |
| EVAL-014 | Evaluator | Score-feedback conflict | 9/10 + “largely incorrect” | Reject or reconcile | Accepted | FAIL | HIGH | `test_eval_014...` |
| EVAL-016 | Evaluation schema | Duplicate score conflict | top overall=9, nested overall=1 | Reject inconsistent fields | Accepted | FAIL | HIGH | `test_eval_016...`; `evaluation.py:18-19` |
| FLOW-007 | Evaluation schema | Score above range | 15/10 | Validation failure | Pydantic rejects | PASS | — | `test_flow_007...` |
| REPORT-001 | Report generator | High scores + negative verdict | 9/10 turns, no_hire/poor summary | Reject contradiction | Accepted | FAIL | HIGH | `test_report_001...` |
| REPORT-004 | Report generator | Missing turn evaluation | completed answer, evaluation null | No crash; expose low confidence | Prompt generated, report accepted | PASS | — | `test_report_004...` |
| REPORT-006 | Report service | Profile edited after session | snapshot Python; current Kubernetes | Use immutable snapshot | Agent receives current profile | FAIL | CRITICAL | `test_report_006...`; `service.py:34-44` |
| FLOW-001 | Start integration | Non-ready profile | fallback name, no skills/evidence | 422 before planning/session | 200; planner and start run | FAIL | HIGH | `test_flow_001...`; `interview.py:112-156` |
| FLOW-012 | QGen prompt boundary | Prompt-like profile field | project says ignore instructions | Mark nested content untrusted | JSON serialized, but no untrusted instruction | FAIL | MEDIUM | `test_flow_012...` |
| FLOW-013 | LLM format boundary | Markdown/prefix before JSON | fenced and prefixed JSON | Recover JSON object | Both normalized | PASS | — | `test_flow_013...` |
| UX-002 | Interview start API | Two rapid starts | identical payload twice | One logical session/replay/conflict | session IDs `1` and `2` | FAIL | HIGH | `test_ux_002...` |
| UX-003 | Resume upload API | Same Resume/key twice | identical bytes + key | Replay original candidate | candidate IDs `1` and `2`; extraction only once | FAIL | HIGH | `test_ux_003...` |
| STATE-001 | Local retriever | Candidate A then B | Java/Spring/Kafka then React/TS/CSS | No A terms in B | Correct Web domain; no A terms | PASS | — | `test_state_001...` |
| STATE-002 | Preparation cache | user/candidate/version isolation | four key variants | Four keys | Four unique keys | PASS | — | `test_state_002...` |
| STATE-003 | Resume cache | same hash, different user | user A store, user B read | No leak | B miss | PASS | — | `test_state_003...` |
| RESUME-010 | Upload API | Missing idempotency header | valid injected PDF | 400 `idempotency_key_required` | 200 and candidate created | FAIL | HIGH | `test_resume_010...`; upload signature line 46 |
| RESUME-011 | Upload API | Two multipart files | two valid PDFs | 400 `multiple_files_not_allowed` | 200, last file accepted | FAIL | HIGH | `test_resume_011...` |
| RESUME-012 | Document acceptance | Zero-byte PDF | empty `.pdf` | `empty_file` | `file_type_mismatch` | FAIL | MEDIUM | `test_resume_012...` |
| BOUNDARY-001 | Upload API | 10 MB + 1 byte | oversized body | Structured 413 `file_too_large` | 413 with unstructured `detail`; no error code | FAIL | MEDIUM | `test_boundary_001...`; upload line 78 |
| BOUNDARY-002 | Interview config | Above server turn limit | question_count=13; configured max=12 | Reject | Accepted | FAIL | MEDIUM | `test_boundary_002...`; schema `interview.py:53` |
| BOUNDARY-003 | Answer schema | 12,000 / 12,001 chars | exact boundary | accept/reject | Correct | PASS | — | `test_boundary_003...` |

Blocked live quality cases:

| Test ID | Agent | Scenario | Input | Expected | Actual | Status | Severity | Evidence |
| ------- | ----- | -------- | ----- | -------- | ------ | ------ | -------- | -------- |
| PROFILE-002 | Resume Agent | Weak Java mention | “Worked with Java once in university” | No expert inference | Provider unavailable | BLOCKED | — | `GOOGLE_CLOUD_PROJECT` absent |
| PLAN-002 | Planner | Frontend CV / Data Engineer target mismatch | profile/config variants | Evidence-aware level/role | Provider unavailable | BLOCKED | — | provider probe |
| QGEN-004 | QGen | Fresher vs Staff difficulty | student project profile | suitable difficulty | Provider unavailable | BLOCKED | — | provider probe |
| QGEN-005 | QGen | Same input repeated | 5 runs | bounded variation | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-002 | Evaluator | Very short correct | `404` | high correctness despite brevity | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-003 | Evaluator | 500-word wrong answer | verbose misconception | low score | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-004 | Evaluator | Confidently wrong | Redis is SQL | detect error | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-005 | Evaluator | Partially correct | 70% correct, 30% wrong | balanced score/feedback | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-006 | Evaluator | Keyword stuffing | technology list only | low score | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-007 | Evaluator | Repeat question | echoed prompt | low score | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-008 | Evaluator | Off-topic | DB question/CSS answer | low score | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-009 | Evaluator | Correct paraphrase | semantic cache explanation | recognize meaning | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-011 | Evaluator | Mixed language quality | Vietnamese + English terms | content-based score | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-012 | Evaluator | Candidate challenges false premise | no Kubernetes evidence | no unfair penalty | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-013 | Evaluator | “I don't know” | unknown answer | no hallucinated praise | Provider unavailable | BLOCKED | — | provider probe |
| EVAL-015 | Evaluator | Same answer, repeated runs | 5 identical cases | no extreme score drift | Provider unavailable | BLOCKED | — | provider probe |
| REPORT-002 | Report | Low scores | 2/3/1 | not Strong Hire | Provider unavailable | BLOCKED | — | provider probe |
| REPORT-003 | Report | One weak, others strong | mixed evaluations | balanced report | Provider unavailable | BLOCKED | — | provider probe |

## 5. Bugs Found

### BUG-001

```text
Bug ID: BUG-001
Severity: CRITICAL
Affected Agent: ReportService / ReportGeneratorAgent
Related Test: REPORT-006
Description: Historical reports use the latest mutable Candidate Profile instead of the Interview Session snapshot.
Steps to Reproduce: Complete a session with profile A; edit/replace the saved profile; generate the old session report.
Expected: Report agent receives state.candidate_profile from the immutable session.
Actual: ReportService reloads repository.get_candidate_profile(session.candidate_id) and passes it to the agent.
Root Cause: backend/services/report_generator/service.py:34-44 selects the current repository profile after validating session state.
Evidence: robustness XML REPORT-006; source lines 34-44.
Suggested Fix: Generate solely from the stored state snapshot and persist/assert candidate_profile_version.
Regression Test Needed: Yes — SQLite and Firestore historical report invariance.
```

### BUG-002

```text
Bug ID: BUG-002
Severity: HIGH
Affected Agent: Interview start integration
Related Test: FLOW-001
Description: A non-ready profile starts an interview.
Steps to Reproduce: Persist CandidateProfile(name="Candidate", skills=[], evidence=[]); POST /api/v2/interview/start.
Expected: 422 profile_not_interview_ready with all issues; zero planner/session calls.
Actual: 200; orchestration runs and a session is persisted.
Root Cause: start_interview loads ownership but never calls evaluate_interview_readiness.
Evidence: robustness XML FLOW-001; gateway/api/interview.py:112-156.
Suggested Fix: Apply the shared validator before preparation and session creation for text and voice.
Regression Test Needed: Yes — identical readiness response for both modes.
```

### BUG-003

```text
Bug ID: BUG-003
Severity: HIGH
Affected Agent: Resume upload boundary
Related Test: RESUME-010, UX-003
Description: Idempotency-Key is optional/ignored and duplicate uploads create duplicate Candidate Profiles.
Steps to Reproduce: POST identical Resume twice with the same key or without a key.
Expected: missing key rejected; completed attempt replays original candidate.
Actual: both requests return 200 and create candidates 1 and 2; only extraction is cached.
Root Cause: upload route has no Header dependency or upload-operation store; processed cache deduplicates model work, not mutations.
Evidence: robustness XML; gateway/api/resume.py:46, 194-200.
Suggested Fix: Implement the documented fenced idempotency operation before extraction and candidate persistence.
Regression Test Needed: Yes — concurrency and 24-hour replay contract for both repositories.
```

### BUG-004

```text
Bug ID: BUG-004
Severity: HIGH
Affected Agent: Resume upload request contract
Related Test: RESUME-011
Description: Multiple multipart files are accepted instead of rejected.
Steps to Reproduce: Send two parts named file.
Expected: 400 multiple_files_not_allowed before extraction.
Actual: 200; FastAPI binds one file and processing continues.
Root Cause: route declares one UploadFile and does not inspect multipart cardinality.
Evidence: robustness XML RESUME-011.
Suggested Fix: Validate raw multipart file count at the route boundary.
Regression Test Needed: Yes.
```

### BUG-005

```text
Bug ID: BUG-005
Severity: HIGH
Affected Agent: Interview start / session repository
Related Test: UX-002
Description: Duplicate start requests create duplicate interviews.
Steps to Reproduce: POST the same ready candidate/config twice rapidly.
Expected: one logical session, processing response, or explicit conflict.
Actual: two successful sessions with IDs 1 and 2.
Root Cause: preparation is deduplicated, but session creation has no start-attempt idempotency key or uniqueness guard.
Evidence: robustness XML UX-002.
Suggested Fix: Introduce a scoped start-attempt idempotency contract if duplicate starts are not intentional product behavior.
Regression Test Needed: Yes — concurrent HTTP calls.
```

### BUG-006

```text
Bug ID: BUG-006
Severity: HIGH
Affected Agent: QuestionGeneratorAgent
Related Test: QGEN-001, QGEN-002, QGEN-003
Description: Schema-valid empty, ungrounded, wrong-topic, and wrong-difficulty questions pass unchanged; history is absent from normal generation.
Steps to Reproduce: Inject valid InterviewQuestion objects with empty text or Kubernetes/hard for a React/easy round.
Expected: reject, repair, or regenerate; deduplicate against history.
Actual: objects are returned unchanged; normal round prompts contain no question history.
Root Cause: schema has no min_length and no cross-field/grounding validator; agent trusts provider schema conformance as quality conformance.
Evidence: robustness XML QGEN-001/002/003; shared/schemas/interview.py:79.
Suggested Fix: Add a bounded post-generation quality gate for nonblank text, round alignment, unsupported assumptions, and semantic history similarity.
Regression Test Needed: Yes — deterministic gate plus provider quality set.
```

### BUG-007

```text
Bug ID: BUG-007
Severity: HIGH
Affected Agent: EvaluatorAgent / AnswerEvaluation
Related Test: EVAL-001, EVAL-014, EVAL-016
Description: The application accepts a high score for an empty answer, score-feedback conflict, and two contradictory overall scores.
Steps to Reproduce: Return schema-valid fault-injected evaluations.
Expected: fail closed or reconcile to a consistent result.
Actual: all are accepted except numeric values outside 0-10.
Root Cause: validation constrains ranges only; duplicate top-level/nested score models have no consistency validator; agent has no deterministic empty-answer guard in isolation.
Evidence: robustness XML; shared/schemas/evaluation.py:13-19.
Suggested Fix: Define one canonical score representation and add cross-field semantic consistency/empty-answer checks.
Regression Test Needed: Yes — adversarial evaluator calibration corpus.
```

### BUG-008

```text
Bug ID: BUG-008
Severity: HIGH
Affected Agent: ReportGeneratorAgent / InterviewReport
Related Test: REPORT-001
Description: 9/10 scores can coexist with no_hire and a poor-knowledge summary.
Steps to Reproduce: Return a schema-valid contradictory report.
Expected: reject/regenerate or deterministically reconcile.
Actual: report is accepted and assigned an ID/timestamp.
Root Cause: report schema checks ranges/enums only and service performs no evidence/score consistency validation.
Evidence: robustness XML REPORT-001.
Suggested Fix: Validate aggregates against completed evaluations and narrative/recommendation polarity before persistence.
Regression Test Needed: Yes.
```

### BUG-009

```text
Bug ID: BUG-009
Severity: MEDIUM
Affected Agent: LocalKnowledgeRetriever
Related Test: RAG-005
Description: An empty/default profile is classified as AI Engineer with curated topics.
Steps to Reproduce: retrieve_topics(CandidateProfile(), junior config).
Expected: empty result or explicit no-evidence outcome.
Actual: Domain: AI Engineer plus three topics.
Root Cause: every domain scores zero and alphabetical tie-breaking selects the first domain.
Evidence: robustness XML; local.py:130-142.
Suggested Fix: Require positive domain evidence before returning a domain/topic list.
Regression Test Needed: Yes.
```

### BUG-010

```text
Bug ID: BUG-010
Severity: MEDIUM
Affected Agent: InterviewPlannerAgent / InterviewPlan
Related Test: PLAN-001
Description: A schema-valid empty plan is accepted and silently becomes a generic CV-deep-dive question.
Root Cause: InterviewPlan permits rounds=[] and orchestrator _get_round_or_finish supplies a generic round.
Evidence: robustness XML PLAN-001.
Suggested Fix: Validate nonempty plan output for a ready profile or make fallback explicit, evidence-based, and observable.
Regression Test Needed: Yes.
```

### BUG-011

```text
Bug ID: BUG-011
Severity: MEDIUM
Affected Agent: ResumeExtractionResult profile projection
Related Test: PROFILE-005
Description: Full-width and ASCII spellings of the same skill survive as duplicates.
Root Cause: projection uses strip().casefold(), not the shared NFKC comparison key.
Evidence: robustness XML; profile_scanner/schemas.py:40-72.
Suggested Fix: Reuse the shared normalizer at this boundary while retaining the first accepted display spelling.
Regression Test Needed: Yes — all published normalization vectors.
```

### BUG-012

```text
Bug ID: BUG-012
Severity: MEDIUM
Affected Agent: InterviewConfig/API
Related Test: BOUNDARY-002
Description: Configured max_interview_turns=12 is not enforced; question_count=13 or much larger validates.
Root Cause: schema declares ge=1 without le and the route does not consult settings.max_interview_turns.
Evidence: robustness XML; shared/schemas/interview.py:53.
Suggested Fix: Enforce one authoritative maximum at the request/domain boundary.
Regression Test Needed: limit-1, limit, limit+1.
```

### BUG-013

```text
Bug ID: BUG-013
Severity: MEDIUM
Affected Agent: Document/upload errors
Related Test: RESUME-012, BOUNDARY-001
Description: Empty PDF maps to file_type_mismatch; oversized upload returns unstructured FastAPI detail.
Root Cause: no explicit zero-byte classifier and direct HTTPException for size.
Evidence: robustness XML.
Suggested Fix: Centralize document acceptance codes and structured response mapping.
Regression Test Needed: Yes.
```

### BUG-014

```text
Bug ID: BUG-014
Severity: MEDIUM
Affected Agent: Downstream planner/question/evaluator prompt boundary
Related Test: FLOW-012
Description: Profile content is JSON serialized but downstream prompts do not explicitly classify nested profile text as untrusted data.
Suspected Root Cause: only the Resume extraction system instruction includes the untrusted-document rule.
Evidence: robustness XML FLOW-012; question_generator/prompts.py.
Suggested Fix: Add a consistent data/instruction boundary to all agents consuming candidate/JD/answer text.
Regression Test Needed: Yes — prompt-like strings through every downstream prompt builder.
```

### BUG-015

```text
Bug ID: BUG-015
Severity: HIGH
Affected Agent: Candidate Profile frontend/API integration
Related Test: Source audit; documented Resume Review seams
Description: Candidate Profile Review is read-only and the API exposes no PATCH or Replacement Upload route, so extraction errors cannot be corrected in the documented durable workspace.
Expected: Editable canonical fields, If-Match save, stale draft recovery, replacement upload.
Actual: ReadOnlyValue components and GET-only API adapter/route.
Root Cause: documented feature is not implemented in the active runtime.
Evidence: CandidateProfilePage.tsx:65, 297-351; frontend api.ts; gateway route inventory.
Suggested Fix: Implement the approved contract in small tested increments; do not weaken ownership/version rules.
Regression Test Needed: Full normative Resume Review testing seams.
```

## 6. Agent Quality Assessment

| Agent | Functional | Robustness | AI Quality | Error Handling | Overall |
| ----- | ---------: | ---------: | ---------: | -------------: | ------: |
| DocumentService | 4.0 | 3.0 | 3.0 | 3.0 | 3.3 |
| ResumeAgent / profile projection | 3.5 | 3.0 | 2.5 | 3.0 | 3.0 |
| Readiness validator | 4.5 | 4.5 | 4.0 | 4.0 | 4.3 |
| LocalKnowledgeRetriever | 3.5 | 2.5 | 2.5 | 2.5 | 2.8 |
| InterviewPlannerAgent | 3.0 | 2.0 | 2.5 | 2.0 | 2.4 |
| QuestionGeneratorAgent | 3.0 | 1.5 | 2.0 | 2.0 | 2.1 |
| EvaluatorAgent | 3.0 | 1.5 | 2.0 | 2.0 | 2.1 |
| Decision/memory/follow-up | 4.0 | 3.5 | 3.0 | 3.5 | 3.5 |
| InterviewOrchestrator | 3.5 | 2.0 | 2.5 | 2.5 | 2.6 |
| ReportGeneratorAgent / service | 2.5 | 1.0 | 1.5 | 2.0 | 1.8 |
| VertexGeminiService | 4.0 | 4.0 | 3.0 | 4.5 | 3.9 |
| Frontend workflow/API adapter | 3.5 | 2.5 | 3.0 | 3.5 | 3.1 |
| Voice/STT/TTS path | 4.0 | 3.5 | 3.0 | 4.0 | 3.6 |

Explanations for scores <=3:

- Resume extraction has bounded context, provenance checks, and injection instructions, but NFKC normalization is inconsistent and real-provider inference cases are blocked.
- Local retrieval has strong deterministic exact-term performance in the supplemental artifact, but an empty profile fabricates a default domain and semantic retrieval is not evaluated by the current labels.
- Planner accepts an empty plan and has no post-model coverage/role/difficulty invariant.
- Question generation relies on prompt compliance; empty/misaligned output passes, normal history is absent, and supplemental artifact flags 80.67% repeated openings and 70.67% possible unsupported-experience assumptions pending human review.
- Evaluator enforces numeric ranges but not answer emptiness, duplicate-score consistency, score-feedback consistency, verbosity bias, or keyword bias.
- Orchestrator skips readiness at start and does not protect duplicate session creation.
- Report generation has both snapshot contamination and no aggregate/narrative consistency gate.
- Frontend protects same-component double clicks for start/answer and deduplicates report requests, but upload lacks an in-flight ref/idempotency key and Candidate Profile Review is read-only.

## 7. Top Failure Cases

| Rank | Test ID | Failure Scenario | Impact | Current Result |
| ---: | ------- | ---------------- | ------ | -------------- |
| 1 | REPORT-006 | Old session report uses newly edited profile | Historical report can claim unevaluated skills or omit evaluated ones | FAIL |
| 2 | FLOW-001 | Non-ready profile starts | Empty/garbage profile propagates through all AI agents | FAIL |
| 3 | EVAL-014 | 9/10 with “largely incorrect” feedback | Corrupt coaching and downstream report | FAIL |
| 4 | EVAL-016 | Nested overall=1, top overall=9 | Different consumers may use different scores | FAIL |
| 5 | REPORT-001 | 9/10 produces no_hire/poor summary | Final report contradicts evidence | FAIL |
| 6 | QGEN-001 | React/easy receives Kubernetes/hard | Hallucinated experience and wrong difficulty | FAIL |
| 7 | QGEN-003 | Empty question accepted | Empty UI/audio turn or broken interview | FAIL |
| 8 | UX-003 | Same Resume/key creates two candidates | Duplicate profiles and state ambiguity | FAIL |
| 9 | UX-002 | Rapid start creates two sessions | Duplicate interviews and model cost | FAIL |
| 10 | RESUME-011 | Two multipart files accepted | Wrong selected Resume can be processed silently | FAIL |
| 11 | RAG-005 | Empty profile retrieves AI Engineer | Wrong context seeds planner hallucination | FAIL |
| 12 | PLAN-001 | Empty plan becomes generic question | Silent upstream failure propagation | FAIL |
| 13 | QGEN-002 | No normal question history in prompt | Semantic repetition across interview | FAIL |
| 14 | EVAL-001 | Empty answer can score 9 in isolation | Evaluator fails open outside HTTP guard | FAIL |
| 15 | BOUNDARY-002 | Arbitrary question count accepted | Unbounded duration/cost and poor UX | FAIL |
| 16 | PROFILE-005 | Unicode-equivalent skills duplicate | Polluted plan/RAG/question coverage | FAIL |

## 8. AI-Specific Weaknesses

- **Hallucination:** QGEN-001 proves there is no application gate against a schema-valid unsupported Kubernetes assumption. The supplemental artifact flags 106/150 questions (70.67%) with conservative unsupported-experience patterns; because human review is pending, this is **PARTIAL evidence**, not 106 confirmed hallucinations.
- **Grounding:** Supplemental deterministic grounding overlap is 0.3049 and LLM-judge retrieval grounding is 1.42/2. The benchmark intentionally strips real project/experience prose, so it cannot establish deep experience grounding.
- **Duplicate Questions:** QGEN-002 shows normal generation has no history. Supplemental exact duplicate rate is low (0.67%), but opening-phrase repetition is 80.67%; semantic duplicate rate remains **BLOCKED/NOT EVALUATED**.
- **Difficulty Alignment:** Fault-injected wrong difficulty passes unchanged. Supplemental exact difficulty-label match is 83.33%, leaving 25/150 mismatches.
- **Role Alignment:** Supplemental LLM judge reports 100% role relevance on redacted, catalog-selected profiles, but QGEN-001 shows no deterministic enforcement under provider drift or malformed valid output.
- **Score Bias:** Live EVAL-002 through EVAL-013 are blocked by provider configuration. Range validation alone is working; score correctness is not established.
- **Verbosity Bias:** **BLOCKED**. No current live comparison of short-correct versus long-wrong answers could run.
- **Keyword Bias:** **BLOCKED**. The prompt asks for correctness/depth, but no deterministic guard or current provider result prevents keyword stuffing.
- **Evaluator Consistency:** **BLOCKED** for repeated provider calls. Structural inconsistency is already FAIL because two overall-score fields can disagree.
- **Report Consistency:** REPORT-001 and REPORT-006 are executed FAILs. A valid schema does not guarantee consistency with evaluations or immutable historical evidence.

Supplemental artifact integrity:

- `QUESTION_METRICS.json`, `QUESTION_PATTERN_AUDIT.json`, `RETRIEVAL_METRICS.json`, `questions.jsonl`, and `retrieval.jsonl` SHA-256 hashes all match `docs/evaluation/cv_question_rag/RUN_MANIFEST.json`.
- Manifest status is `PARTIAL_PENDING_HUMAN_REVIEW`; completed human reviews are 0/60.
- These metrics are therefore retained as supporting evidence with their original claim boundary.

## 9. Pipeline Failure Propagation

### Chain A — empty profile to hallucinated interview

```text
Resume/Profile has no usable evidence
  -> Interview start skips readiness (FLOW-001)
  -> Local retriever selects AI Engineer on zero evidence (RAG-005)
  -> Planner may accept an empty plan (PLAN-001)
  -> Orchestrator creates generic CV Deep Dive round
  -> Question generator accepts ungrounded/empty output (QGEN-001/QGEN-003)
  -> Evaluator may accept internally inconsistent scores (EVAL-016)
  -> Report has no consistency gate (REPORT-001)
```

### Chain B — historical state contamination

```text
Session created with immutable Profile A snapshot
  -> Candidate Profile later edited/replaced
  -> ReportService reloads current Profile B-like state (REPORT-006)
  -> Report prompt combines old answers/evaluations with new profile skills
  -> Historical coaching report can invent strengths or weaknesses
```

### Chain C — duplicate user action

```text
User retries the same Resume with the same logical attempt
  -> extraction artifact/cache avoids a second LLM call
  -> route still creates a second Candidate Profile (UX-003)
  -> both profiles can be used to start sessions
  -> two rapid start requests create two sessions (UX-002)
  -> duplicated interviews/reports and ambiguous history
```

### Chain D — provider returns malformed but schema-valid quality

```text
Provider returns empty/misaligned InterviewQuestion
  -> Pydantic accepts it (QGEN-001/QGEN-003)
  -> candidate answers an invalid premise or sees empty UI
  -> evaluator receives compromised question context
  -> high/conflicting evaluation can pass (EVAL-014/EVAL-016)
  -> contradictory report can be persisted (REPORT-001)
```

Positive containment observed:

- Out-of-range scores are rejected by Pydantic.
- Markdown fences and leading text around a JSON object are normalized.
- LLM timeouts and malformed JSON are retried and map to a safe 503 at the gateway.
- Answer submission has repository-backed idempotent claims.
- Resume and preparation caches include user/candidate/version inputs and passed isolation tests.

## 10. Recommended Regression Suite

### Smoke

- RESUME-001, RESUME-002, RESUME-010, READY-001, FLOW-001, QGEN-003, FLOW-007, REPORT-006.
- One configured-provider Resume -> plan -> question -> answer -> report path in both `vi` and `en`.

### Agent Regression

- PROFILE-001/004/005 and every shared NFKC normalization vector.
- READY-001 through READY-007.
- RAG-001 and RAG-005, plus a positive-score threshold for domain selection.
- PLAN-001 nonempty plan and bounded rounds.
- QGEN-001/002/003 post-generation quality gate.
- EVAL-001/014/016 cross-field consistency.
- REPORT-001/004/006 aggregate and snapshot invariants.

### AI Quality Regression

- Short-correct vs long-wrong pair.
- Confidently wrong, partially correct, keyword-stuffed, repeated-question, and off-topic answers.
- Vietnamese and mixed-language semantic equivalents.
- Unsupported candidate-experience assumptions and false-premise challenges.
- Five-run score consistency with an explicit maximum spread.
- Semantic question duplication across full history, not only exact strings.
- Report recomputation checks against deterministic evaluation aggregates.
- Complete the frozen 60-case human review before treating LLM-judge scores as release evidence.

### Integration Regression

- Non-ready start blocked identically for text and voice.
- Empty extraction, zero retrieval, empty plan, malformed QGen JSON, score >10, missing evaluation, provider timeout/empty response.
- Resume upload idempotency, multiple-file rejection, lease recovery, replacement atomicity, and stale fencing on SQLite and Firestore.
- Immutable session snapshot and existing-report invariance after profile correction/replacement.
- Concurrent duplicate start policy.

### UX Regression

- Existing double-start and double-answer same-tick tests.
- Upload in-flight lock plus server idempotency key reuse.
- Refresh/back during upload, preparation, interview, and report generation.
- Structured 400/404/409/412/422/429/500/503 messages.
- 1440/1024/768/390 viewport pass, keyboard-only pass, screen-reader smoke, and no horizontal overflow.
- Editable Candidate Profile draft/save/stale conflict/reload flow when implemented.

## 11. Final Verdict

```text
Demo Ready: NO

Production Ready: NO
```

Top 5 blockers:

1. Historical report generation violates the immutable Candidate Profile snapshot contract.
2. Interview start bypasses authoritative Interview Readiness.
3. Resume upload and interview start are not safely idempotent; duplicate resources are reproducible.
4. Question, evaluation, and report agents lack post-model semantic consistency/grounding gates.
5. The current environment has no `GOOGLE_CLOUD_PROJECT`, so live AI quality and end-to-end demo execution are blocked; Candidate Profile correction/replacement flows are also absent from runtime.

Security penetration testing, real Firebase credential behavior, Firestore vector runtime, production data migration, live microphone/speaker quality, real responsive screenshots, keyboard-only navigation, and screen-reader behavior were outside or unavailable in this run. They must not be inferred as passed from the automated results.

### Commands and evidence

```text
backend/.venv/Scripts/python.exe -m pytest evaluation/agent_robustness/test_full_system_agent_robustness.py -q --tb=short
  -> 20 passed, 20 failed

backend/.venv/Scripts/python.exe -m pytest
  -> 286 passed

npm test -- --reporter=junit
  -> 119 passed

python -m pytest evaluation/cv_question_rag/tests -q
  -> 7 passed

npm exec tsc -- -b
npm run lint
npm run build
python -m compileall -q core gateway infrastructure orchestrator services shared speech_service
  -> all passed

live Vertex Gemini probe
  -> BLOCKED: GOOGLE_CLOUD_PROJECT is required for Vertex AI Gemini
```

Evidence files:

- `evaluation/agent_robustness/evidence/robustness-results.xml`
- `evaluation/agent_robustness/evidence/backend-full-results.xml`
- `evaluation/agent_robustness/evidence/frontend-full-results.xml`
- `evaluation/agent_robustness/evidence/cv-question-rag-tooling-results.xml`
- `evaluation/agent_robustness/test_data/synthetic_cases.json`
- `docs/evaluation/cv_question_rag/RUN_MANIFEST.json` (supplemental, pre-existing)

```text
=== FULL SYSTEM AGENT TEST SUMMARY ===

Agents discovered: 13
Tests designed: 70
Tests executed: 40 primary robustness cases

PASS: 20
FAIL: 20
PARTIAL: 0 (primary ledger)
BLOCKED: 18

Critical: 1
High: 8
Medium: 6
Low: 0

Most fragile agent: ReportGeneratorAgent / ReportService
Most serious bug: Historical report uses the latest mutable Candidate Profile instead of the session snapshot
Most important regression testcase: REPORT-006

Demo Ready: NO
Production Ready: NO

Report:
docs/evaluation/FULL_SYSTEM_AGENT_ROBUSTNESS_REPORT.md

Test files created:
evaluation/agent_robustness/test_full_system_agent_robustness.py
evaluation/agent_robustness/test_data/synthetic_cases.json
evaluation/agent_robustness/README.md
```
