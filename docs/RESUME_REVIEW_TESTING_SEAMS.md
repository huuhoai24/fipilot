# Resume Review Confirmed Testing Seams

Status: specification for implementation; production behavior is not implemented yet.

The feature should be tested at stable behavioral boundaries instead of only through the large setup page. The HTTP routes in section 3 are public contracts. The validators, services, repositories, frontend state models, and components in the other sections are required internal module contracts to introduce during implementation; they are not claimed to be existing public interfaces.

## 1. Backend pure-domain seams

### Profile update validator

One pure validator should accept the canonical editable projection and return normalized data or structured field issues.

Required cases:

- Accept each canonical editable key.
- Reject aliases, unknown keys, and every read-only key.
- Reject nested read-only source or provenance fields in the correction payload.
- Accept `evidence_id` only as an immutable correlation key for an existing Skill Evidence entry.
- Reject unknown, duplicate, changed, or client-selected new evidence IDs.
- Return the documented `unknown_field`, `read_only_field`, evidence-ID, education-shape, and empty-skill issue codes with exact paths.
- Return `empty_update` when PATCH has no editable canonical field.
- Accept valid incomplete profiles.
- Reject negative `years_experience`.
- Trim skills, reject empty skills, and deduplicate case-insensitively.
- Require each skill-evidence reference to match a normalized skill.
- Reject completely empty project, experience, education, and evidence entries.
- Preserve meaningful zero and null values.
- Validate all nested shapes and return exact field paths.
- Return `invalid_years_experience`, `empty_nested_entry`, and `evidence_skill_not_found` as Profile Validity issues.
- Preserve legacy string education when `education` is omitted.
- Reject a string `education` correction and accept only structured entries or `null`.
- Run every normalization vector in `docs/RESUME_REVIEW_UI_SPEC.md` against the backend normalizer.
- Run the same compatible normalization vectors against the frontend helper and compare results.

### Interview Readiness validator

One pure validator is shared by profile responses and both interview modes.

Required cases:

- Report every applicable issue, not only the first.
- Reject blank and fallback `Candidate` names.
- Reject missing skills.
- Accept skill evidence only when at least one evidence string is nonblank after normalization.
- Accept a meaningful project.
- Accept a meaningful experience.
- Accept education with `institution` and `degree`.
- Accept education with `institution` and `field_of_study`.
- Reject education missing its institution.
- Support students and interns without experience or projects.
- Produce identical readiness results for text and speech start.
- Treat a persisted Profile Validity failure as not interview-ready without reclassifying the originating issue as a missing minimum-evidence requirement.

### Document acceptance classifier

Keep document acceptance separate from LLM extraction.

Required cases:

- Genuine PDF and DOCX content.
- Renamed or misleading extensions.
- Zero bytes.
- Exactly 10 × 1024 × 1024 bytes is accepted when otherwise valid; one byte more is rejected.
- More than 10 MB.
- Encrypted or password-protected document.
- Malformed container.
- Valid image-only PDF.
- A valid PDF or DOCX container with no readable text returns `no_extractable_text`.
- Fewer than 50 meaningful normalized characters.
- Meaningless whitespace does not count toward the threshold.
- Page count alone never causes rejection.
- OCR is never invoked.
- Rejections do not call profile extraction or mutate Candidate Profile or Resume persistence; an idempotency rejection record may still be stored.
- Incomplete processing produces `partial_extraction`, not a rejection.

## 2. Backend service and persistence seams

### Profile correction service

Test the application service with a fake repository:

- It receives authenticated user identity from the route boundary and resolves ownership server-side.
- A foreign or missing candidate is indistinguishable through a `404`.
- It merges only allowlisted fields.
- It preserves candidate identity, ownership, confidence, extraction, provenance, and audit data.
- It records user-corrected evidence without changing source metadata.
- It assigns UUID v4 evidence IDs to new entries and preserves existing IDs through edits and reorder.
- It backfills and persists IDs before returning existing evidence to the structured editor.
- It initializes an unversioned existing profile at version 1; a backfill mutation on an already versioned profile increments once.
- It retains removed evidence provenance in audit history.
- It preserves legacy education on unrelated PATCH and retains the original string in audit metadata after explicit replacement.
- It recomputes `seniority_signal` after relevant changes.
- It returns the persisted profile, not the request object.
- It requires the last-read version, atomically compares it, and increments `profile_version` exactly once on success.
- It returns `profile_version_required` when the precondition is missing and `stale_profile_version` without mutation when stale.
- It rejects weak, wildcard, unquoted, or multi-value `If-Match` with `invalid_profile_version_precondition`.
- Stale conflict returns the current version/ETag but never replaces or echoes the local draft.
- A normalization-equivalent successful review save increments the version and can acknowledge Partial Extraction.
- Failed and stale saves do not acknowledge Partial Extraction.
- The first successful review save records acknowledgement time/version, removes the prominent warning, and preserves the original warning metadata.
- It appends the exact audit version, UTC timestamp, source, changed fields, and evidence changes without accepting ownership mutation.
- It derives mutation source server-side and rejects client-supplied audit source.

### Upload idempotency store

Run the same contract suite against each persistence implementation:

- First request creates `processing` before extraction begins.
- Same user, key, and fingerprint while processing returns `upload_in_progress`.
- Same user, key, and fingerprint after completion returns the original response.
- Same key with another fingerprint returns `idempotency_key_reused`.
- Same key and content with another operation or replacement target returns `idempotency_key_reused`.
- Same replacement key with another expected Profile Version returns `idempotency_key_reused`.
- Deterministic rejection is replayed without extraction.
- Deterministic rejection replay preserves the original status/body, and completion replay preserves the original success body.
- `retryable_failure` can restart or continue without duplicate persistence.
- Keys are isolated by authenticated user and operation.
- A unique constraint or transactional create prevents concurrent duplicate profiles.
- Completed and deterministic rejected records expire 24 hours after finalization.
- Retryable failures expire 24 hours after their last update.
- A processing lease becomes recoverable after 30 minutes without an update.
- A new lease increments a fencing generation and prevents a stale worker from committing.
- Status lookup is owner-scoped and returns the terminal original result or error.
- Status responses always contain `upload`, `result`, and `error`, with nulls matching the documented state.

### Atomic Replacement Upload service

Test the application-service contract against each repository implementation:

- Each rejection preserves the previous Candidate Profile byte-for-byte.
- Timeout or raised exception before commit preserves the previous profile.
- Successful extraction atomically replaces the profile and Resume data.
- Successful Partial Extraction atomically replaces the profile and records its warning.
- No reader observes a half-replaced Candidate Profile.
- A pending replacement does not change the readiness response for the saved profile.
- Replacement requires an owned `candidate_id` route target and the matching `If-Match`.
- A correction committed during replacement extraction causes stale replacement commit to fail without mutation.
- Successful replacement increments `profile_version` once.
- Retrying the same file against a newly loaded Profile Version uses a new idempotency key.

### Interview Session snapshot

Required integration cases:

- Start reloads the owned persisted profile rather than accepting client profile data.
- Non-ready start is rejected before orchestration or session creation.
- Text and speech use the same readiness validator.
- A successful start stores the exact persisted profile version used for the session.
- The session stores `candidate_profile_version` beside the immutable profile snapshot.
- Interview start success exposes the selected version in both session state and the snapshot profile.
- Later profile updates do not change session state.
- Later profile updates do not change an existing report.
- A concurrent profile save and interview start have a deterministic transactional outcome.
- Starting while a Replacement Upload is pending snapshots the existing persisted profile.
- Starting after an atomic replacement succeeds snapshots the replacement profile.

## 3. API contract seams

Use FastAPI `TestClient` tests adjacent to:

- `backend/app/tests/test_resume_upload_v2.py`
- `backend/app/tests/test_interview_api.py`
- `backend/app/tests/test_auth_and_ownership.py`
- Repository suites for SQLite and Firestore

Required route coverage:

| Route | Contract assertions |
| --- | --- |
| Initial Resume upload | Auth, exactly one multipart file, no candidate body field, header requirement, file classification, structured codes, ETag, warning response, idempotency replay |
| Replacement Upload | Owned candidate path, `If-Match`, idempotency scope, atomic replacement, stale commit protection |
| Upload status | Ownership, processing recovery fields, terminal result/error, expiry |
| Profile GET | Auth, ownership, ETag, canonical response, version, evidence identity/provenance, readiness, warning and audit metadata |
| Profile PATCH | Auth, ownership, `If-Match`, strict extra-field rejection, immutable evidence correlation, normalization, partial-valid save, version increment, conflict response |
| Interview start | Auth, ownership, authoritative readiness, all applicable issue codes, immutable snapshot and selected Profile Version, correct mode |

Validate structured bodies, not only HTTP status codes. Contract tests should assert that aliases and read-only fields fail rather than disappear.

Assert every mapping in the specification's HTTP status table, including:

- `200` success responses and Partial Extraction warning success
- `202 upload_in_progress` with `Location` and `Retry-After`
- `400 multiple_files_not_allowed`
- `400 idempotency_key_required` and `invalid_profile_version_precondition`
- `422 request_validation_failed` when the multipart file is missing
- `409 idempotency_key_reused`
- `412 stale_profile_version`
- `413`, `415`, and document-specific `422` rejections
- `422 profile_validation_failed`
- `422 profile_not_interview_ready`
- `428 profile_version_required`
- `503 transient_service_failure`

## 4. Frontend state seams

### Upload state reducer

Extract upload transitions from `TextInterviewPage.tsx` into a pure state model.

Required transitions:

- `idle → file_selected → uploading → extracting → completed`
- `extracting → completed_with_warning`
- Local or server validation → `validation_rejected`
- Network or server failure → `transient_failure`
- Unrecoverable auth failure → `authentication_required`
- Explicit retry reuses the idempotency key.
- Selecting another file generates a new key.
- Partial Extraction transitions into Profile Review, never into `Try again`.
- Failed replacement retains the existing saved profile and readiness.
- Deterministic Upload Rejections expose actionable copy and `Choose another file`, not a generic `Try again`.
- `upload_in_progress` follows the owned status URL after `Retry-After` without retransmitting the file.
- `retryable_failure` offers explicit retry with the same key only while the selected file remains in memory.

### Profile form model

Maintain separate `serverProfile` and editable `draftProfile` values.

Required cases:

- Dirty state is derived from canonical editable fields only.
- Read-only response changes do not become editable payload keys.
- The model retains the last-read ETag/Profile Version separately from the editable payload.
- Successful save replaces both server and draft state with the returned profile.
- Failed save preserves the draft and last server profile separately.
- Reload restores only persisted server data.
- Start actions disable for dirty data, unsuccessful latest save, or backend-not-ready state.
- A ready profile from a successful accepted upload may start before any correction save; after a correction save is attempted, only its latest successful response can re-enable start.
- A stale save preserves the local draft, exposes Reload latest as primary recovery, and never automatically resubmits or merges.
- Reload latest updates the server baseline while retaining the local draft for comparison.
- Legacy education remains readable until explicit structured replacement succeeds.
- Existing evidence IDs are echoed unchanged; new evidence entries omit IDs.
- Readiness issue links resolve to stable field IDs.
- First invalid field receives focus after failed save.

### API adapter

Test `frontend/src/lib/api.ts` with mocked fetch/auth boundaries:

- Upload sends `Idempotency-Key`.
- Replacement Upload sends both the owned candidate route and `If-Match`.
- Profile PATCH sends `If-Match` and no JSON `profile_version`.
- The one authentication refresh resends the same body and key.
- No retry occurs after non-auth failures.
- Structured codes and issue paths survive error parsing.
- Profile save sends canonical editable top-level keys only.
- Existing evidence IDs are the only immutable nested correlation values sent.
- The adapter parses Profile, Upload Success, Upload Processing, Upload Status, common error, warning, and readiness structures without falling back to `detail` strings.
- Upload transient failures preserve structured recovery `upload_id` and `status_url`.
- Start sends `candidate_id` and the existing interview configuration, never local profile data.

## 5. Frontend component and route seams

Use React Testing Library around the feature components and protected routes.

Required user-visible cases:

- Accepted upload automatically opens or navigates to Profile Review.
- Partial Extraction displays `Resume partially extracted`.
- Readiness summary lists and focuses every missing requirement.
- Labels, descriptions, errors, and `aria-invalid` relationships are correct.
- Add, remove, and reorder controls work by keyboard.
- Existing Skill Evidence retains stable identity and read-only provenance while reordered or corrected.
- Legacy education is readable and can be explicitly replaced without inferred fields.
- `Save corrections` is primary while dirty.
- A valid partial profile can be saved.
- A clean incomplete profile exposes `Complete missing details`.
- Both start buttons are visible and disabled with reasons when not ready.
- Successful save can enable both starts based on server readiness.
- Stale save shows the approved conflict copy and actions while preserving edits.
- Start failure does not navigate.
- Successful text start navigates to `/text-interview/:sessionId`.
- Successful speech start navigates to `/speech-interview/:sessionId`.
- Unsaved navigation warns and does not describe the draft as saved.
- A pending replacement explains that start uses the currently saved profile.

## 6. Responsive and accessibility seams

At 1440px, 1024px, 768px, and 390px verify:

- No horizontal overflow.
- Section and keyboard order remain the approved order.
- Actions and validation copy remain visible.
- Touch targets remain at least 44px.
- Sticky content does not cover focused controls.
- Readiness links focus visible controls.
- Color is not the only status indicator.
- Text and controls meet the contrast requirements in both themes.
- Reduced motion removes nonessential transitions.

Automated accessibility checks are necessary but not sufficient. Complete a keyboard-only pass and screen-reader smoke test for upload, nested editing, failed save, and interview start.

## 7. Regression boundary

Existing interview, report, history, authentication, SQLite, and Firestore tests remain in scope. Fixtures that currently use only a name and skill must add qualifying evidence when testing a successful interview start; they should not weaken the new readiness rule.
