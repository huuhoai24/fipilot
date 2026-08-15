# FiPilot Capstone Presentation — Proposed Revision Plan

This plan is based on `SYSTEM_TRUTH_MAP.md`. No edits have been made to the PPTX.
The proposed deck remains a blue/white, clean academic 16:9 presentation and
uses **FiPilot** consistently.

## Mandatory evidence guardrails

- Describe orchestration as ordinary in-process Python; **no LangGraph**.
- Describe retrieval as deterministic packaged-catalog lexical token overlap;
  **no vector database or embeddings**.
- Label the text workflow as production-verified on **2026-07-23** only.
- Label voice as **implemented in source/local/private-service operation;
  production deployment unconfirmed**.
- Show evaluation metrics only as implemented methodology. Current empirical
  results are **N/A / `no_data`**; remove every unsupported number from the
  source deck.
- Treat visible screenshot scores as sanitized demo output, never evaluation
  evidence.

The controlling source citations and exact safe wording are in
`EVALUATION_EVIDENCE_AUDIT.md`.

## Proposed 33-slide structure

| # | Proposed slide | Change from current deck |
| ---: | --- | --- |
| 1 | FiPilot — AI-Powered Interview Training System | Keep visual direction; normalize capitalization and date formatting |
| 2 | Team Members | Keep |
| 3 | Agenda | Rebuild the empty table of contents with the final five sections |
| 4 | Section 01 — Introduction | Keep; normalize section/footer style |
| 5 | Why Interview Preparation Needs Personalization | Keep with minor copy cleanup |
| 6 | Problem Statement & Technical Challenges | Keep |
| 7 | Limitations of Existing Approaches | Keep |
| 8 | Objectives & Technical Contributions | Keep, but describe retrieval precisely |
| 9 | Project Scope | Keep; distinguish text production from voice source/local capability |
| 10 | Out of Scope | Keep |
| 11 | Existing Application Capability Matrix | Keep; clean table alignment and evidence wording |
| 12 | Section 02 — Architecture & System Design | Keep |
| 13 | System Architecture | **Complete redesign.** Layered diagram: Frontend → Firebase Auth / FastAPI API → Orchestrator & agents → repositories → Firestore/SQLite, Vertex AI, private speech service |
| 14 | Deployment Architecture & Trust Boundaries | Move current slide 23 here and replace it. Show confirmed production text path separately from local/target voice worker; label evidence date |
| 15 | Multi-Agent & Orchestration Architecture | Replace current slide 14/part of 20. Show Resume, Planner, Question, Evaluator, Report agents around the in-process orchestrator and deterministic decision service |
| 16 | Adaptive Interview / Session State Flow | New editable state-flow diagram: opening/interviewing → evaluate → follow-up / increase difficulty / next round / finish → closing/report; include persisted state and voice-only memory |
| 17 | Retrieval-Augmented Planning — Lexical, Not Vector | Redesign current slide 15. Show packaged 10-domain/4-level catalog, token-based domain/topic scoring, top-8 bounded context, planner-only use, and explicit “no embeddings/vector DB” note |
| 18 | Data Model, Ownership & Persistence | Merge/improve current slide 17. Show owner-scoped Firestore hierarchy and SQLite local adapter; list canonical Candidate Profile/session/report records |
| 19 | Section 03 — AI Methodology | Replace the current Data and AI section split with one technical-method section |
| 20 | Resume-to-Candidate-Profile Method | Improve current slide 18: PDF/DOCX → temporary file → pypdf/python-docx → SHA/cache → Gemini Flash-Lite structured extraction → Pydantic → owned repository; disclose current upload limitations |
| 21 | AI Model Selection | New matrix: module, actual default model/method, structured/streaming mode, and code-backed selection reason |
| 22 | Question Generation Methodology | New slide: candidate evidence + selected round + config → one typed question; expected answer points and follow-up probes; language/difficulty constraints |
| 23 | Answer Evaluation & Adaptive Decision | New slide: expected points + answer + profile → typed scores/gaps/follow-up signal → deterministic branching rules; separate LLM judgment from rule-based control |
| 24 | Speech Interview Pipeline | New diagram: browser PCM16 → gateway WebSocket → private speech service → Silero VAD/faster-whisper → shared orchestrator → streamed Gemini question → VieNeu-TTS → PCM playback/barge-in |
| 25 | Section 04 — Evaluation & Results | Keep as a section divider with accurate wording |
| 26 | Evaluation Dataset & Readiness | New slide from the implemented manifest: CV, STT, TTS, question, evaluator, and voice-turn slices; disclose that no approved non-empty fixture set exists and state the privacy/provenance gates |
| 27 | Implemented Evaluation Methodology | New metric map: precision/recall/F1, field accuracy, WER/CER, TTS timing ratio, LLM-judge dimensions, evaluator repetitions/MAE, voice p50/p95/failure rate; label every item as implemented methodology, not a measured result |
| 28 | Reproducible Result Status | Replace current slide 22. Show only `status=no_data`, zero cases, the passing framework unit suite, and the empty-manifest rerun; keep qualitative deployment E2E PASS separate and do not convert it into accuracy or latency metrics |
| 29 | Evaluation Readiness / Remaining Evidence Gap | New analysis slide: no approved labelled corpus; required consented/sanitized fixtures, reference transcripts, multi-rater human labels, frozen model/config versions, per-language/domain slices, and production voice benchmark |
| 30 | Section 05 — Demonstration | Keep as a restrained section divider |
| 31 | End-to-End Product Flow | **New evidence-oriented slide using real local UI captures.** Three-stage flow: saved Candidate Profile → active adaptive interview → final coaching report. Use `docs/presentation/screenshots/01-candidate-profile.png`, `02-interview-session.png`, and `03-final-report.png`; retain `04-interview-history.png` as backup evidence. Label all content sanitized demo data and state that displayed report scores are product-output examples, not benchmark results |
| 32 | Contributions, Limitations & Future Work | Merge current slides 26–27; retain source-backed contributions and clearly label production voice and evaluation gaps |
| 33 | Thank You / Q&A | Keep and normalize capitalization/footer |

## Existing architecture SVG evidence

Five already-generated, PowerPoint-readable SVGs are available under
`docs/diagrams/` and are included in the evidence package:

1. `01-system-context.svg`
2. `02-container-architecture.svg`
3. `03-text-interview-sequence.svg`
4. `04-voice-interview-sequence.svg`
5. `05-data-model.svg`

They are supporting architecture evidence, not proof of deployment. When using
the voice diagrams, preserve the source/local/target-production label. Do not
add LangGraph, embeddings, or a vector database. Any new slide-native diagram
should be redrawn with editable PowerPoint shapes while retaining these
evidence boundaries.

## Slides removed or merged

- Current slide 14 and current slide 20 overlap; their content becomes slides
  15, 21, 22, and 23 with clearer technical boundaries.
- Current slide 17 is merged into the storage/data-model slide.
- Current slide 23 is moved out of Evaluation and rebuilt as Architecture slide
  14.
- Current slide 22 is removed because its metrics are unsupported; it becomes
  the four-slide evaluation sequence at slides 26–29.
- Current conclusion slides 26 and 27 are merged to keep the final section
  concise.

## Slide-editing execution notes

- Use `FiPilot` everywhere; remove `FIPILOT`, `Fipilot`, and mixed variants.
- Use the section names in the agenda and running headers exactly.
- Number all content slides consistently as `n / 33`; omit numbering only on
  the title and final Q&A slides.
- Remove stale `33/36`, `34/36`, template-note numbering, and duplicate section
  labels.
- Keep one blue accent family, white backgrounds, Aptos/Satoshi-compatible
  typography, restrained icons, and no decorative gradients.
- Add concise evidence footnotes to technical slides (module paths or deployment
  report date), without shrinking body text below PowerPoint-readable sizes.
