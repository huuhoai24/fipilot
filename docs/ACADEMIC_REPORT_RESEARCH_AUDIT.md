# Academic Report Research Audit

Audit date: 2026-08-20

Repository revision: `78048d410e67df3e882fc469727c1f52915f0242` (`feature/ai-lab-vertex`)

Worktree state: dirty; the architecture suite and most M1-M8 executable evaluation material are untracked

Scope: report/manuscript assets, implemented system, architecture diagrams, evaluation and experiment evidence, and tests

> **Post-audit build addendum (2026-08-20):** This document records the evidence boundary before manuscript construction. The resulting `report/Final_report.tex` now compiles to a 115-page `report/Final_report.pdf`. Twenty selected existing Mermaid sources were rendered to tightly bounded high-resolution publication figures and visually sampled; all 20 succeeded. The full 95-source suite also retains its static-validator PASS. Statements below that a report/toolchain or Mermaid rendering is absent describe the pre-build audit state and are superseded for those deliverables only; the suite remains untracked until the user chooses to add it to Git.

## Evidence policy and status vocabulary

This audit treats executable source, checked-in schemas/configuration, checked-in test source, and machine-readable result artifacts as primary repository evidence. Narrative reports are accepted only within the boundaries stated by their manifests and limitations. A result produced from a dirty tree is historical evidence for that recorded run, not proof of the current checkout. Untracked files are explicitly flagged because a clean clone cannot reproduce or review them.

| Label | Meaning in this audit |
| --- | --- |
| **IMPLEMENTED** | Executable runtime source exists and is connected to an active entry point. |
| **PARTIAL** | A working seam exists, but its contract, operational proof, or evidence quality is incomplete. |
| **SPEC-PENDING** | A binding ADR/spec requires the behavior, but active runtime source does not implement it. |
| **NOT IMPLEMENTED** | Neither an active runtime/report artifact nor a binding implementation is present. |
| **EXPERIMENTAL** | Prototype, shadow, evaluation-only, or untracked worktree behavior; not the default production path. |

## Executive findings

1. **There is no academic-report build.** No `report/` directory, `.tex`, `.bib`, `.sty`, `.cls`, or report PDF exists. The required destination therefore is this file under `docs/`.
2. **The application pipeline is substantially implemented**, including Resume extraction/OCR, Candidate Profile creation, planning, question generation, text and voice answer handling, LLM evaluation, and report generation. Several normative Candidate Profile contracts remain **SPEC-PENDING**, especially correction/replacement upload, mutation preconditions, start-readiness enforcement, and immutable report provenance.
3. **Quantitative evidence is controlled rather than real-world.** M1-M7 contain useful tracked reports and JSON metrics, but their manifests disclose synthetic or automated-reference labels, dirty execution trees, missing expert human ground truth, and no production activation for vector/RAG or evaluator changes.
4. **Reproducibility is the largest research-packaging risk.** The 70 tracked `docs/evaluation/**` artifacts are separated from 1,651 untracked evaluation paths containing most M1-M8 runners, fixtures, raw records, caches, and newer defense evidence.
5. **The new architecture suite is useful but untracked.** It contains 95 Mermaid sources and passes its static validator, but it has not been parsed/rendered by Mermaid CLI or a browser.
6. **Tracked presentation evidence is stale.** The presentation package was generated at revision `51fc3b57` and says empirical metrics are `N/A` and vector retrieval is absent, while later checked-in M1-M8 reports and current source establish newer controlled evidence and an opt-in Firestore vector adapter.

## 1. Report and publication-asset inventory

| Asset | Tracking | Status | Audit finding |
| --- | --- | --- | --- |
| `report/` | absent | **NOT IMPLEMENTED** | No conventional manuscript directory exists. |
| LaTeX/BibTeX (`*.tex`, `*.bib`, `*.sty`, `*.cls`) | absent | **NOT IMPLEMENTED** | No typesetting source, bibliography database, citation keys, or reproducible paper build exists. |
| Academic/report PDF | absent | **NOT IMPLEMENTED** | The 25 PDFs found in the worktree are untracked evaluation Resume/invalid-file fixtures, not a report. No PDF is tracked. |
| `docs/BAO_CAO_TONG_QUAN_DU_AN.md` | tracked | **PARTIAL** | Broad Vietnamese project report and a useful prose seed, but not a source-linked academic manuscript. |
| `docs/AI_Interview_Platform_Documentation_VI.md` and `.docx` | tracked | **PARTIAL** | Project documentation exists in Markdown and a 43,029-byte Word file. The Word content describes older modules/routes and legacy Gemma/Ollama behavior, so it cannot be treated as current implementation truth without rewriting. |
| `docs/PIPELINE_CV_TO_INTERVIEW_DEEP_DIVE_VI.md` | tracked | **IMPLEMENTED evidence / PARTIAL freshness** | Best detailed architecture/runtime narrative. It explicitly separates implemented and pending behavior and identifies source conflicts; runtime source remains controlling. |
| `docs/SYSTEM_DESIGN_VI.md` and `docs/local-architecture.md` | tracked | **PARTIAL** | Useful system/deployment narratives, but design recommendations and live-deployment claims must remain distinct. |
| `docs/presentation/**` | tracked | **PARTIAL / stale snapshot** | Contains a prior evidence audit, 33-slide plan, screenshot evidence, four PNG screenshots, and a ZIP. Its manifest is bound to revision `51fc3b57`, earlier than the current evaluation work. |
| `docs/diagrams/*.svg` | tracked | **IMPLEMENTED asset** | Five figures: system context, container architecture, text sequence, voice sequence, and data model. All five parse as well-formed XML. XML validity is not semantic or visual correctness. |
| `docs/architecture/**` | untracked | **EXPERIMENTAL** | Six architecture documents and 95 Mermaid files form the most complete current architecture suite, but are absent from a clean clone until added. |
| `FS_CV_VoQuangTrieu.docx` | tracked | **PARTIAL / privacy risk** | A candidate Resume-like Word asset is tracked at repository root. It must not be embedded, quoted, or distributed with an academic artifact without an explicit consent/redaction decision. |

Tracked publication-ready visual assets have exact sizes: four screenshots at 101,556, 87,792, 108,830, and 56,126 bytes; five SVG diagrams at 6,188, 8,142, 6,051, 6,117, and 8,144 bytes. Their provenance is documented in `docs/presentation/PACKAGE_MANIFEST.md` and `docs/presentation/PRODUCT_SCREENSHOT_EVIDENCE.md`.

## 2. Current implementation matrix

Runtime source, not the older `.docx` or presentation package, controls these classifications.

| Capability | Status | Direct evidence and report-safe interpretation |
| --- | --- | --- |
| React web application | **IMPLEMENTED** | Production routes are declared in `frontend/src/App.tsx`; Candidate Profile, text interview, speech interview, history, report, and settings pages have tracked RTL tests. |
| FastAPI gateway | **IMPLEMENTED** | `backend/gateway/main.py:87` constructs the active app. REST routes live in `backend/gateway/api/**`; voice uses `/api/v2/voice/interview/{session_id}` in `voice.py:169`. |
| Firebase authentication and ownership | **IMPLEMENTED** | `backend/core/dependencies.py:169-205` resolves Firebase/current user behavior; routes pass `current_user.uid` into owned repository operations. This supports an implementation claim, not a compliance certification. |
| PDF/DOCX validation and extraction | **IMPLEMENTED** | `backend/infrastructure/documents/**` validates document structure and performs native extraction; `backend/app/tests/test_document_processing.py:26-130` covers mismatch, malformed DOCX, OCR, and OCR failure/timeout. |
| OCR fallback | **IMPLEMENTED** | Sparse/image PDF paths invoke injected/local OCR and return structured method/warnings. This conflicts with the older wording of ADR 0004 and should be described as a documented architecture drift. |
| LLM Candidate Profile extraction | **IMPLEMENTED** | `ResumeAgent.extract_raw()` calls typed JSON generation with task `simple` and temperature `0.1` (`backend/services/profile_scanner/agent.py:35-50`). |
| Candidate Profile schema | **IMPLEMENTED** | Canonical model is `backend/shared/schemas/candidate.py:38`; no report should use legacy aliases from the old Word document. |
| Post-LLM source verification/provenance | **PARTIAL** | Rule-based reconciliation exists, but the deep dive records that full provenance is not persisted/returned (`docs/PIPELINE_CV_TO_INTERVIEW_DEEP_DIVE_VI.md:287-319`, `1089`). |
| Profile GET, ETag, readiness response | **IMPLEMENTED** | Candidate Profile GET and the shared validator exist (`backend/services/candidate_profile/readiness.py:17`; deep dive lines 408-455). |
| Profile correction, replacement upload, versioned mutation | **SPEC-PENDING** | No PATCH/replacement route implements the ADR contract; the deep-dive matrix marks profile increment, PATCH/If-Match, durable editing, and replacement upload pending (`1096-1101`). |
| Upload idempotency/status/lease/fencing | **SPEC-PENDING** | Required by ADR 0005/0009 and repository instructions, but current upload remains synchronous and lacks these resources (`docs/PIPELINE_CV_TO_INTERVIEW_DEEP_DIVE_VI.md:962`; matrix lines 1091-1093). |
| Start-readiness enforcement | **SPEC-PENDING** | `backend/gateway/api/interview.py:111-177` loads the owned profile and creates a plan/session without calling the readiness validator. |
| Interview planning | **IMPLEMENTED** | Planner retrieves knowledge and calls typed Gemini output at temperature `0.1` (`backend/services/interview_planner/agent.py:26-60`). |
| Default lexical retrieval | **IMPLEMENTED** | `LocalKnowledgeRetriever` performs deterministic weighted token overlap and exact-title bonus, selects a domain, and returns up to eight catalog topics (`backend/services/interview_knowledge/local.py:82-142`). |
| Firestore vector retrieval | **IMPLEMENTED opt-in / PARTIAL operational proof** | The dependency factory can select `firestore_vector`; Vertex query embeddings and Firestore cosine KNN are implemented (`backend/core/dependencies.py:288-327`; `backend/infrastructure/interview_knowledge/firestore_vector.py:18-171`). Default remains `local`. |
| Question generation | **IMPLEMENTED** | Typed Gemini generation uses `simple` routing and temperature `0.2` (`backend/services/question_generator/agent.py:20-49`). |
| Answer evaluation | **IMPLEMENTED / PARTIAL empirical trust** | Text uses configured `complex` routing; voice forces `simple`; both use temperature `0.1` (`backend/services/answer_evaluator/agent.py:30-62`). M7 says production score trust is not established. |
| Adaptive decision policy | **IMPLEMENTED** | `backend/orchestrator/decision_service.py:6-38` applies deterministic score thresholds, including score `>=8` for difficulty increase. |
| Answer-submission idempotency | **IMPLEMENTED** | Persistent per-turn claim/replay behavior is tested in `backend/app/tests/test_answer_submission_idempotency.py:130-246`. This does not imply Resume upload idempotency. |
| Text interview loop | **IMPLEMENTED** | Orchestrator creates plans/turns, evaluates answers, selects follow-ups, persists state, and prefetches text questions (`backend/orchestrator/interview_orchestrator.py`). |
| Voice interview loop | **IMPLEMENTED source / PARTIAL production evidence** | WebSocket auth, STT/VAD, TTS, barge-in, transcript, and shared answer submission are present. Production load/reliability and real STT/TTS quality are not established. |
| Session snapshot | **PARTIAL** | Profile content is copied into session state, but selection/version persistence is not the required atomic immutable snapshot transaction (`docs/PIPELINE_CV_TO_INTERVIEW_DEEP_DIVE_VI.md:671-681`). |
| Final report generation | **IMPLEMENTED / PARTIAL correctness** | Structured Gemini report uses complex routing at temperature `0.1` (`backend/services/report_generator/agent.py:16-31`) and sequential reuse exists. However, `ReportService.generate_for_session()` reloads the current Candidate Profile (`backend/services/report_generator/service.py:35-42`) instead of using the session snapshot. |
| SQLite and Firestore repositories | **IMPLEMENTED / PARTIAL contract parity** | Both adapters implement the public repository seam and ownership tests exist; atomic Profile Version/upload/snapshot contracts are pending. |
| Observability | **PARTIAL** | Structured timing/logging and voice latency registry exist, but no repository evidence establishes a complete metrics/tracing backend or production SLO monitoring. |
| CI/CD validation | **NOT IMPLEMENTED** | `git ls-files .github/workflows` returns zero. Validation is local/manual. |
| Academic manuscript toolchain | **NOT IMPLEMENTED** | No manuscript source, bibliography, figure build, citation check, or PDF build command exists. |

### Current model and retrieval configuration

The checked-in defaults in `backend/core/settings.py:44-63` and `164-173` are:

| Task/path | Default model or algorithm | Temperature/task details |
| --- | --- | --- |
| Resume extraction | `gemini-2.5-flash-lite` | `0.1`, simple, dedicated global endpoint, one attempt in dependency factory |
| Planning | `gemini-2.5-flash` | `0.1`, simple |
| Question generation | `gemini-2.5-flash` | `0.2`, simple |
| Text answer evaluation | `gemini-2.5-pro` | `0.1`, configured complex task |
| Voice answer evaluation | `gemini-2.5-flash` | `0.1`, forced simple task |
| Report generation | `gemini-2.5-pro` | `0.1`, complex |
| Default knowledge retrieval | weighted lexical | local catalog, topic limit 8 |
| Opt-in vector retrieval | `gemini-embedding-001` + Firestore KNN | global, 768 dimensions, configured default Top-K 5 |
| Local speech | faster-whisper `large-v3`; VieNeu `v3turbo` | Vietnamese default; Silero VAD; source-level implementation only |

These are static defaults, not proof of the values used by an arbitrary deployment. Environment variables can override them.

## 3. Architecture and diagram inventory

### Tracked diagrams

`docs/diagrams/` contains five SVG diagrams covering system context, containers, text sequence, voice sequence, and data model. All five passed an XML parse during this audit. Their conceptual source snapshot predates current vector/evaluation work; use the current source tree to review labels before publication.

### Untracked Mermaid suite

The worktree contains 95 `.mmd` files plus `docs/architecture/DIAGRAMS.md`, `DIAGRAM_INDEX.md`, `SYSTEM_INVENTORY.md`, `ARCHITECTURE_GAPS.md`, `RESEARCH_EVIDENCE.md`, and `README.md`. All 101 documentation paths and `scripts/docs/validate_mermaid.ps1` are untracked.

Fresh static validation result:

| Check | Result |
| --- | ---: |
| Standalone `.mmd` files | 95 |
| Indexed diagrams | 95 |
| Narrative sections | 95 |
| Mermaid fences | 95 |
| Evidence fields | 95 |
| Flowcharts | 76 |
| Sequence diagrams | 8 |
| Class diagrams | 7 |
| State diagrams | 3 |
| ER diagrams | 1 |
| Static validator | PASS |

Validity boundary: the validator checks manifest/declaration structure, balanced delimiters, forbidden HTML/fences, metadata, coverage, and status labels. Neither Mermaid CLI nor a browser-render test is installed or recorded. Therefore the correct claim is **static structure PASS; render validity NOT VERIFIED**.

The suite is academically useful because it explicitly labels `IMPLEMENTED`, `PARTIAL`, `SPEC-PENDING`, and offline paths. It becomes publication evidence only after it is tracked, reviewed against the final commit, rendered, and exported to stable vector/raster figures with captions and source revision.

## 4. Evaluation and experiment inventory

### Provenance boundary

- Exactly 70 paths under `docs/evaluation/**` are tracked.
- The current worktree has 1,651 untracked evaluation paths: 55 under `docs/evaluation/defense_extension`, 7 under `docs/evaluation/defense_final`, 9 under `evaluation/defense_extension`, and 1,580 under `evaluation/m1` through `evaluation/m8`.
- The M1-M8 narrative/metric outputs are mostly tracked, but their runners, frozen datasets, raw samples, caches, and tests are mostly untracked. A clean checkout therefore cannot reproduce most milestones from the checked-in reports alone.
- Several run manifests explicitly record `dirty_tree: true` or dirty Git state. Report claims must be tied to each manifest's exact commit, hashes, model configuration, dataset class, and limitations.

### Tracked evaluation milestones and directly supported results

| Milestone | Status | Exact directly supported evidence | Academic claim boundary |
| --- | --- | --- | --- |
| M0 audit | **IMPLEMENTED methodology** | `docs/evaluation/m0/**` inventories system, models, RAG, CV processing, and gaps. | Method definition and historical audit only; not a performance result. |
| RAGAS-style pilot | **EXPERIMENTAL** | Tracked runner/results use 10 retrieval queries, 10 question generations, and 40 answer samples. `ragas_installed=false`; zero official RAGAS metrics; 122 logical model calls; visible-token cost estimate `$0.423725`. Retrieval Hit@8/Recall@8/MRR@8 were `1.0/1.0/1.0`; answer controlled set was declared invalid with `0/10` validated groups. | Call it a custom RAGAS-inspired smoke, never an official RAGAS benchmark or validated answer-accuracy study. Sources: `evaluation/ragas_pilot/run_manifest.json` and the three `summary.json` files. |
| M1 baseline | **IMPLEMENTED controlled evaluation** | 30 synthetic Resumes: micro-F1 `0.947808`, macro-F1 `0.921840`, Experience F1 `0.721311`; 50 controlled retrieval cases: Hit@3 `0.98`, MRR@8 `0.911667`; 30 generated-question cases; 40 answer cases with pairwise ordering `0.783333` and Spearman tier correlation `0.722441`. Models: Resume Flash-Lite, planner/question/judges Flash, text evaluator Pro, voice evaluator Flash. | No human-labelled production ground truth. Question/feedback semantic values are LLM-as-judge quality scores. The manifest ran from a dirty tree at commit `3a38b481...`. Source: `docs/evaluation/m1/M1_METRICS.json`, `RUN_MANIFEST.json`. |
| M2 Resume upgrade | **IMPLEMENTED controlled evaluation** | Same 30-case controlled comparison: Experience F1 `1.0000`, skills F1 `0.9772`, micro-F1 `0.9853`, post-old-cutoff boundary recall `1.0000`; six image-only OCR fixtures had success `1.0000`; four invalid/mismatched files were added. 54/55 paid attempts reported tokens; known subtotal `$0.019958`, conservative estimate `$0.021275`. Model: `gemini-2.5-flash-lite`, temperature `0.1`. | Synthetic English fixtures do not establish noisy-photo, handwriting, multilingual, or real-CV generalization. Source: `docs/evaluation/m2/M2_RESUME_UPGRADE_REPORT.md`, `M2_METRICS.json`, `RUN_MANIFEST.json`. |
| M3 corpus | **EXPERIMENTAL shadow preprocessing** | 4,419 Markdown documents (4,379 domain topics + 40 level guides) produced 4,492 chunks; exact duplicate analysis found 673 groups/1,533 members; 3,446 chunks were classified tiny; source-token coverage was `128263/128263`; validation passed with 0 errors and 3,446 warnings; model/embedding calls `0`. | This is deterministic offline corpus construction, not active production indexing or proof of retrieval quality. Source: `docs/evaluation/m3/M3_KNOWLEDGE_REPORT.md`, `M3_METRICS.json`. |
| M4 vector shadow | **EXPERIMENTAL shadow retrieval** | 4,492/4,492 valid 768D `gemini-embedding-001` document vectors; stress vector Hit@5 `0.98`, Recall@5 `0.9567`, MRR@8 `0.8087`, versus stress lexical `0.44/0.42/0.2467`; 100-case local/Firestore first-result and rank agreement `1.0`; one live end-to-end sample took `19,982.34 ms`; 86 provider requests; estimated Vertex cost `$0.062286`. | Shadow index only; N=1 live timing is not generalizable and cost is an estimate, not an invoice. Source: `docs/evaluation/m4/M4_VECTOR_SHADOW_REPORT.md`, `M4_METRICS.json`. |
| M5 retrieval benchmark | **IMPLEMENTED evaluation / no production activation** | Frozen set 120 cases: 72 development and 48 holdout, plus preserved M1/M4 sets. Holdout lexical/vector/hybrid Recall@5: `0.6667/1.0000/1.0000`; MRR@8: `0.6562/0.9531/0.9688`. Frozen hybrid: RRF `k=60`, weights `.75/1.0`, candidate depth 8, output Top-K 8. Recommendation `INSUFFICIENT_EVIDENCE`; activation `NO`. | Labels are source-derived/synthetic, not human-labelled production judgments. Source: `docs/evaluation/m5/M5_RETRIEVAL_BENCHMARK.md`, `M5_METRICS.json`, `RETRIEVAL_DECISION.md`. |
| M6 question quality/RAG ablation | **IMPLEMENTED evaluation / no production activation** | 80 scenarios, development 48, holdout 32, four conditions: no RAG, lexical, vector, hybrid. Holdout technical validity `1.0000/1.0000/0.9688/0.9688`; difficulty exact `0.8750/0.9375/0.9062/0.9062`; grounding for lexical/vector/hybrid `1.6562/1.8750/1.6875`; hallucination `0` in all conditions. QG Flash `0.2`; blinded judge Pro `0`; human-review pack 20 scenarios/80 outputs remained pending. | The raw retrieved block was evaluation-only and the holdout had no Vietnamese cases. `QG_ACCEPTABLE`, but RAG recommendation `INSUFFICIENT_EVIDENCE`, activation `NO`. Source: `docs/evaluation/m6/M6_QUESTION_QUALITY_REPORT.md`, `M6_METRICS.json`. |
| M7 answer evaluation | **IMPLEMENTED evaluation / PARTIAL trust** | Frozen 20 groups/80 answers: development 12/48, holdout 8/32. Holdout Text/Voice automated-reference MAE `1.2982/1.2443`, Spearman `0.9540/0.8894`, pairwise ordering `95.83%/89.58%`, strict monotonic groups `75.0%/37.5%`, critical-error detection `87.5%/87.5%`. Text Pro and Voice Flash, both `0.1`. | No expert-human ground truth; correlated Gemini-family bias. Milestone closed, evaluator engineering targets not passed, production score trust not established. Source: `docs/evaluation/m7/M7_ANSWER_EVALUATION_REPORT.md`, `M7_METRICS.json`. |
| M7.1 calibration | **PARTIAL** | A2 development used 48 Text and 48 Voice primary calls plus 40 repeatability calls. It failed frozen gates: Text monotonicity `75%`, cross-mode material disagreement `16.67%`, unsupported feedback Text `16.67%`, Voice `12.5%`. `NO_SAFE_WINNER`; no holdout; conservative envelope `$1.69`. | Evaluation candidate was not activated. Source: `docs/evaluation/m71/M71_EVALUATOR_CALIBRATION_REPORT.md`, `M71_METRICS.json`, `RUN_MANIFEST.json`. |
| M7.2 shared Flash | **PARTIAL** | Stage 0 passed with zero paid calls. Stage 1 ran 8 answers; unsupported feedback `25%` exceeded the `12.5%` smoke ceiling; Stage 2/holdout/repeatability were not run. Incremental estimate `$0.035239`; candidate `gemini-2.5-flash`, temperature `0.1`, thinking budget 0. | Directional N=8 smoke only; not activated. Source: `docs/evaluation/m72/M72_SHARED_FLASH_EVALUATION_REPORT.md`, `M72_METRICS.json`. |
| M8 tracked report | **PARTIAL** | Tracked report says zero-cost Phase A passed `10/10`; Phase B's one Text and one Voice scenario failed before accepted technical completion; actual provider spend was unknown; Phase C not run. | End-to-end live completion/report consistency remains unmeasured in tracked evidence. Source: `docs/evaluation/m8/M8_REPORT.md`. |

### Untracked defense and newer worktree evidence

These artifacts may inform future work but must be labelled **EXPERIMENTAL / UNTRACKED** in a report:

- `docs/evaluation/defense_extension/e3_ablation/**` reconstructs 20 Vietnamese cases across Profile-only, lexical, and vector conditions with zero new provider calls. Technical validity is `0.95` in all three; retrieval-grounding/utilization credit is `0.10` lexical versus `0.90` vector; vector retrieval P50/P95 is `376.01/405.23 ms` versus lexical `5.57/7.70 ms`. The selection gate was explicitly not run because available relevance is an offline oracle.
- `docs/evaluation/defense_extension/e4/HUMAN_VS_AI_METRICS.json` has `human_reviewers=0`, `n=0`, all comparison metrics null, status `BLOCKED`.
- `docs/evaluation/defense_extension/e5/PERFORMANCE_REPORT.json` has no live sessions and all latency metrics null, status `NOT TESTED`.
- `docs/evaluation/defense_final/RUN_MANIFEST.json` explicitly names untracked `evaluation/m1` through `evaluation/m8` as a reproducibility blocker and records zero extension provider calls/new live sessions.
- A newer untracked `evaluation/m8/evidence/phase-b-m82-authorized/PHASE_B_VERDICT.json` reports two completed live journeys, 11 unique successful attempts, and a `$0.14792` estimate, but report consistency is false and unsupported rates are `1.0` and `0.909091`. It is later worktree evidence and does not replace the tracked M8 conclusion.

## 5. Test evidence

### Current source inventory

| Suite | Tracking | Files | Static test definitions/blocks | Evidence boundary |
| --- | --- | ---: | ---: | --- |
| Backend `backend/app/tests` | tracked | 43 | 282 definitions | Current collection discovers 286 test cases because parametrization affects collected count. |
| Frontend | tracked | 18 | 116 `it`/`test` blocks | Static count only; no fresh full frontend run was performed for this audit. |
| RAGAS pilot | tracked | 9 | 15 definitions | Tests custom pilot data/metrics/contracts, not official RAGAS. |
| M1-M8 evaluation suites | untracked | 57 | 156 definitions | Not reproducible from a clean clone. |
| Defense extension | untracked | 4 | 17 definitions | Worktree-only. |

Fresh audit checks:

- `pytest backend/app/tests --collect-only -q -p no:cacheprovider`: **PASS**, 286 tests collected.
- `pytest evaluation --collect-only -q -p no:cacheprovider`: **FAIL during collection** after 193 items because `evaluation/ragas_pilot/tests/test_metrics.py` conflicts with the already imported `evaluation/m5/tests/test_metrics.py`. Do not claim that a single all-evaluation command currently collects or passes.
- `scripts/docs/validate_mermaid.ps1`: **PASS** with the 95-diagram counts above; this is static validation only.
- Tracked CI workflows: **0**.

Historical result artifacts are not fresh validation. `docs/evaluation/m8/M8_REPORT.md` records 281 backend, 154 evaluation, and 119 frontend tests passing for its run; the later untracked defense manifest records 286 backend and selected 66 evaluation tests. The counts reflect different snapshots/scopes and must be cited with their respective manifests rather than merged.

The tracked tests cover core behavioral seams: ownership, Resume validation/OCR, Profile readiness, SQLite/Firestore parity, local/vector knowledge retrieval, planner/question/evaluator agents, orchestration decisions, answer idempotency, reports, voice WebSocket/STT/TTS behavior, frontend upload/profile/interview/report flows, and accessibility-facing interactions. Missing tests do not automatically imply missing implementation, but they limit claims of system reliability.

## 6. Missing evidence and claim restrictions

| Missing or weak evidence | Status | Consequence for an academic report |
| --- | --- | --- |
| Expert human scoring benchmark | **NOT IMPLEMENTED** | Do not claim human agreement, human-level scoring, evaluator accuracy, or validated hiring reliability. |
| Completed blinded M6 human review | **PARTIAL** | LLM-judge question-quality results cannot be generalized as human preference or correctness. |
| Real-world Resume corpus with consent and labels | **NOT IMPLEMENTED** | M1/M2 support controlled synthetic performance only. Do not claim production Resume accuracy. |
| Real STT WER/CER and subjective TTS quality | **NOT IMPLEMENTED** | Voice implementation can be described, but speech quality cannot be quantified from current evidence. |
| Complete current live E2E benchmark | **PARTIAL** | Tracked M8 is blocked; newer untracked evidence still fails report consistency/unsupported-claim criteria. |
| Current production deployment verification | **PARTIAL / unknown** | Deployment files show deployability, not current live state, traffic, reliability, or scale. |
| Provider invoice-backed cost | **PARTIAL** | Use “estimate” and preserve missing-token/failed-call telemetry limitations. |
| Statistical confidence intervals/power plan | **PARTIAL** | Most milestone tables report point estimates on small controlled sets. Avoid population-level claims and significance language unless recomputed under a predeclared method. |
| Independent judge family | **NOT IMPLEMENTED** | Gemini generation/evaluation/reference use creates correlated-model-family bias. |
| Reproducible clean-clone experiment package | **NOT IMPLEMENTED** | Track runners, frozen data permitted for distribution, manifests, raw outputs or immutable hashes, and environment lock before publication. |
| Mermaid render validation and stable figure export | **NOT IMPLEMENTED** | Do not publish screenshots of unverified diagrams as final figures. |
| Citation database and related-work primary sources | **NOT IMPLEMENTED** | Repository-only evidence supports implementation/method claims, not scholarly related-work claims. |
| Research ethics/privacy statement | **NOT IMPLEMENTED** | Must address Resume personal data, external LLM transfer, retention, consent, and the tracked candidate document without asserting unsupported compliance. |
| CI evidence | **NOT IMPLEMENTED** | All validation must be reported as local commands tied to a revision/environment. |

## 7. Academic report gap analysis

### What is ready to write

- **System design and implementation:** The modular FastAPI/React architecture, typed Gemini seams, repository abstraction, Resume pipeline, interview orchestration, text/voice convergence, and status-aware current-vs-target analysis have direct source evidence.
- **Controlled experimental method:** M1-M7 provide dataset counts, models, temperatures, frozen configurations, metric definitions, costs/latencies, and explicit limitations. These support a rigorous controlled-evaluation chapter if every table preserves evidence class and activation status.
- **Negative results:** M5 `INSUFFICIENT_EVIDENCE`, M7 trust failures, M7.1 `NO_SAFE_WINNER`, M7.2 smoke failure, and M8 live blockers are valuable research findings and should not be hidden.
- **Figures:** Five tracked SVGs can seed the report; the 95-diagram suite can supply focused figures after tracking, render validation, simplification, and revision locking.

### What must be created before submission

1. A manuscript source tree with title/abstract, research questions, contributions, method, implementation, experiments, threats to validity, ethics/privacy, limitations, conclusion, appendices, and reproducible build instructions.
2. A bibliography sourced from primary papers/official documentation. Repository documents alone cannot support related-work or foundational-model claims.
3. A claim-to-evidence table that records revision, dataset class, N, split, model, temperature, prompt/config hash, metric implementation, result artifact, and limitation for every number.
4. A clean-clone evaluation package. At minimum, track or archive the allowed M1-M8 runners, frozen datasets, raw/derived evidence, environment/dependency lock, and manifests; exclude secrets, private Resumes, and unnecessary provider caches.
5. A single reproducible validation entry point that avoids the current pytest module-name collision and reports backend/frontend/evaluation/build results against one commit.
6. Publication figures rendered from reviewed diagram sources, with figure IDs, captions, revision hashes, accessible color/text conventions, and explicit `CURRENT`, `EXPERIMENTAL`, or `TARGET` scope.
7. Human validation if the paper's contribution includes evaluator quality or hiring usefulness. Predeclare sampling, reviewer expertise, blinding, rubric, agreement statistic, adjudication, exclusion policy, and confidence intervals before inspecting holdout results.
8. A real-data protocol if claims extend beyond controlled fixtures: consent, de-identification, retention/deletion, permitted provider transfer, sampling frame, label quality, and leakage prevention.

### Recommended claim posture

The strongest defensible thesis today is:

> FiPilot implements an evidence-traceable Resume-to-interview architecture and demonstrates controlled improvements in Resume extraction and retrieval experiments, while controlled ablations and end-to-end gates show that RAG activation, evaluator trust, human agreement, and production readiness remain unestablished.

Avoid these unsupported formulations:

- “The system is production ready.”
- “The evaluator is accurate” or “matches human interviewers.”
- “RAG improves question quality” without naming the condition, N, metric, and controlled/LLM-judged boundary.
- “Vector retrieval is deployed by default.”
- “OCR achieves 100% accuracy”; M2 reports success on six controlled image-only fixtures, not OCR character accuracy.
- “Costs are exact”; most are estimates and some failed-call usage is unknown.
- “All tests pass”; current one-command evaluation collection fails, and no CI workflow exists.

## 8. Primary repository source index

- Runtime authority: `backend/gateway/main.py`, `backend/gateway/api/**`, `backend/core/dependencies.py`, `backend/core/settings.py`.
- Domain/contracts: `backend/shared/schemas/**`, `backend/infrastructure/repositories/base.py`, `CONTEXT.md`, `AGENTS.md`, `docs/adr/**`.
- Resume/Profile: `backend/infrastructure/documents/**`, `backend/services/profile_scanner/**`, `backend/services/candidate_profile/**`.
- Interview/AI: `backend/services/interview_planner/**`, `question_generator/**`, `answer_evaluator/**`, `report_generator/**`, `backend/orchestrator/**`.
- Retrieval: `backend/services/interview_knowledge/local.py`, `backend/infrastructure/interview_knowledge/firestore_vector.py`.
- Voice: `backend/gateway/api/voice.py`, `backend/services/voice_session/**`, `backend/infrastructure/speech/**`, `backend/speech_service/**`.
- Architecture truth: `docs/PIPELINE_CV_TO_INTERVIEW_DEEP_DIVE_VI.md`, `docs/SYSTEM_DESIGN_VI.md`, `docs/local-architecture.md`, `docs/adr/**`.
- Tracked measurements: `docs/evaluation/m1` through `m8`, `evaluation/ragas_pilot/**`.
- Worktree-only experimental evidence: `evaluation/m1` through `m8`, `evaluation/defense_extension/**`, `docs/evaluation/defense_extension/**`, `docs/evaluation/defense_final/**`.
- Tests: `backend/app/tests/**`, `frontend/src/**/*.test.ts(x)`, `evaluation/ragas_pilot/tests/**`, plus untracked milestone suites.

## Audit conclusion

**Overall status: PARTIAL.** The repository contains enough primary implementation evidence and controlled experimental results for a technically honest academic report, but it does not yet contain an academic report, reproducible clean-clone experiment package, human-ground-truth validation, current complete live E2E evidence, or a publication-ready figure/citation toolchain. The report should center traceable architecture, controlled methods, and negative/limiting results rather than claim production or human-equivalent performance.
