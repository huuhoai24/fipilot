# FULL SYSTEM AGENT ROBUSTNESS REPORT — HISTORICAL POST-FIX BASELINE

> **Current release validation (2026-08-24) supersedes the historical summary below.**
>
> | Metric | Current |
> | --- | ---: |
> | Designed | 74 |
> | Executed | 66 |
> | PASS | 60 |
> | FAIL | 0 |
> | PARTIAL | 3 |
> | BLOCKED | 3 |
> | NOT TESTED | 8 |
> | Confirmed Critical | 0 |
> | Confirmed High | 0 |
>
> Current inventory: backend deterministic **35 PASS / 2 PARTIAL** (37 original cases; one additional evaluator regression also passed), frontend **10 PASS / 1 PARTIAL**, retained Live Azure AI **15 PASS / 1 BLOCKED**, and Speech **2 BLOCKED**. Backend regression is **129/129 PASS**; frontend regression is **28/28 PASS**; frontend robustness has **15/15 executable assertions PASS**; typecheck, build, and Python compile PASS. Lint remains 3 pre-existing `react-hooks/set-state-in-effect` errors plus one image warning.
>
> `PLAN-002`, `FLOW-005`, and `READY-003` remain medium PARTIAL cases. `RESUME-LIVE-001`, `SPEECH-LIVE-001`, and `SPEECH-LIVE-002` are environment/provider BLOCKED cases, not confirmed product failures. The eight NOT TESTED cases still require unavailable real fixtures or environments. The primary text-interview demo path is **Demo Ready: YES**; **Production Ready: NO** pending those partial, blocked, untested, and lint conditions.

Date: 2026-08-23  
Scope: final validation of the current `fipilot-cv_classify` codebase after the completed robustness fixes.

## Executive Summary

```text
Overall Status: FAIL
Tests Designed: 74
Tests Executed: 66
NOT TESTED: 8

PASS: 57
FAIL: 3
PARTIAL: 3
BLOCKED: 3

Confirmed Critical Bugs: 0
Confirmed High Bugs: 0

Demo Ready: CONDITIONAL
Production Ready: NO
```

Baseline comparison:

| Result | Original | Final | Change |
| --- | ---: | ---: | ---: |
| PASS | 43 | 57 | +14 |
| FAIL | 17 | 3 | -14 |
| PARTIAL | 3 | 3 | 0 |
| BLOCKED | 3 | 3 | 0 |
| Confirmed Critical bugs | 3 | 0 | -3 |
| Confirmed High bugs | 8 | 0 | -8 |

The original inventory contains 66 executable cases and 8 cases without the required fixture or environment. The backend runner also executes the newer `EVAL-REG-01` regression; it passed but is excluded from the 74-case aggregate to keep the comparison like-for-like.

## Final Execution

| Suite | Inventory cases | PASS | FAIL | PARTIAL | BLOCKED |
| --- | ---: | ---: | ---: | ---: | ---: |
| Backend deterministic robustness | 37 | 33 | 2 | 2 | 0 |
| Frontend robustness | 11 | 9 | 1 | 1 | 0 |
| Live Azure AI | 16 | 15 | 0 | 0 | 1 |
| Live Azure Speech | 2 | 0 | 0 | 0 | 2 |
| **Total executed** | **66** | **57** | **3** | **3** | **3** |

## Completed Fix Verification

| Area | Evidence | Final status |
| --- | --- | --- |
| Session and candidate isolation | `STATE-01` through `STATE-04` | PASS |
| Native 0–10 scoring and guardrail | SCORE10 backend regressions, `REPORT-002`, `EVAL-LIVE-006` | PASS |
| Planner grounding | `PLAN-001` | PASS |
| Unsupported-premise handling | `EVAL-REG-01`, `EVAL-LIVE-007` | PASS |
| Resume context bounding | `BOUNDARY-001` | PASS |
| Empty experience handling | `FLOW-001` | PASS |
| QGen deduplication | `QGEN-002`, `QGEN-LIVE-003` | PASS |
| Frontend request coalescing | `UX-001` | PASS |
| Report consistency | `REPORT-003`, `REPORT-LIVE-001` | PASS |
| Semantic RAG and content deduplication | `RAG-002`, `RAG-003` | PASS |

`QGEN-LIVE-003` is classified on final system behavior: raw Azure output may repeat or closely paraphrase a question, but the current history-aware backend does not accept a duplicate into the final interview. Raw model duplication alone is not counted as a product failure.

P0 regressions: none.  
P1 regressions: none.  
Score 0–10 regressions: none.

## Remaining Non-PASS Cases

| Test | Status | Severity | Current result |
| --- | --- | --- | --- |
| RESUME-007 | FAIL | MEDIUM | Corrupt PDF still returns an uncontrolled 500 extraction response |
| PROFILE-002 | FAIL | LOW | Canonically equivalent Unicode skills are not deduplicated |
| UX-002 | FAIL | MEDIUM | Latest-resume service errors are still exposed as an empty result |
| PLAN-002 | PARTIAL | MEDIUM | Weak project evidence lacks an explicit warning |
| FLOW-005 | PARTIAL | MEDIUM | Provider timeout handling remains a generic 502 response |
| READY-003 | PARTIAL | MEDIUM | Education-only readiness lacks a shared authoritative policy |
| RESUME-LIVE-001 | BLOCKED | CRITICAL | Azure content policy blocks the prompt-injection resume fixture; no product failure confirmed |
| SPEECH-LIVE-001 | BLOCKED | MEDIUM | TTS executable/provider prerequisite is unavailable |
| SPEECH-LIVE-002 | BLOCKED | MEDIUM | STT cannot execute because the TTS prerequisite is blocked |

No executable case currently confirms a Critical or High product defect.

## NOT TESTED Cases

| Test | Reason |
| --- | --- |
| RESUME-NT-001 | Password-protected PDF fixture unavailable |
| RESUME-NT-002 | Mixed image/table/icon PDF fixtures unavailable |
| RAG-NT-001 | Live pgvector database unavailable |
| FLOW-NT-001 | Test database required for concurrent persistence |
| UX-NT-001 | No checked-in Playwright back/refresh seam |
| UX-NT-002 | No checked-in physical-browser rapid-click seam |
| STATE-NT-001 | No checked-in two-real-tabs seam |
| SPEECH-NT-001 | Real microphone/noisy human audio unavailable |

## Regression and Build Validation

| Check | Result |
| --- | --- |
| Backend regression | PASS — 65 tests and 10 subtests |
| Frontend tests | PASS — 25/25 tests |
| Frontend robustness runner | PASS — 15/15 executable assertions; inventory classification 9 PASS, 1 FAIL, 1 PARTIAL |
| TypeScript typecheck | PASS |
| Production build | PASS |
| Python compile | PASS |
| Lint | FAIL — 3 pre-existing `react-hooks/set-state-in-effect` errors and 1 pre-existing image warning; not a new regression |

## Readiness

Demo Ready: **CONDITIONAL** — the fixed P0/P1, scoring, QGen, report, boundary, and RAG paths pass. Text interview demos are viable, but the speech environment is blocked and three medium/low robustness failures remain.

Production Ready: **NO** — 3 executable cases fail, 3 are partial, 3 are blocked, and 8 remain untested.

Top remaining risks:

1. Corrupt resume input can still surface an uncontrolled server error (`RESUME-007`).
2. Resume service outages can be mistaken for an empty resume state (`UX-002`).
3. Speech provider prerequisites and several real-environment concurrency/browser seams remain blocked or untested.

## Commands and Evidence

- Backend robustness: `backend/.venv/Scripts/python.exe evaluation/agent_robustness/run_backend_evaluation.py`
- Frontend robustness: `npm test -- evaluation/agent_robustness/frontend_robustness.test.ts`
- Live AI: `backend/.venv/Scripts/python.exe evaluation/agent_robustness/run_live_ai_evaluation.py`
- Live Speech: `backend/.venv/Scripts/python.exe evaluation/agent_robustness/run_live_speech_evaluation.py`
- Backend regression: `uv run --with pytest pytest -q`
- Frontend regression: `npm test`
- Typecheck: `npm run typecheck`
- Build: `npm run build`
- Compile: `python -m compileall -q fipilot api`
- Lint: `npm run lint`

Evidence files:

- `evaluation/agent_robustness/backend_results.json`
- `evaluation/agent_robustness/frontend_results.json`
- `evaluation/agent_robustness/live_ai_results.json`
- `evaluation/agent_robustness/live_speech_results.json`
