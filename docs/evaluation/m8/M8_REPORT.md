## M8.2 STATUS

**PARTIAL — PROVIDER PREFLIGHT BLOCKED**

M8.2 identified the exact Phase B failure as missing Vertex project
configuration, not a model JSON mismatch. The previous adapter wrapped
`LLMConfigurationError` as `LLMResponseValidationError`. Phase A still passes
10/10. The one authorized Text/Voice retry stopped before any outbound provider
request, and Phase C was not opened. Full analysis and corrected telemetry are
in `M82_ROOT_CAUSE_ANALYSIS.md` and
`evaluation/m8/evidence/phase-b-m82/POST_RUN_DIAGNOSIS.json`.

## M8.1 STATUS

**PARTIAL**

The duplicate-answer production defect is fixed and the zero-cost Phase A gate
now passes 10/10. Phase B was opened exactly once for its one Text and one Voice
scenario. Both stopped before technical completion with
`LLMResponseValidationError`; Phase C was not opened.

## ROOT CAUSE

Text submitted only `{answer}` and Voice submitted the final transcript without
an immutable turn identity. Both paths reloaded whatever turn was current at
request time, called the evaluator, then wrote the new state. A delayed replay
therefore attached the old answer to the next turn. The repositories had no
unique `(session_id, turn_id)` answer-submission record, so application-level
in-flight locks could not protect reconnects, multiple processes, or concurrent
requests.

## INVARIANT DESIGN

The minimal contract is now:

- submission identity is the server-issued `session_id + turn_id`;
- the normalized answer is compared by SHA-256 hash;
- persistence claims the turn before opening handling or evaluator invocation;
- an exact completed replay returns the latest persisted state with
  `answer_replayed=true` and performs no state/evaluator write;
- a different answer for the same turn returns `answer_already_submitted`;
- an active duplicate returns `answer_submission_in_progress`;
- stale and unknown/future turn IDs are rejected before a claim is created;
- evaluator failure abandons the processing claim, leaving state unchanged so
  an explicit retry can safely claim the turn again.

SQLite has a database unique constraint on `(session_id, turn_id)`. Firestore
uses an atomic create of a deterministic per-turn submission document and a
batch that completes the claim with the session-state transition.

## TEXT

The Text API requires `turn_id`. The React client captures the visible current
turn before awaiting the request and sends it with the answer. Text opening and
technical answers use the shared submission service. Structured conflicts are
returned without invoking the evaluator.

## VOICE

Voice uses the same submission service. The websocket binds the current
server-owned `turn_id` when listening or barge-in begins, so a delayed final STT
callback cannot drift to a later turn. Manual `confirm_answer` controls require
`turn_id`.

## CONCURRENCY SAFETY

A deterministic concurrent test holds the first evaluator call after the
persistent claim and starts a second identical submission. The second request
receives `answer_submission_in_progress`; evaluator calls remain one. After the
first transition completes, an exact replay returns the same state. Counts for
submission claims, Message rows, and Evaluation rows do not increase on replay.

## TEST RESULTS

Focused fix and regression run:

- M8 + answer/API/Voice/Firestore/ownership: 77 passed;
- dedicated answer idempotency: 3 passed;
- Voice websocket + Firestore rerun: 34 passed;
- focused Text frontend: 23 passed.

Final regression:

- full backend: 281 passed, one Starlette deprecation warning;
- M1-M8 evaluation suites: 154 passed, seven dependency deprecation warnings;
- Python compileall: passed;
- frontend TypeScript and lint: passed;
- full frontend: 119 passed;
- frontend production build: passed.

No user-visible layout was changed, so responsive screenshots and Playwright
visual checks were not applicable. No M8 Playwright seam exists.

## PHASE A RERUN

Canonical evidence: `evaluation/m8/evidence/phase-a/PHASE_A_RESULT.json`.

- paid calls: 0;
- reliability: 10/10;
- duplicate write count: 0;
- scenario reconstruction: 6/6;
- completion, continuity, question invariants, and report consistency: 100%;
- unsupported structured report claims: 0%.

The production-isolation guard retained the M7 model routes and local lexical
retrieval.

## PHASE B RESULT

Canonical evidence: `evaluation/m8/evidence/phase-b/LIVE_RESULT.json`.

The dry-run estimate for one Text plus one Voice scenario was **$0.121620**,
below the preferred $0.15 Phase B target. The runner attempted exactly those two
scenarios. Both failed with `LLMResponseValidationError` before technical
completion; no result was accepted and Phase C was not run.

The evidence reports zero provider records and `$0` usage. That value is not
trusted as an invoice fact: `CachedJSONProvider` currently increments miss/call
telemetry only after a valid response, while `VertexGeminiService` can make up
to three provider attempts before raising a validation error. Therefore actual
Phase B spend and token usage are **UNKNOWN**, not proven zero. No automatic
retry of Phase B was made.

## EVALUATOR LIMITATION

Production Answer Evaluator trust remains **LOW**. No expert human ground truth
was introduced. M8.1 changes request identity and persistence only; it does not
retune evaluator prompts, models, thresholds, retrieval, STT, or TTS.

## REGRESSION

Production routing remains:

- resume: `gemini-2.5-flash-lite`;
- planner/question/Voice evaluator: `gemini-2.5-flash`;
- Text evaluator/report: `gemini-2.5-pro`;
- Text evaluator task type: `complex`;
- retrieval: local lexical, eight candidate-aligned topics plus domain/level;
- STT: `large-v3`;
- TTS: `v3turbo`.

## REMAINING ISSUES

- Phase B completion and report consistency remain unmeasured because both live
  scenarios failed response validation.
- Failed-response provider attempts are not counted by M8 cache telemetry, so
  exact new live cost is unknown.
- Real STT WER/CER and subjective TTS quality remain not evaluated.
- Evaluator and final-score trust remain LOW from M7.

## NEXT MILESTONE

Do not auto-run Phase C and do not start M9. The next authorized work should
first fix M8 failed-response usage telemetry and diagnose the live JSON-schema
validation failures without repurchasing the two Phase B scenarios unless a new
retry is explicitly approved.
