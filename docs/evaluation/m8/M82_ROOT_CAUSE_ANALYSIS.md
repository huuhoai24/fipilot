# M8.2 Root Cause Analysis

## Status

**PARTIAL — PROVIDER PREFLIGHT BLOCKED.** Phase A passes. The single authorized
Phase B retry attempted exactly one Text and one Voice scenario, then stopped.
Phase C was not run. Neither scenario reached a provider response or the schema
parser because the required Vertex project configuration is absent.

## Exact failing stage

Both Phase B scenarios stop on the first technical stage:

`M8OfflineHarness.run_scenario` → `InterviewOrchestrator.create_plan` →
`InterviewPlannerAgent.create_plan` → `VertexGeminiService.generate_json`

The selected provider/model/schema contract is Vertex AI Gemini,
`gemini-2.5-flash`, operation `interview_planning`, expected Pydantic schema
`InterviewPlan`, temperature `0.1`, and thinking budget `0`.

The exception presented by the old adapter was `LLMResponseValidationError`.
An offline reproduction of the same production code path exposed its direct
cause:

```text
LLMConfigurationError: GOOGLE_CLOUD_PROJECT is required for Vertex AI Gemini
```

`Settings.google_cloud_project` resolves to `None`. The exception is raised by
`VertexGeminiService._create_default_client` before
`client.models.generate_content` can be invoked. Therefore:

- no provider request was sent;
- no provider response or failed JSON payload exists;
- schema parsing did not begin;
- the exact prior expected-versus-received JSON mismatch is **not applicable**
  to this retry and is **unavailable** for the old M8.1 run.

The previous generic validation exception was a classification defect: the
adapter wrapped a provider configuration error as if it were invalid model JSON.

## Production schema contract

The planner system instruction and task both require JSON-only output. The
adapter configures `application/json`, the SDK-native Pydantic
`response_schema`, temperature `0.1`, and thinking budget `0`.

`InterviewPlan` accepts:

- `duration_minutes`: integer, default 30, range 5–180;
- `rounds`: list, default empty; every `InterviewRound` requires non-null string
  `round_id` and `topic`;
- round `difficulty`: `easy | medium | hard`, default `medium`;
- round `objective` and `reasoning`: strings with empty-string defaults;
- `recommended_question_areas` and `target_skills`: string lists;
- round `weight`: number from 0 through 1;
- round `question_budget`: integer at least 1;
- `coverage_goals` and `risk_areas`: string lists;
- `planner_summary`: string with an empty-string default.

There are no field aliases or custom post-validators. None of the typed fields
are nullable. The models use Pydantic's default extra-field behavior (`ignore`),
so unexpected keys are not the cause of this failure.

Expected versus received for M8.2 is therefore: expected `InterviewPlan` JSON;
received **no provider response**. `RAW FAILED RESPONSE = UNAVAILABLE`. No
missing field, enum value, null, wrapper object, markdown, or numeric mismatch
can be attributed to the actual retry without inventing evidence.

## Evidence correction

`evaluation/m8/evidence/phase-b-m82/LIVE_RESULT.json` is the immutable output of
the attempted run. Its first telemetry patch marked `provider_request_sent`
before client construction, so it incorrectly reports two provider/paid
attempts. The code-path reproduction proves both operations failed before that
boundary. The correction is recorded separately in
`evaluation/m8/evidence/phase-b-m82/POST_RUN_DIAGNOSIS.json`:

- scenario operations attempted: 2;
- outbound provider requests: 0;
- successful provider responses: 0;
- schema-invalid provider responses: 0;
- paid calls: 0;
- exact incremental M8.2 cost: `$0.00`;
- Phase C calls: 0.

This correction does not infer cost from missing token telemetry. Cost is zero
because the provider method was never reached, not because usage fields were
empty. The older M8.1 cost remains **UNKNOWN** because its old evidence cannot
prove the same pre-request boundary retrospectively.

## Minimal adapter and telemetry fix

The production structured-output adapter now:

1. passes the Pydantic type through the Google SDK's `response_schema` contract
   and validates `response.parsed` when the SDK provides it;
2. retains strict Pydantic validation and falls back to validating response text
   when parsed output is unavailable;
3. exposes `LLMConfigurationError` instead of converting it to
   `LLMResponseValidationError`;
4. records sanitized per-attempt lifecycle transitions, hashes, schema name,
   model, latency, usage availability, error category, and validation locations;
5. marks `provider_request_sent` only at the provider method boundary;
6. records failed/invalid/timeout attempts without caching invalid output;
7. blocks M8 paid execution in a zero-call preflight when
   `GOOGLE_CLOUD_PROJECT` is missing.

No prompt, model route, evaluator threshold, retrieval path, STT, or TTS design
was changed. No raw prompt, raw response, candidate answer, credential, token,
or secret is written to the attempt ledger.

## Schema safety

Tests exercise the public `generate_json` boundary with `InterviewPlan`:

- valid nested output passes;
- an out-of-range nested value fails;
- a missing required nested field fails;
- a wrong container type fails;
- an unsupported enum fails;
- SDK-parsed output still undergoes Pydantic validation;
- invalid output and timeouts remain explicit failures;
- invalid outputs create no provider cache entry.

These are deterministic boundary fixtures. They are not represented as the raw
output from M8.1 or M8.2.

## Phase A rerun

Canonical evidence remains
`evaluation/m8/evidence/phase-a/PHASE_A_RESULT.json`:

- 6/6 scenario reconstructions completed;
- reliability gate 10/10;
- continuity, question invariants, and report consistency: 100%;
- unsupported report claims: 0%;
- duplicate replay: 0 model calls, 0 answer rows, 0 evaluation rows, and 0
  state transitions;
- paid calls: 0.

## Phase B budget and outcome

The pre-execution plan for exactly one Text and one Voice scenario was:

- 12 base provider calls: 2 planner Flash, 4 question Flash, 2 Text evaluator
  Pro, 2 Voice evaluator Flash, and 2 report Pro;
- token envelope: 7,000 planner Flash, 10,000 question Flash, 12,000 evaluator
  Pro, 6,200 evaluator Flash, and 11,000 report Pro tokens;
- base estimate: `$0.121620`;
- at most two attempts per operation: worst-case `$0.243240`;
- M8.2 incremental hard ceiling: `$0.25`.

The authorized retry failed at local provider preflight for both scenarios.
Actual outbound calls and incremental cost were zero. No second retry is made.

## Validation results

- focused structured-output and M8 telemetry/regression tests: 40 passed;
- focused M8.1 idempotency, Text API, and Voice websocket tests: 33 passed;
- full backend suite: 286 passed with one existing Starlette deprecation warning;
- M1–M8 evaluation suites: 144 passed with seven dependency deprecation
  warnings;
- Python compileall: passed;
- frontend TypeScript, lint, 119 tests, and production build: passed.

No frontend API contract or user-visible layout changed. Responsive screenshot
and Playwright visual checks are not applicable to this backend/evaluation fix.

## Remaining blocker and trust

Phase B completion, live latency, report consistency, and real Voice STT/TTS
quality remain unmeasured. A valid `GOOGLE_CLOUD_PROJECT` setting and applicable
ADC/Vertex permissions are required before any future explicitly authorized
live run.

Production Answer Evaluator trust remains **LOW**. There is no expert human
ground truth. M8 is not closed, Phase C remains unopened, and M9 must not start.
