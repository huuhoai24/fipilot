# Resume Review Implementation Risks

Status: contract closure complete. The specification blockers identified during review are resolved by ADRs 0007 through 0011 and `docs/RESUME_REVIEW_UI_SPEC.md`. The remaining items are implementation and release risks; they do not require additional product-preference decisions.

## Closed contract blockers

| Former blocker | Final contract |
| --- | --- |
| Replacement target identity | Users may own multiple Candidate Profiles. Replacement uses the ownership-checked route `POST /api/v2/candidates/{candidate_id}/resume`. |
| Legacy education | A string remains readable and unchanged until explicit structured replacement; the original is retained in audit metadata. |
| Skill Evidence identity | Existing entries use immutable server-issued UUID v4 `evidence_id` values; source metadata remains bound to the ID. |
| Concurrent saves | Strong `If-Match` optimistic concurrency with monotonically increasing `profile_version`; stale writes return `412 stale_profile_version`. |
| Public responses | Profile, upload, status, warning, issue, error, processing, and HTTP status structures are normative in the UI specification. |
| Normalization | Shared backend-authoritative NFKC, Unicode whitespace, case-folded skill comparison, and concrete test vectors are normative. |
| Idempotency lifecycle | Terminal records last 24 hours; inactive processing leases become recoverable after 30 minutes with fencing. |
| Upload recovery | `202 upload_in_progress` supplies an owned status URL and `Retry-After`; status polling does not retransmit the file. |
| Multipart cardinality | More than one file returns `400 multiple_files_not_allowed`. |
| Audit metadata | Version, UTC time, mutation source, changed fields, and evidence changes are immutable and ownership-free. |
| Partial Extraction acknowledgement | Original warning and first successful review-save acknowledgement are persisted separately. |
| Interview snapshot selection | Start atomically reads the latest committed Profile Version and creates the session with that version and snapshot. |

## 1. Persistence migrations across SQLite and Firestore

Classification: **Release blocker**

Current SQLite rows store profile JSON and Resume text on `users`, while Firestore stores profile data in candidate documents. Neither implementation has Profile Version columns, evidence provenance, audit events, Partial Extraction acknowledgement, or upload-operation records.

Resolution criterion: introduce equivalent repository contracts and safe migrations for both stores. Migration must initialize existing Candidate Profiles, assign stable evidence IDs once, preserve legacy education, and never rewrite prior Interview Session snapshots or reports.

## 2. Existing Skill Evidence backfill

Classification: **Release blocker**

The structured editor cannot safely open existing evidence until each entry has a persisted UUID and provenance. Recomputing IDs on each read would break correlation.

Resolution criterion: perform an idempotent `system_backfill` that initializes `profile_version` where absent, assigns and persists each missing `evidence_id`, binds current source metadata, and produces stable results across repeated reads.

## 3. Conditional mutation atomicity

Classification: **Release blocker**

SQLite and Firestore use different transaction primitives. PATCH and Replacement Upload must compare `If-Match`, persist normalized data and audit metadata, increment the version once, and return the committed state atomically.

Resolution criterion: repository contract tests prove that two writers using the same version cannot both commit and that failed or stale mutations change no profile, Resume, warning, or audit data.

## 4. Interview-start transactional boundary

Classification: **Release blocker**

The current start route loads a profile, awaits orchestration, creates a session, and then saves state. This does not yet atomically select and persist the snapshot Profile Version.

Resolution criterion: atomically read the latest committed owned profile and create the session with its snapshot and `candidate_profile_version` before orchestration uses that stored snapshot. A later profile commit must not alter it.

## 5. Upload-operation storage and fencing

Classification: **Release blocker**

Neither repository currently has an upload-operation record, unique idempotency claim, processing lease, heartbeat, expiry, or fencing generation.

Resolution criterion: both repositories atomically claim user, operation, target, key, and fingerprint; enforce 24-hour replay; transition inactive 30-minute leases; and reject completion from a superseded worker.

## 6. Complete-document processing

Classification: **Release blocker**

`backend/services/profile_scanner/prompts.py` currently passes only the first 12,000 characters to extraction.

Resolution criterion: process the complete Resume or persist and return `partial_extraction` whenever any content is omitted. The original warning must survive later acknowledgement.

## 7. Actual document detection

Classification: **Release blocker**

The current upload route trusts the filename extension and collapses document failures into generic responses.

Resolution criterion: detect the actual PDF or DOCX format, distinguish every approved document rejection, enforce multipart cardinality, and complete deterministic validation before profile mutation.

## 8. Observable upload and extraction phases

Classification: **Release blocker**

The current `fetch` adapter cannot expose reliable upload progress, and the synchronous endpoint does not expose an extraction phase.

Resolution criterion: use an honest upload-progress mechanism and the upload-operation status resource, or avoid asserting a phase when it is unknown. Never invent percentage progress.

## 9. Strict schemas and response adapters

Classification: **Release blocker**

The current `CandidateProfile` model mixes editable and read-only fields and ignores unknown fields by default. The frontend `ApiError` expects a string-like `detail` rather than the new structured contract.

Resolution criterion: introduce strict correction/request schemas, versioned response types, common error parsing, warning and issue types, immutable evidence correlation, and the exact HTTP mappings without adding field aliases.

## 10. Existing readiness fixtures

Classification: **Release blocker**

Several interview tests use only a name and skills, which is intentionally insufficient under the approved readiness rule.

Resolution criterion: add qualifying evidence to successful-start fixtures and add explicit readiness, legacy invalid-data, snapshot-version, and text/voice parity cases.

## 11. Setup page responsibility

Classification: **Implementation note**

`TextInterviewPage.tsx` currently owns upload, profile preview, interview configuration, text-session execution, and mode branching.

Resolution criterion: extract the specified feature components and pure state contracts while continuing to use the existing UI primitives and API adapter.

## 12. Unsaved state across authentication

Classification: **Implementation note**

Browsers do not guarantee that an in-memory File or local profile draft survives reload, redirect, or process termination.

Resolution criterion: preserve upload files and drafts only for the current page lifetime unless a separately reviewed secure draft-persistence design is approved. Copy must never imply that local edits were saved.

## 13. Operational audit retention

Classification: **Implementation note**

Audit event shape is closed, but long-term retention, administrative access, and deletion policy are outside this Resume Review feature.

Resolution criterion: retain the metadata required by current profile provenance and existing-session immutability; define broader compliance retention separately without exposing ownership mutation through Candidate Profile PATCH.
