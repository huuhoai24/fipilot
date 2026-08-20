# M8 council brief

## M8.2 update

The exact live blocker is now known: `GOOGLE_CLOUD_PROJECT` is absent. The old
adapter mislabeled this pre-request configuration failure as invalid JSON. The
single authorized M8.2 Text/Voice retry reached no provider endpoint, cost
exactly `$0.00`, and stopped without Phase C. Phase A remains 10/10, but M8 is
not closed and evaluator trust remains LOW.

## Does the whole system work?

The duplicate replay defect is fixed. The offline production workflow completed
6/6 reconstructed interviews and the Phase A reliability gate passed 10/10.
The one-Text/one-Voice Phase B smoke was attempted, but both scenarios failed
JSON response validation before technical completion. Phase C was not opened.

## How is data preserved?

Forty-two canonical trace records carry scenario/candidate/session identity,
stage timestamps, input/output hashes, model/config snapshots, latency, and
status without raw prompts, answers, or secrets. All six offline scenarios
preserved profile, plan/retrieval, questions, answers, evaluations, state, and
report identity. Exact replay now produces zero additional writes.

## What is total latency?

Only offline integration latency is available: summed traced time averaged
39.136 ms per scenario (median 38.488, max 53.921). This excludes provider,
network, real STT, and user time and must not be presented as live latency.

## What does one interview cost?

The zero-call dry run estimated $0.121620 for Phase B. Exact live spend is
**UNKNOWN**: both calls ended in provider response-validation errors, and the
current cache wrapper records usage only after a valid response. Its reported
$0 must not be treated as invoice evidence.

## Is the final AI score accurate?

The score is not claimed as expert-human accuracy. M7 automated-reference
evaluation found remaining Answer Evaluator limitations, so production score
trust is currently **LOW**. No expert human ground truth was used in M8.

## Then why demo it?

Do not claim full E2E readiness yet. Duplicate-submit safety now passes, but the
two live Phase B scenarios did not complete. Any later demo must still disclose
LOW score trust.
