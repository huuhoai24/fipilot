# Architecture Gaps and Unknowns

This matrix separates executable behavior from target contracts and unverified operations. It is descriptive, not a remediation plan.

| Area | Classification | Current evidence | Required or expected boundary | Consequence |
|---|---|---|---|---|
| PDF OCR | PARTIAL / documentation conflict | Runtime invokes RapidOCR for sparse/image-only pages | ADR 0004 and older testing seam describe no OCR | Tests and operator expectations can disagree with executable behavior |
| Initial upload idempotency | SPEC-PENDING | `POST /api/v2/resume/upload` has no `Idempotency-Key` contract | Durable 24-hour replay, request binding, conflict detection | Duplicate requests can repeat work or create resources |
| Upload lifecycle | SPEC-PENDING | Synchronous request; no status resource, lease, generation, or fencing | `processing/completed/rejected/retryable_failure` state machine | No safe recovery from concurrent or abandoned workers |
| Multipart cardinality | PARTIAL / MISSING TEST | Route declares one `UploadFile` | Explicit `multiple_files_not_allowed` structured response | Framework parsing behavior may define the outcome |
| Replacement Upload | SPEC-PENDING | No replacement endpoint | Atomic replacement with `If-Match` and idempotency | Existing profile cannot be safely replaced under target contract |
| Profile Correction | SPEC-PENDING | No canonical PATCH mutation path | Strict allowlist, strong `If-Match`, one version increment and audit | UI cannot commit reviewed corrections under the documented contract |
| Evidence correlation/provenance | PARTIAL | Provenance is computed in memory; `evidence_id` is absent | Server-controlled IDs and persisted source metadata | Existing evidence cannot be safely correlated across edits |
| Readiness enforcement | PARTIAL | GET computes authoritative issues | Text and speech start must call the same validator | Non-ready profiles can currently start an interview |
| Session snapshot | PARTIAL | Session copies profile content | Atomic immutable snapshot plus exact `candidate_profile_version` | Start can race profile changes and lacks version traceability |
| Historical report input | RISK | Report service reloads latest Candidate Profile | Report must use the session snapshot only | Later profile changes can affect a historical report |
| Report first-write concurrency | RISK | Check, generate, then save; sequential reuse exists | Durable single-writer claim or equivalent | Concurrent clients can duplicate model work |
| Plan/completion invariant | RISK / MISSING TEST | Completion also occurs when plan rounds are exhausted | Configured question count and plan length need a guaranteed invariant | Session can complete earlier than configured count |
| Production hybrid RAG | SPEC-PENDING | No runtime hybrid retriever | Only add if explicitly adopted; M6 hybrid is offline evidence | Do not describe offline hybrid results as deployed behavior |
| Per-question retrieval | PARTIAL | Retrieval feeds Planner; Question Generator receives a selected round | No direct raw-chunk retrieval at each question | Fine-grained source attribution is unavailable |
| RAG traceability | PARTIAL | Vector results include topic/path/similarity strings | No persisted chunk IDs on plan/question/report | Runtime outputs cannot be traced to exact knowledge records |
| Vector operations | UNKNOWN | Code and provisioning documentation exist | Live index, dimensions, population, permissions, and selected mode | Repository audit cannot assert vector mode is healthy in production |
| Vector fallback | PARTIAL | Provider/search errors propagate | Explicit fallback policy if operational requirements demand it | Vector configuration failures abort preparation |
| Model resilience | PARTIAL | Same-provider exponential retry with jitter | No alternate provider/model fallback or circuit breaker | Regional/provider outage stops AI stages |
| Error envelope | PARTIAL | Some routes return structured domain errors; others use generic FastAPI detail | Stable transport-wide envelope if required by clients | Frontend recovery logic is inconsistent |
| Observability | PARTIAL | Request IDs, JSON logs, redaction and stage timings | No metrics endpoint, distributed tracing, alert rules, or durable trace backend | Cross-service diagnosis depends on log correlation |
| Database migrations | RISK | Schema setup is adapter-owned; no migration framework is evident | Versioned migration process for persistent production upgrades | Schema evolution and rollback are operationally fragile |
| Checked-in CI | SPEC-PENDING | No `.github/workflows` | Automated compile, test, lint and build gates | Validation depends on local/manual execution |
| Responsive/keyboard acceptance | MISSING TEST | Component tests exist; no checked-in Playwright seam found | Required viewport and keyboard smoke coverage | Repository cannot demonstrate all documented UX acceptance points |
| Live backend/frontend revision | UNKNOWN | Docker/deploy scripts and dated deployment report exist | Current control-plane/runtime evidence | Configuration and deployment diagrams remain source-level only |
| Remote speech availability | UNKNOWN | Speech service source and local compose/scripts exist | Current deployed endpoint and health evidence | Voice operational readiness cannot be asserted |
| Speech durability | PARTIAL | Audio and coordination queues are bounded process memory | Durable recovery only if product requirements demand it | Instance loss terminates the active voice session |
| `vector_prototype` | UNUSED IN PRODUCTION | Throwaway frontend prototype is outside production source imports | Keep as design evidence only | Must not be represented as a deployed route |
| `shared/schemas/graph_state.py` | UNUSED / COMPATIBILITY | Compatibility schema exists outside the active orchestrator contract | Remove only after dependency proof | Not evidence of a graph-orchestration runtime |
| `backend/app/**` | COMPATIBILITY, NOT A SECOND RUNTIME | Active modules/tests re-export or exercise gateway/shared paths | Continue routing new behavior through active seams | Editing it as a parallel implementation would create divergence |
| Offline M1-M8/E3 artifacts | IMPLEMENTED OFFLINE / WORKTREE | Evaluation scripts and reports exist as untracked worktree evidence | Commit/review separately before treating as repository baseline | Results are useful evidence but not production functionality |

## Highest-impact architecture mismatches

1. The documented Profile Version, conditional mutation, Replacement Upload, upload idempotency, and audit contracts are not implemented in the active gateway.
2. Interview start neither enforces the shared readiness result nor atomically records the exact Profile Version with an immutable snapshot.
3. Report generation reloads the latest profile, which conflicts with historical session immutability.
4. Production RAG is Planner-only and single-mode: lexical by default or vector when configured. Hybrid and direct per-question RAG exist only in offline evaluation evidence.
5. Source proves deployability, not current live health. Deployment, vector index freshness, and remote speech availability therefore remain UNKNOWN.

