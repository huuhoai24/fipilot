# M0 System & Model Audit

## Status

**M0 STATUS: CLOSED**

All 17 exit-gate questions can be answered from the current filesystem. This
status closes only the source/configuration audit. It does not certify model
accuracy, a deployed environment, or the contents of the optional remote
Firestore vector collection.

Audit timestamp: `2026-08-18T18:44:23+07:00`

Git commit: `3a38b4818a0bb4d2c9e51efd013c295a4f039894`

Branch: `feature/ai-lab-vertex`

Working tree: **DIRTY before M0**. The pre-existing changes include an
uncommitted Firestore vector adapter/indexer and a deleted tracked
`backend/evaluation_report.json`. M0 treats the complete current filesystem as
the baseline and does not attribute those changes to this audit.

## Runtime boundary

The active HTTP entry point is `gateway.main:app`, selected by
`scripts/run_backend.ps1`, `scripts/run_backend.sh`, `docker-compose.local.yml`,
and `backend/README.md`. The production-shaped modules are `gateway/`, `core/`,
`infrastructure/`, `services/`, `orchestrator/`, and `shared/`.

`backend/app/` is mainly a compatibility import surface. `backend/ai_lab/` is a
CLI lab with separate schemas/prompts and is not imported by `gateway.main`.
Neither is counted as an additional production execution path.

The repository helper loads `backend/.env.local`. At audit time that file
resolved to Firestore persistence, a remote speech service, Vertex
`gemini-2.5-flash`/`gemini-2.5-pro`, Resume model
`gemini-2.5-flash-lite`, and **local lexical** interview knowledge. The optional
Firestore vector backend is implemented but not enabled by that configuration.

## AI module inventory

| Module | Source and entry point | Input | Output | Runtime/model | Failure and fallback | Existing evaluation |
| --- | --- | --- | --- | --- | --- | --- |
| Resume processing | `gateway/api/resume.py:39`; `infrastructure/documents/pdf_service.py:8` | One multipart `UploadFile`, filename extension, bytes | Extracted plain text | `pypdf` or `python-docx`; no AI at parser stage | Unsupported extension/size/short text rejected; parser exceptions are not comprehensively mapped; no OCR fallback | Framework exists; labelled dataset absent; historical aggregates only |
| Candidate Profile extraction | `services/profile_scanner/agent.py:13` | First 12,000 characters of extracted text | `ResumeExtractionResult` converted to `CandidateProfile` | Vertex `gemini-2.5-flash-lite`, temp 0.1, 60 s, one attempt | Pydantic/provider schema; non-Resume threshold 0.7; no second model/provider fallback | Historical skill aggregates conflict; no reproducible ground truth |
| Interview planning | `services/interview_planner/agent.py:17` | Profile, `InterviewConfig`, retrieved context strings | `InterviewPlan` | Vertex `gemini-2.5-flash`, temp 0.1, 60 s, up to 3 attempts | Invalid/transient output follows shared LLM retry; no alternate provider/model | Synthetic RAGAS-style pilot, not human-labelled accuracy |
| Knowledge retrieval | `core/dependencies.py:288` | Profile + config | Ordered context strings | Active local: deterministic lexical overlap; opt-in: Vertex embeddings + Firestore cosine KNN | Local has no remote failure; vector errors propagate and have no lexical runtime fallback | Synthetic local top-8 pilot; vector retrieval quality not evaluated |
| Question generation | `services/question_generator/agent.py:17` | Profile, one `InterviewRound`, config | `InterviewQuestion` | Vertex `gemini-2.5-flash`, temp 0.2, 60 s, up to 3 attempts | Schema validation and shared retries; no provider fallback | Synthetic judge pilot; historical aggregates only for claimed production quality |
| Voice question streaming | `services/question_generator/streaming_service.py:88` | Same as question generation + delta publisher | Streamed question text and final `InterviewQuestion` | Vertex `gemini-2.5-flash`, temp 0.2, 60 s stream, up to 3 pre-emission attempts | If JSON tail is invalid after spoken text, metadata is rebuilt deterministically from the selected round | Deterministic parsing tests; no labelled quality benchmark |
| Follow-up generation/selection | `orchestrator/interview_orchestrator.py:270`; `orchestrator/follow_up_service.py:8` | Current question probes, evaluator output, memory | Next `InterviewTurn` | Existing probe selected deterministically; otherwise normal Question Generator | Avoids already asked probes; no separate follow-up model or prompt | Unit tests only; no follow-up quality dataset |
| Answer evaluation | `services/answer_evaluator/agent.py:19` | Profile, question/rubric, answer, config | `AnswerEvaluation` | Text: `gemini-2.5-pro`; voice: `gemini-2.5-flash`; temp 0.1; 60 s; 3 attempts | Shared schema/retry behavior; no rule-based scoring fallback | Synthetic judge/repeatability pilot; human MAE/correlation not evaluated |
| Final report | `services/report_generator/agent.py:12` | Profile plus completed `InterviewSessionState` | `InterviewReport` | Vertex `gemini-2.5-pro`, temp 0.1, 60 s, 3 attempts | Existing report is replayed; generation failure propagates; no deterministic report fallback | No report-quality evaluation |
| STT | `infrastructure/speech/stt/faster_whisper.py:127`; remote boundary in `infrastructure/speech/remote.py:80` | 16 kHz PCM16 audio after VAD | Partial/final transcript events | `faster-whisper`; configured speech-service model `large-v3-turbo`, CUDA/int8_float16 in `.env.speech` | Empty transcript returns no event; no alternate STT provider; remote client has no explicit timeout/retry/fallback | Historical WER/CER only; labelled WAV/reference set absent |
| TTS | `infrastructure/speech/tts/vieneu.py:67`; remote boundary at `remote.py:29` | Question text | 24 kHz PCM16 frames | VieNeu mode `v3turbo`, watermark enabled | Errors surface as TTS failure events; no alternate synthesizer; no explicit retry/timeout | Framework measures latency only; no populated dataset |
| Orchestration | `orchestrator/interview_orchestrator.py:32`; `orchestrator/workflow.py:1` | Profile snapshot-in-state, plan, turns, answers, evaluations | Updated `InterviewSessionState` | In-process Python orchestration; **no LangGraph** | Model failures propagate to REST 503 or voice recovery events; deterministic branching/memory remain | Behavioral unit/API tests; no end-to-end accuracy metric |

## Prompt audit

| Component | Prompt location | System instruction and variables | Output/guardrails |
| --- | --- | --- | --- |
| Resume extraction | `services/profile_scanner/prompts.py:6` | Untrusted Resume text (JSON-encoded, first 12,000 chars), supported domains | JSON `ResumeExtractionResult`; ignore document instructions, extract supported facts only, classify non-Resume, cap skills/evidence/projects/experience |
| Planner | `services/interview_planner/prompts.py:7` | Profile, config, retrieved `curated_knowledge` | JSON `InterviewPlan`; evidence-first, no job description, bounded concise areas, language/level/style controls |
| Question | `services/question_generator/prompts.py:14` | Profile, selected round, config/personality | JSON `InterviewQuestion`; one evidence-grounded question, expected points and probes, language control |
| Streaming question | `services/question_generator/prompts.py:71` | Same variables plus serialized schema | JSON object with `question` first; full object is validated after streaming |
| Evaluator | `services/answer_evaluator/prompts.py:7` | Profile, question, answer, config | JSON `AnswerEvaluation`; 0–10 rubric, evidence/rubric inputs, follow-up signal; voice output is shortened |
| Report | `services/report_generator/prompts.py:9` | Profile, config, plan, completed turns | JSON `InterviewReport`; evidence-only coaching, no invented claims, language control |
| Shared wrapper | `services/prompt_builder.py:38` | Task, language, context, agent task | Repeats system/language/task/context sections; no external prompt registry or prompt version persisted |
| Evaluation-only question judge | `services/system_evaluation/judges.py:8` | Synthetic/labelled benchmark case and generated question | JSON `QuestionQualityScore`, temp 0; explicitly outside interview business logic |
| RAGAS-style pilot judges | `evaluation/ragas_pilot/judges.py:11` | Synthetic pilot outputs and versioned rubric | JSON judge schemas, Flash temp 0; evaluation-only |

The LLM adapter also appends a JSON-only instruction and supplies the Pydantic
JSON schema to Gemini (`infrastructure/llm/vertex_gemini.py:182-184,552-557`).
This reduces malformed output. It does not prove factual grounding: only the
Resume prompt tells the model not to invent facts, and no post-generation code
checks extracted values against source spans.

## Dependency and failure chain

All production LLM agents share `VertexGeminiService`. The normal service uses
three attempts with exponential backoff from 0.5 s, capped at 4 s, plus up to
0.1 s jitter. Timeout and common 408/409/429/5xx/transient errors are retryable.
Resume extraction deliberately uses one attempt. JSON validation failures can
be retried only while attempts remain. After exhaustion, the gateway maps
`LLMServiceError` to a generic structured 503. There is no OpenAI-compatible,
local LLM, or secondary provider fallback in the active gateway.

## Architecture versus implementation summary

- `docs/AI_Interview_Platform_Documentation_VI.md` describes obsolete
  OpenAI-compatible/Ollama Gemma, Groq Whisper fallback, and PhoWhisper paths.
  The active gateway uses Vertex Gemini and faster-whisper/VieNeu.
- `docs/BAO_CAO_TONG_QUAN_DU_AN.md:173,976` says knowledge retrieval is only a
  reserved seam. Local lexical retrieval is now wired into the planner, and an
  opt-in Firestore vector adapter exists in the dirty tree.
- `docs/presentation/SYSTEM_TRUTH_MAP.md:28,233-234` correctly describes the
  configured local lexical baseline but its absolute statement that no
  embedding/vector implementation exists is stale relative to the current
  uncommitted adapter.
- The normative Resume Review ADRs/spec require content-based file detection,
  idempotency, replacement upload, Profile PATCH/If-Match, audit/provenance,
  authoritative start readiness, and atomic versioned snapshots. The active
  routes do not implement those contracts. See `IMPLEMENTATION_GAPS.md`.
- `DEPLOYMENT_REPORT.md:80` is a dated phase report that says voice was not
  deployed. Current source contains voice/STT/TTS, but no newer checked-in
  deployment evidence proves that current voice source is live in production.

## M0 exit gate

1. **CV pipeline:** extension check → temporary file → SHA-256 → pypdf or
   python-docx text extraction → 50-character gate → cache/artifact lookup →
   Gemini structured extraction → Pydantic conversion → repository persistence.
2. **Scanned/image Resume:** no OCR/image processing; an image-only file usually
   fails the 50-character gate with 422.
3. **Profile creation:** `ResumeAgent.extract_profile` and
   `ResumeExtractionResult.to_candidate_profile`, persisted by
   `gateway/api/resume.py:142-162`.
4. **Knowledge location:** source Markdown under `Knowledge/`; packaged runtime
   catalog at `backend/services/interview_knowledge/catalog.json`; optional
   vector documents in a Firestore collection when manually indexed.
5. **Knowledge structure:** 10 domains, 4,379 topic records (`title`, `path`,
   `anchors`), and Intern/Junior/Middle/Senior guidance for each domain.
6. **Active retrieval algorithm:** deterministic domain scoring and weighted
   lexical token overlap.
7. **Embedding model:** not used by the configured local baseline; optional
   adapter uses `gemini-embedding-001` at 768 dimensions.
8. **Vector database:** not used by the configured local baseline; optional
   adapter uses Cloud Firestore Vector Search.
9. **Query:** local path recursively collects all string values in the profile;
   vector path uses role/specialization, level, language, skills, and objective,
   excluding identity.
10. **Top-K:** local top 8 topics; optional vector top 5.
11. **Similarity:** local weighted overlap plus exact-title bonus; vector uses
    Firestore cosine distance and displays `1 - distance`.
12. **Models:** enumerated in `MODEL_INVENTORY.md`.
13. **Prompts:** enumerated above and in the component `prompts.py` files.
14. **Evaluation:** executable empty-manifest framework, synthetic RAGAS-style
    pilot artifacts, deterministic tests, and unsupported historical aggregates.
15. **Ground truth:** no populated verified production ground-truth dataset;
    synthetic expected topic IDs exist only for the controlled local pilot.
16. **Historical metrics:** Resume, STT, question, and answer aggregates in
    `evaluation/evidence/` are historical only.
17. **Mismatches:** documented above and expanded in `IMPLEMENTATION_GAPS.md`.

## Files consulted

Primary evidence included `gateway/main.py`, dependency construction in
`core/dependencies.py`, settings/environment loaders, every active AI agent and
prompt, shared schemas, both repository adapters, document/speech adapters,
orchestration, knowledge build/index code, evaluation framework and artifacts,
README/deployment/architecture documents, Resume Review ADRs/specifications,
and current Git state.

## Validation results

All validation was run after creating only the M0 documentation. No unrelated
failure was repaired.

| Command | Result | Passed | Failed | Skipped | Environment issue |
| --- | --- | ---: | ---: | ---: | --- |
| `backend/.venv/Scripts/python.exe -m pytest` from `backend/` | PASS | 264 | 0 | 0 | One Starlette/httpx deprecation warning; non-failing |
| Focused AI/Resume/retrieval/planner/question/evaluator/orchestrator/report/evaluation tests | PASS | 64 | 0 | 0 | Same non-failing deprecation warning |
| `backend/.venv/Scripts/python.exe -m pytest evaluation/ragas_pilot/tests -q` | PASS | 15 | 0 | 0 | None |
| `python -m compileall -q core gateway infrastructure orchestrator services shared speech_service` | PASS | N/A | 0 | N/A | None |
| `npm exec tsc -- -b` | PASS | N/A | 0 | N/A | None |
| `npm run lint` | PASS | N/A | 0 | N/A | None |
| `npm test -- --run` | PASS | 119 tests in 18 files | 0 | 0 | None |
| `npm run build` | PASS | Build completed | 0 | N/A | Vite emitted a non-failing plugin timing advisory |

No checked-in Playwright command/workflow was found for this documentation-only
change, and no user-visible responsive behavior changed, so visual/keyboard
smoke checks were not applicable to M0.
