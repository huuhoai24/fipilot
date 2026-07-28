# Resume Upload and Candidate Profile Review UI Specification

Status: approved product behavior; implementation pending.

This specification applies `docs/UI_GUIDELINES.md`, `docs/RESUME_UI_AUDIT.md`, the decisions in `docs/adr/0001` through `0011`, the current frontend components, and the existing backend domain model. It does not authorize a broad `CandidateProfile` naming migration.

## 1. Outcome and scope

The candidate journey is:

`Sign in → Upload resume → Wait for extraction → Review Candidate Profile → Correct extracted information → Save corrections → Start interview`

The redesign covers:

- Initial and replacement Resume uploads
- Extraction progress, rejection, transient failure, and Partial Extraction
- A durable, editable Candidate Profile workspace
- Backend-authoritative Profile Validity and Interview Readiness
- Separate text and speech interview start actions
- Navigation into the existing interview session routes

The redesign does not cover:

- OCR
- A page-count limit
- Recruiter workflows
- A broad Candidate Profile naming migration
- Changes to existing Interview Session snapshots or historical reports
- Automatic persistence of unsaved form edits

## 2. Current implementation seams

The implementation should evolve these existing seams instead of introducing a second UI or domain model:

| Concern | Current seam |
| --- | --- |
| Protected routes | `frontend/src/App.tsx` |
| Shared text/voice setup screen | `frontend/src/pages/TextInterviewPage.tsx` |
| Current read-only profile rendering | Local `CandidateProfilePreview` in `TextInterviewPage.tsx` |
| Introductory marketing content | `frontend/src/components/interview/InterviewExperienceIntro.tsx` |
| Shared controls | `Button`, `Input`, `Label`, `Select`, `Textarea`, `Card`, and `Badge` in `frontend/src/components/ui` |
| Frontend API adapter | `frontend/src/lib/api.ts` |
| Frontend canonical types | `frontend/src/types/index.ts` |
| Upload route | `POST /api/v2/resume/upload` in `backend/gateway/api/resume.py` |
| Interview start route | `POST /api/v2/interview/start` in `backend/gateway/api/interview.py` |
| Canonical backend schema | `backend/shared/schemas/candidate.py` |
| Persistence boundary | `InterviewRepository`, including `update_candidate_profile`, in `backend/infrastructure/repositories/base.py` |

`CandidateProfilePreview` should become a composed review feature rather than grow further inside `TextInterviewPage`. The smallest useful separation is:

- `ResumeUpload`
- `UploadStatus`
- `CandidateProfileReview`
- `InterviewReadinessSummary`
- `ProfileSection`
- Repeatable editors for skill evidence, projects, experiences, and education
- `InterviewStartActions`

These are feature components built from the existing shared controls. They are not a new design system.

The current backend and frontend `CandidateProfile` types do not yet contain `profile_version`, evidence identity/provenance, audit metadata, or upload-operation types. Those are narrow contract additions defined here, not aliases for existing editable fields.

## 3. Route and navigation behavior

### Entry

- `/login` remains the authentication entry.
- `/text-interview` remains the default post-sign-in entry and initially emphasizes text interview intent.
- `/speech-interview` remains a supported entry and initially emphasizes speech interview intent.
- Both entry routes use the same upload and profile-review capability.

### Durable Profile Review

Add a protected canonical route for returning to a persisted profile:

`/candidate-profile/:candidateId`

After an accepted initial upload or successful Replacement Upload, navigate to this route and load the persisted profile from the backend. Do not depend on the in-memory upload response as the durable source of truth.

The entry intent may be preserved as route state or a non-authoritative query value:

- Text entry makes `Start text interview` the primary start action.
- Speech entry makes `Start speech interview` the primary start action.
- A direct or restored profile route defaults to text as the primary start action.

The alternate mode remains a separate secondary action. It must never be hidden behind a menu.

### Interview start

After `POST /api/v2/interview/start` succeeds:

- Text mode navigates to `/text-interview/:sessionId`.
- Speech mode navigates to `/speech-interview/:sessionId`.
- Navigation occurs only after the backend has created the session and immutable profile snapshot.
- A failed start remains in Profile Review, retains saved data, and displays the structured error.

## 4. Page information hierarchy

The Profile Review page uses this order:

1. Page title: `Candidate Profile`
2. Concise explanation: `Review the information used to prepare your interview.`
3. Upload or extraction status, including Partial Extraction when applicable
4. Interview Readiness summary
5. Identity and current role
6. Skills and skill evidence
7. Projects
8. Work experience
9. Education
10. Interview preferences already supported by the current setup flow
11. Save and interview-start actions

Do not render every section as a separate rounded card. Use one main form surface, section headings, spacing, and dividers. The readiness summary may use a bordered status region because it has a distinct operational purpose.

Extraction confidence, method, inferred seniority, evidence source metadata, and audit information do not compete with readiness. If shown, place them in a read-only `Extraction details` disclosure after the editable content.

### Prototype-validated production baseline

Direction B, Professional Workspace, is the selected production baseline:

- At 1024px and 1440px, use a compact two-column workspace with a narrow Interview Readiness and section-navigation rail beside one continuous Candidate Profile editor.
- Readiness issues in the rail link to and focus the corresponding editor fields.
- Do not frame the readiness rail, upload source, every profile section, or every nested entry as separate rounded cards. Use a flat rail, one editor flow, and section or row dividers.
- Use restrained headings, no decorative icons, and compact repeatable-entry rows suited to long profiles.
- Keep a restrained persistent action area at desktop widths. It must not cover focused fields, validation messages, or prototype/diagnostic controls.
- At 768px and 390px, move Interview Readiness above the editor, remove the side rail, and return actions to normal document flow.
- Treat Partial Extraction as an informational warning. It remains prominent until the first successful Profile Review save, but it must not use danger styling.
- While edits are unsaved, `Save corrections` is the only filled primary action and both interview starts remain visible but disabled.
- With an unchanged interview-ready profile, the entry-mode start action is primary and the other mode remains a separate secondary action. Text is the default emphasis when no prior mode intent exists.
- Keep stale-version conflict copy and recovery actions visible without replacing or discarding the local editor state. Present `Reload latest profile` once as the primary recovery action.
- Routine saved or interview-ready confirmation is visually quieter than an actionable warning, validation failure, save failure, or conflict.

These decisions were validated in the isolated deterministic prototype at
`frontend/prototypes/candidate-profile-review-THROWAWAY/`. The prototype is
throwaway evidence and is not part of the production route or API.

## 5. Editable field specification

User-facing labels may be friendly, but state, payloads, responses, schemas, tests, and persistence use the existing canonical keys.

| Canonical key | UI label | Control and behavior |
| --- | --- | --- |
| `name` | Full name | Text input. May be saved blank but prevents Interview Readiness. The extraction fallback `Candidate` also prevents readiness. |
| `years_experience` | Years of experience | Optional numeric input; accepts zero or a nonnegative number. |
| `recent_role` | Most recent role | Optional text input. |
| `specialization` | Specialization | Optional text input. |
| `skills` | Skills | Repeatable normalized text values. Trim values, reject empty values, and deduplicate case-insensitively. Reordering is supported. |
| `skill_evidence` | Skill evidence | Repeatable entries. Existing entries echo their immutable server-issued `evidence_id`; new entries omit it. The associated skill and evidence text are editable. Source and provenance metadata remain read-only. |
| `projects` | Projects | Repeatable editor using existing `name`, `description`, `technologies`, and `role` keys. |
| `experiences` | Work experience | Repeatable editor using existing `company`, `title`, `start_date`, `end_date`, `description`, and `technologies` keys. The label for `title` is `Job title`. |
| `education` | Education | Repeatable structured editor using `institution`, `degree`, `field_of_study`, `start_date`, and `end_date`. A legacy string remains readable and unchanged until the candidate explicitly replaces it with structured entries. |

Nested entries may be added, corrected, reordered, and removed. Reordering must have keyboard-operable `Move up` and `Move down` controls; drag-and-drop may be supplementary but cannot be the only mechanism.

Completely empty nested entries are invalid. Removing an unwanted blank entry is preferable to silently discarding it during save.

### Legacy education

When `education` is a legacy string:

- Display it in a read-only `Legacy education` region.
- Do not infer an institution, degree, field, or dates from it.
- `Replace with structured education` opens an empty structured editor while retaining the legacy value until save succeeds.
- Omitting `education` from PATCH preserves the legacy string.
- PATCH rejects a new string value; it accepts a structured list or `null`.
- A successful explicit replacement increments `profile_version` and retains the original string in read-only audit metadata.
- A stale or failed replacement preserves both the legacy value and local structured draft.

### Read-only data

The form never sends:

- `candidate_id`
- `profile_version` in the JSON body; concurrency uses `If-Match`
- Owner or Firebase user identity
- `confidence`
- `confidence_score`
- `extraction_method`
- `seniority_signal`
- Evidence source metadata such as `source_section`
- Persistence, provenance, correction, and audit metadata

Within `skill_evidence`, `evidence_id` is the only server-issued correlation value that may be echoed in a correction request. It is required for an existing entry, omitted for a new entry, and cannot be changed. `source_section`, origin, correction flags, and timestamps remain omitted.

The backend resolves candidate identity and ownership, recomputes derived values, preserves immutable source metadata, assigns new evidence IDs, and records evidence corrections.

Aliases including `full_name`, `years_of_experience`, and `work_experience` are prohibited in frontend state and API payloads.

## 6. Profile Validity and Interview Readiness

### Profile update validity

An incomplete profile may be saved. A save is valid when:

- Every supplied field has the canonical type and shape.
- `years_experience` is null or nonnegative.
- Skills are trimmed and normalized, empty values are rejected, and duplicates are removed case-insensitively.
- Every `skill_evidence.skill` references a skill in `skills`.
- Nested entries are not completely empty.
- No unknown, alias, or read-only field is present.

Validation runs on blur and on save. The backend remains authoritative.

### Interview Readiness

The latest saved profile is ready only when it has:

- A nonblank `name`
- A `name` other than the extraction fallback `Candidate`
- At least one normalized skill
- At least one interviewable evidence item

An interviewable evidence item is:

- A `skill_evidence` entry with at least one nonblank normalized evidence string; or
- A project with a meaningful `name` or `description`; or
- An experience with a meaningful `title`, `company`, or `description`; or
- Structured education with `institution` and either `degree` or `field_of_study`

`years_experience`, `recent_role`, and `specialization` are optional. Students and interns do not need professional experience or projects when their structured education satisfies the evidence requirement.

For these rules, meaningful text is nonblank after trimming and whitespace normalization. This definition does not introduce a minimum word or character count for individual evidence, project, experience, or education fields.

### Issue presentation

Profile Validity and Interview Readiness use the same structured issue format but remain distinct evaluations. The backend returns every applicable issue. The UI translates codes into specific copy and links each issue to its field or section:

| Code | Origin | UI copy | Focus target |
| --- | --- | --- | --- |
| `missing_name` | Interview Readiness | `Add your full name.` | `name` |
| `fallback_name` | Interview Readiness | `Replace “Candidate” with your full name.` | `name` |
| `missing_skills` | Interview Readiness | `Add at least one skill.` | Skills entry control |
| `missing_interviewable_evidence` | Interview Readiness | `Add skill evidence, a project, work experience, or qualifying education.` | Evidence choice group |
| `invalid_years_experience` | Profile Validity | `Enter zero or a positive number.` | `years_experience` |
| `empty_nested_entry` | Profile Validity | `Complete or remove this entry.` | Exact nested entry |
| `evidence_skill_not_found` | Profile Validity | `Choose a skill that is present in your skills list.` | Exact evidence skill control |

Validity-origin issues block a correction save. They may also block interview start if invalid legacy or extracted data is already persisted. Issue codes are stable programmatic identifiers; user-facing messages may be localized.

## 7. Action hierarchy

Only one action uses the filled primary treatment at a time:

| State | Primary action | Secondary actions |
| --- | --- | --- |
| No file selected | `Choose resume` | None |
| File selected | `Upload and extract` | `Choose another file` |
| Transient upload failure | `Try again` | `Choose another file` |
| Accepted upload | None; open Profile Review automatically | None |
| Unsaved valid or invalid corrections | `Save corrections` | Interview starts remain visible but disabled |
| Unchanged, saved, not ready | `Complete missing details` | Disabled text and speech starts |
| Unchanged, saved, ready after text entry | `Start text interview` | `Start speech interview`, `Replace resume` |
| Unchanged, saved, ready after speech entry | `Start speech interview` | `Start text interview`, `Replace resume` |

`Save corrections`, `Start text interview`, and `Start speech interview` are always distinct controls. Saving never starts an interview.

Start actions are enabled only when:

- The latest server response says the saved profile is interview-ready.
- There are no unsaved corrections.
- The latest profile persistence operation succeeded. A successful accepted upload satisfies this condition until a correction save is attempted; after that, the latest correction save must have succeeded.
- No start request is already in progress.

A pending Replacement Upload does not disable starts for an existing ready profile. Display: `Starting now will use your currently saved Candidate Profile.`

## 8. State behavior

### Upload state model

| State | Required presentation and next action |
| --- | --- |
| `idle` | Format and size guidance; `Choose resume`. |
| `file_selected` | Filename and size; `Upload and extract`; `Choose another file`. |
| `uploading` | `Uploading resume`; progress only when measurable; actions disabled except a supported cancel. |
| `extracting` | `Extracting Candidate Profile`; do not show invented percentage progress. |
| `completed` | Announce `Resume extracted` and open the persisted Profile Review workspace. |
| `completed_with_warning` | Open Profile Review and display `Resume partially extracted` with an explanation that review and correction are required. |
| `validation_rejected` | Actionable rejection message; existing profile unchanged; normally `Choose another file`. |
| `transient_failure` | Explain that no replacement was applied; `Try again`; `Choose another file`. |
| `authentication_required` | Explain that sign-in is required and the file may need to be selected again. |

`partial_extraction` maps to `completed_with_warning`, never to failure. It remains visibly associated with the profile until the first successful Profile Review save and then moves to metadata or history.

### Upload outcome and recovery copy

| Code | Category | Actionable copy |
| --- | --- | --- |
| `unsupported_file_type` | Upload Rejection | `Choose a PDF or DOCX resume.` |
| `file_too_large` | Upload Rejection | `Choose a resume that is 10 MB or smaller.` |
| `empty_file` | Upload Rejection | `This file is empty. Choose another PDF or DOCX.` |
| `encrypted_document` | Upload Rejection | `Remove the document password and upload it again, or choose another file.` |
| `invalid_document` | Upload Rejection | `This file is not a readable PDF or DOCX. Export it again or choose another file.` |
| `no_extractable_text` | Upload Rejection | `No readable text was found. Upload a text-based PDF or DOCX.` |
| `insufficient_text` | Upload Rejection | `This document does not contain enough resume text. Upload a more complete resume.` |
| `idempotency_key_reused` | Request conflict | `This upload attempt no longer matches the selected file. Choose the file again.` |
| `upload_in_progress` | Processing response | `This resume is already being extracted.` |

`idempotency_key_reused` and `upload_in_progress` are not document rejection codes. `upload_in_progress` reflects the existing operation and must not start another extraction.

### Review and save states

| State | Required behavior |
| --- | --- |
| Loading persisted profile | Preserve the form layout with labeled skeleton regions; announce `Loading Candidate Profile`. |
| No persisted profile | Show the upload task, not an empty profile form. |
| Clean and incomplete | Show every readiness issue; primary `Complete missing details`. |
| Dirty | Mark the page as having unsaved corrections; primary `Save corrections`; disable starts. |
| Saving | Keep field values visible; button label `Saving corrections`; prevent duplicate save. |
| Save success | Replace all local form state with the returned server profile; announce `Corrections saved`; update readiness and warning state. |
| Field validation failure | Preserve edits; show every field message; focus the first invalid control. |
| Stale profile conflict | Preserve the local draft and show `Your profile changed in another session. Your current edits have not been discarded.` Primary: `Reload latest profile`. Secondary: `Continue reviewing my local edits`. |
| Unknown/read-only field rejection | Treat as an application contract failure, not user error; preserve edits and expose a recoverable error. |
| Transient save failure | Preserve edits; show `Save corrections` retry; starts remain disabled because the latest save did not succeed. |
| Authentication failure | Preserve edits only for the current page lifetime; require sign-in and do not claim they are persisted. |
| Load failure | Keep navigation available; show `Try loading again`; never show stale local data as saved. |

Success feedback is restrained and announced with a polite live region. It does not use a modal or confetti.

### Unsaved navigation

When corrections are dirty:

- Internal navigation asks whether to stay or discard unsaved corrections.
- Browser unload uses the platform-provided confirmation behavior where supported.
- `Stay and continue editing` is the safe primary choice.
- Discarding returns to the last server profile; unsaved data is never presented as persisted.

## 9. Target API contracts

These contracts describe the required boundary and are not implemented yet.

### Candidate Profile resource

The repositories support multiple Candidate Profiles per authenticated user. Candidate identity therefore appears in an ownership-checked resource path:

- `GET /api/v2/candidates/{candidate_id}/profile`
- `PATCH /api/v2/candidates/{candidate_id}/profile`
- `POST /api/v2/candidates/{candidate_id}/resume` for Replacement Upload

The server never accepts owner identity in a request body. A missing candidate and a candidate owned by another user both return `404 candidate_profile_not_found`.

#### Profile Version and conditional mutation

- Initial upload creates `profile_version: 1`.
- Every successful Profile Correction or Replacement Upload increments the version exactly once.
- Profile GET and successful mutation responses include `ETag: "<profile_version>"`.
- PATCH and Replacement Upload require `If-Match: "<last-read-profile_version>"`.
- `If-Match` accepts exactly one strong quoted decimal version; weak validators, `*`, unquoted values, and lists are rejected.
- `profile_version` is never sent in the JSON or multipart body.
- Missing `If-Match` returns `428 profile_version_required`.
- Malformed or unsupported `If-Match` returns `400 invalid_profile_version_precondition`.
- A nonmatching version returns `412 stale_profile_version` without mutation.
- A normalization-equivalent successful PATCH is still a review mutation: it increments the version, creates an audit event, and can acknowledge Partial Extraction.

After a stale conflict, retain the local draft. Recovery copy is:

`Your profile changed in another session. Your current edits have not been discarded.`

- Primary: `Reload latest profile`
- Secondary: `Continue reviewing my local edits`

Reload replaces the server baseline and leaves the local draft available for comparison; it does not silently merge or resubmit it.

`Continue reviewing my local edits` dismisses the blocking prompt and keeps the draft editable, but Save remains unavailable until the latest profile and ETag have been loaded.

#### Profile response

Profile GET and successful PATCH return `200` with:

```json
{
  "profile": {
    "candidate_id": "123",
    "profile_version": 8,
    "name": "Nguyen An",
    "years_experience": 0,
    "recent_role": null,
    "specialization": "Backend development",
    "skills": ["Python"],
    "skill_evidence": [
      {
        "evidence_id": "5d2edfc8-5f42-43be-99d8-7ef58dcc5725",
        "skill": "Python",
        "evidence": ["Built an interview platform with Python."],
        "source_section": "Projects",
        "origin": "resume_extraction",
        "user_corrected": true,
        "last_corrected_at": "2026-07-27T10:00:00Z",
        "last_corrected_profile_version": 8
      }
    ],
    "projects": [],
    "experiences": [],
    "education": [
      {
        "institution": "Example University",
        "degree": "Bachelor of Science",
        "field_of_study": "Computer Science",
        "start_date": null,
        "end_date": null
      }
    ],
    "seniority_signal": "entry",
    "confidence": 0.72,
    "confidence_score": 0.72,
    "extraction_method": "resume"
  },
  "readiness": {
    "is_ready": true,
    "issues": []
  },
  "warnings": [],
  "metadata": {
    "last_mutation": {
      "profile_version": 8,
      "occurred_at": "2026-07-27T10:00:00Z",
      "source": "candidate_review",
      "changed_fields": ["skill_evidence"]
    },
    "partial_extraction": {
      "occurred": true,
      "upload_id": "8dc9ba6c-512f-4668-a490-e1e32a95e355",
      "detected_at": "2026-07-27T09:30:00Z",
      "acknowledged_at": "2026-07-27T10:00:00Z",
      "acknowledged_profile_version": 8
    },
    "legacy_education_replacement": null
  }
}
```

`source` is one of `resume_extraction`, `candidate_review`, `replacement_upload`, or `system_backfill`. Audit timestamps use UTC RFC 3339. Audit metadata contains no owner or mutable user identity.

When a legacy education string is explicitly replaced, `legacy_education_replacement` is:

```json
{
  "original_text": "BSc Computer Science, Example University",
  "replaced_at": "2026-07-27T10:00:00Z",
  "replacement_profile_version": 8
}
```

The original value is immutable audit metadata. It is not copied into invented structured fields.

#### Profile correction request

PATCH accepts any nonempty subset of the nine canonical editable top-level keys. A supplied list replaces that entire list, preserving submitted order.

Existing Skill Evidence entries include their server-issued `evidence_id` solely for correlation:

```json
{
  "skills": ["Python", "FastAPI"],
  "skill_evidence": [
    {
      "evidence_id": "5d2edfc8-5f42-43be-99d8-7ef58dcc5725",
      "skill": "FastAPI",
      "evidence": ["Built authenticated APIs."]
    },
    {
      "skill": "Python",
      "evidence": ["Created data-processing tools."]
    }
  ]
}
```

- Existing IDs must belong to the target profile.
- New entries omit `evidence_id`; the server assigns a lowercase hyphenated UUID v4.
- Duplicate or unknown IDs return a validation issue.
- Clients cannot choose an ID for a new entry or change an existing ID.
- `source_section`, origin, correction flags, timestamps, and audit metadata are forbidden in the request.
- Editing an existing entry's skill or evidence sets `user_corrected: true`; reordering alone does not.
- Removing an entry removes it from the current profile while its immutable provenance remains in audit history.
- Existing entries receive persisted IDs through a one-time `system_backfill` before the structured editor receives them.
- Backfill initializes an unversioned profile at version 1. If a versioned profile still requires metadata backfill, the atomic backfill increments its version once and records a `system_backfill` audit event.

PATCH accepts `education` only as `list[CandidateEducation]` or `null`. Existing string education remains unchanged when `education` is omitted and is preserved in audit metadata when explicitly replaced.

Correction validation uses these additional stable issue codes:

| Code | Meaning |
| --- | --- |
| `unknown_field` | An unknown or alias field was submitted. |
| `read_only_field` | A prohibited identity, source, version, derived, confidence, or audit field was submitted. |
| `empty_update` | PATCH did not contain an editable canonical field. |
| `evidence_id_invalid` | The evidence ID is not a valid UUID-style identifier. |
| `evidence_id_not_found` | The ID is not an existing entry on the owned target profile. |
| `duplicate_evidence_id` | The same existing entry appears more than once. |
| `invalid_education_shape` | PATCH attempted to submit legacy string education or a malformed structured entry. |
| `empty_skill` | A skill becomes empty after normalization. |

### Audit and warning persistence

Every successful profile mutation appends an immutable audit event:

```json
{
  "profile_version": 8,
  "occurred_at": "2026-07-27T10:00:00Z",
  "source": "candidate_review",
  "changed_fields": ["skill_evidence", "education"],
  "evidence_changes": [
    {
      "evidence_id": "5d2edfc8-5f42-43be-99d8-7ef58dcc5725",
      "change": "corrected"
    }
  ]
}
```

`evidence_changes.change` is `added`, `corrected`, `reordered`, or `removed`. The audit store retains source metadata for removed evidence. It never records an ownership change from this endpoint.

The server derives audit `source` from the authenticated operation; clients never submit it.

A normalization-equivalent review save records `changed_fields: []` while still creating the new review Profile Version and acknowledgement.

Partial Extraction persistence contains two distinct facts:

1. The immutable original warning: upload ID and detection time.
2. The acknowledgement: the time and Profile Version of the first successful `candidate_review` PATCH after that warning.

Before acknowledgement, Profile responses include:

```json
{
  "code": "partial_extraction",
  "message": "Resume partially extracted.",
  "acknowledged": false
}
```

After acknowledgement, the warning is omitted from prominent `warnings`; `metadata.partial_extraction` remains available.

### Resume upload resources

#### Initial upload

`POST /api/v2/resume/upload`

- Creates a new Candidate Profile because one user may own multiple profiles.
- Accepts exactly one multipart part named `file`.
- Requires `Idempotency-Key`.
- Does not accept `candidate_id` or owner identity.

#### Replacement Upload

`POST /api/v2/candidates/{candidate_id}/resume`

- Ownership-checks the path candidate.
- Requires both `Idempotency-Key` and `If-Match`.
- Applies the replacement only if the expected Profile Version still matches at atomic commit.
- Increments `profile_version` once on success.
- A pending, failed, rejected, or stale replacement preserves the existing profile and raw Resume.

For idempotency scope, the operation is `initial_resume_upload` or `replacement_resume_upload:{candidate_id}:{expected_profile_version}`. The file fingerprint is SHA-256 content hash, detected document type, and byte size. Retrying a stale replacement after loading a newer Profile Version is a new upload intent and requires a new idempotency key.

#### Multipart cardinality

- Zero files returns `422 request_validation_failed`.
- More than one file-bearing multipart part, regardless of field name, returns `400 multiple_files_not_allowed`.
- Cardinality rejection occurs before extraction or Candidate Profile mutation.

#### Idempotency lifecycle

- Persist the idempotency record after cardinality and fingerprint calculation but before extraction.
- Bind it to authenticated user, operation including replacement target, key, SHA-256 content hash, detected type, and byte size.
- Retain `completed` and deterministic `rejected` records for 24 hours after finalization.
- Retain `retryable_failure` for 24 hours after its last update.
- A `processing` record whose lease has not been updated for 30 minutes becomes `retryable_failure`.
- Explicit retry with the same key and file may atomically acquire a new processing lease.
- Each lease has a fencing generation; a superseded worker cannot persist a profile or finalize the operation.
- Reuse with different content, operation, or replacement target returns `409 idempotency_key_reused`.
- Deterministic rejection replay returns the original status and error body; completed replay returns the original Upload Success body.
- After a terminal record expires, replay guarantees end; a client should generate a new key rather than reuse an expired one.
- An expired upload operation is no longer available from the status route and returns `404 upload_not_found`.

No file upload or extraction is automatically retried. The one authentication-token refresh may resubmit the same request once with the same key and body.

#### Upload status and recovery

An upload operation has an opaque `upload_id` and authenticated status resource:

`GET /api/v2/resume/uploads/{upload_id}`

The resource is owner-scoped and returns `404 upload_not_found` for missing or foreign operations. A duplicate POST while the original lease is active returns `202` with:

```json
{
  "code": "upload_in_progress",
  "upload": {
    "upload_id": "8dc9ba6c-512f-4668-a490-e1e32a95e355",
    "state": "processing",
    "status_url": "/api/v2/resume/uploads/8dc9ba6c-512f-4668-a490-e1e32a95e355",
    "created_at": "2026-07-27T09:30:00Z",
    "updated_at": "2026-07-27T09:31:00Z",
    "stale_at": "2026-07-27T10:01:00Z",
    "expires_at": null
  },
  "retry_after_seconds": 5
}
```

It also sends `Location` with `status_url` and `Retry-After: 5`. The UI may poll that GET after the stated interval; status polling is not an upload retry because it does not retransmit the file.

The status response always contains `upload`, `result`, and `error`:

- `result` is the original Upload Success response when `completed`; otherwise null.
- `error` is the common error object when `rejected` or `retryable_failure`; otherwise null.
- Both are null while `processing`.

When status becomes `retryable_failure`, show `Try again`; explicit retry resubmits the in-memory file with the original key. If the file is no longer available, show `Choose another file`.

#### Upload Success

Initial and replacement success retain the existing top-level upload fields and add the new contract:

```json
{
  "candidate_id": "123",
  "profile": {
    "candidate_id": "123",
    "profile_version": 1,
    "name": "Nguyen An",
    "skills": ["Python"]
  },
  "confidence_score": 0.72,
  "readiness": {
    "is_ready": false,
    "issues": [
      {
        "code": "missing_interviewable_evidence",
        "origin": "interview_readiness",
        "field_path": "skill_evidence"
      }
    ]
  },
  "warnings": [],
  "metadata": {
    "last_mutation": {
      "profile_version": 1,
      "occurred_at": "2026-07-27T09:30:00Z",
      "source": "resume_extraction",
      "changed_fields": [
        "name",
        "years_experience",
        "recent_role",
        "specialization",
        "skills",
        "skill_evidence",
        "projects",
        "experiences",
        "education"
      ]
    },
    "partial_extraction": null,
    "legacy_education_replacement": null
  },
  "upload": {
    "upload_id": "8dc9ba6c-512f-4668-a490-e1e32a95e355",
    "state": "completed",
    "status_url": "/api/v2/resume/uploads/8dc9ba6c-512f-4668-a490-e1e32a95e355",
    "expires_at": "2026-07-28T09:30:00Z"
  }
}
```

The abbreviated `profile` above illustrates compatibility fields; the actual response contains the complete Candidate Profile shape used by Profile GET.

Successful initial and replacement upload responses include `ETag: "<profile_version>"`.

Upload Success with Partial Extraction has the same `200` response and includes:

```json
{
  "code": "partial_extraction",
  "message": "Resume partially extracted.",
  "acknowledged": false
}
```

in `warnings`. Partial Extraction is never returned in `error`.

For that response, `metadata.partial_extraction` records `occurred: true`, the same `upload_id`, `detected_at`, and null acknowledgement fields.

### Common issue and error structures

Every structured issue is:

```json
{
  "code": "evidence_skill_not_found",
  "origin": "profile_validity",
  "field_path": "skill_evidence.0.skill"
}
```

`origin` is `profile_validity` or `interview_readiness`. `field_path` is omitted only when no specific field applies.

Every new failure response is:

```json
{
  "error": {
    "code": "profile_validation_failed",
    "message": "Some profile fields need attention.",
    "retryable": false,
    "issues": [
      {
        "code": "evidence_skill_not_found",
        "origin": "profile_validity",
        "field_path": "skill_evidence.0.skill"
      }
    ]
  },
  "request_id": "req_01J3..."
}
```

Messages are user-safe fallbacks; clients use stable codes for localized copy.

A stale-version response adds:

```json
{
  "conflict": {
    "current_profile_version": 9,
    "current_etag": "\"9\""
  }
}
```

inside `error`. It does not include or overwrite the client's draft.

For an upload-related transient failure with a persisted operation, `error` also includes:

```json
{
  "recovery": {
    "upload_id": "8dc9ba6c-512f-4668-a490-e1e32a95e355",
    "status_url": "/api/v2/resume/uploads/8dc9ba6c-512f-4668-a490-e1e32a95e355"
  }
}
```

### HTTP status mapping

| Status | Code or result | Applies to |
| --- | --- | --- |
| `200` | Profile response | Profile GET or PATCH success |
| `200` | Upload Success | Initial or Replacement Upload completed, with or without warnings |
| `200` | Interview Session response | Interview start success |
| `200` | Upload status response | Owned status lookup |
| `202` | `upload_in_progress` | Duplicate POST while the original upload is processing |
| `400` | `multiple_files_not_allowed` | More than one multipart file |
| `400` | `idempotency_key_required` | Missing upload idempotency header |
| `400` | `invalid_profile_version_precondition` | `If-Match` is not one strong quoted decimal version |
| `401` | `authentication_required` | Missing, invalid, or expired authentication after one refresh |
| `404` | `candidate_profile_not_found` | Missing or foreign Candidate Profile |
| `404` | `upload_not_found` | Missing or foreign upload operation |
| `409` | `idempotency_key_reused` | Key reused with different content, operation, or target |
| `412` | `stale_profile_version` | `If-Match` does not match the current version |
| `413` | `file_too_large` | File exceeds 10 × 1024 × 1024 bytes |
| `415` | `unsupported_file_type` | Actual document type is not PDF or DOCX |
| `422` | `empty_file`, `encrypted_document`, `invalid_document`, `no_extractable_text`, or `insufficient_text` | Deterministic document rejection |
| `422` | `profile_validation_failed` | Correction payload is invalid |
| `422` | `request_validation_failed` | Required multipart file is missing |
| `422` | `profile_not_interview_ready` | Interview start fails authoritative readiness |
| `428` | `profile_version_required` | Missing `If-Match` on PATCH or Replacement Upload |
| `503` | `transient_service_failure` | Retryable extraction, persistence, orchestration, or dependency failure |

For `503` during upload, the error includes `upload_id` and `status_url` when an idempotency record exists. The operation becomes `retryable_failure`; explicit retry uses the same key and file.

### Interview start

`POST /api/v2/interview/start` retains its existing request shape and does not accept a client profile or Profile Version:

```json
{
  "candidate_id": "123",
  "interview_config": {
    "mode": "text",
    "language": "en",
    "experience_level": "intern"
  }
}
```

The start transaction:

1. Authenticates the user.
2. Atomically reads the latest committed owned Candidate Profile and its `profile_version`.
3. Runs Profile Validity and the shared Interview Readiness evaluator on that committed version.
4. Rejects a non-ready profile with `422 profile_not_interview_ready` and every applicable issue.
5. Creates the Interview Session with an immutable Candidate Profile snapshot and `candidate_profile_version`.

This atomic read-and-create selects the snapshot version. A Replacement Upload or Profile Correction committed before the transaction is included; one committed afterward is not. Pending uploads are never included. Orchestration uses the stored snapshot, and later profile mutations never alter the session or its reports.

Interview start retains the existing successful response shape and adds the selected version to session state:

```json
{
  "session_id": "session-123",
  "state": {
    "candidate_profile_version": 8,
    "candidate_profile": {
      "candidate_id": "123",
      "profile_version": 8
    }
  }
}
```

The abbreviated `state` above only highlights the added version fields; all existing interview state fields remain.

## 10. Shared normalization contract

The backend applies these steps before Profile Validity, Interview Readiness, persistence, or the 50-character Resume threshold:

1. Apply Unicode NFKC.
2. Treat Unicode whitespace as whitespace, including nonbreaking spaces.
3. Trim leading and trailing Unicode whitespace.
4. For names, roles, specialization, skills, evidence, project text, experience text, education text, technologies, and extracted Resume text, collapse each internal Unicode whitespace run to one ASCII space.
5. Preserve letters, diacritics, capitalization, digits, and punctuation.
6. Reject a required or list-item string whose normalized value is empty.

Date strings receive NFKC and surrounding trim, but internal whitespace is not collapsed. This feature does not introduce a new date-format migration. A retained legacy education string is not rewritten, and its audit copy preserves the original persisted value.

Additional rules:

- Preserve display capitalization for names and skills.
- Compare the fallback name by `casefold(NFKC(normalized_name)) == "candidate"`.
- `name` may persist as `""` for an incomplete valid profile and then produces `missing_name`.
- Normalize empty optional scalar fields such as `recent_role`, `specialization`, optional roles, and optional dates to `null`.
- Preserve empty strings for canonical required-string members inside a nonempty nested object where the current schema uses strings; reject the entry only when every meaningful member is empty.
- Reject normalized-empty items inside `skills`, `technologies`, and evidence-text lists rather than silently dropping them.
- Use `casefold(NFKC(normalized_skill))` as the skill comparison key.
- Preserve the first accepted display spelling and order when deduplicating skills.
- Reject later normalized-empty skills; do not silently remove them.
- Match `skill_evidence.skill` to `skills` through the comparison key and persist the accepted skill display spelling.
- Normalize evidence whitespace without removing or rewriting meaningful punctuation.
- Count Unicode code points in normalized Resume text, including single internal separator spaces; accept at 50 or more and return `insufficient_text` below 50.
- Numeric `years_experience` is not text-normalized; it must be finite and nonnegative when present.

### Normalization test vectors

| Input | Field | Expected |
| --- | --- | --- |
| `"  Nguyễn   Văn\tAn  "` | `name` | `"Nguyễn Văn An"` |
| `"Vie\u0302\u0323t Nam"` | any text | `"Việt Nam"` |
| `"Ｃ＋＋"` | skill | `"C++"` |
| `[" Python ", "PYTHON", "Ｐｙｔｈｏｎ"]` | skills | `["Python"]` |
| `["C++", "c++"]` | skills | `["C++"]` |
| `"  PYTHON "` with skills `["Python"]` | `skill_evidence.skill` | Match and persist `"Python"` |
| `"Built\tAPI.\nReduced  latency—without regressions."` | evidence | `"Built API. Reduced latency—without regressions."` |
| `"\u00A0\t\n"` | required or list-item string | Normalized empty; reject |
| `" \t "` | `name` | `""`; saveable but `missing_name` |
| `" \t "` | `recent_role` | `null` |
| `"  Trường Đại học Bách Khoa  "` | `education.institution` | `"Trường Đại học Bách Khoa"` |
| 49 normalized code points | Resume text | `422 insufficient_text` |
| 50 normalized code points | Resume text | Accepted for extraction |
| `-0.5` | `years_experience` | `invalid_years_experience` |
| `NaN` or infinity | `years_experience` | Validation failure |

Frontend code may apply the same rules for immediate feedback, but only the normalized server response replaces the saved baseline.

## 11. Responsive behavior

All behavior must work at 1440px, 1024px, 768px, and 390px.

| Width | Layout |
| --- | --- |
| 1440px | Use the shared 1280px content frame. Main form and a narrower readiness/action rail may use two columns. |
| 1024px | Retain two columns only when labels, errors, and actions do not wrap awkwardly; otherwise use one column. |
| 768px | Use one column. Readiness appears before editable sections. No side rail. |
| 390px | Use 16px gutters, one column, full-width primary action, and stacked start actions. Repeatable-entry actions remain at least 44px high. |

At every width:

- Keep page title, status, form, and actions aligned to the same content frame.
- Preserve the approved section order.
- Do not hide readiness issues in a hover interaction.
- Do not use horizontal scrolling for form content.
- Sticky actions, if used at larger widths, must not cover focused fields or validation messages and must become normal-flow content on narrow screens.

## 12. Accessibility

- Use one `h1` and ordered `h2` section headings.
- Use a real `form` with visible labels and native controls where possible.
- Connect helper and error copy through `aria-describedby`.
- Set `aria-invalid` on invalid fields.
- Use `role="status"` or polite live regions for extraction, save, and start progress.
- Use an assertive alert only when immediate intervention is required.
- When an issue link is activated, focus the field and scroll it into view without obscuring it.
- After failed save, focus the first invalid field.
- After adding a nested entry, move focus to its first field.
- After removing an entry, return focus to a predictable adjacent control.
- Make file selection keyboard accessible; drag-and-drop is optional.
- Do not communicate warning, error, success, or disabled state through color alone.
- Maintain WCAG AA text contrast, 3:1 control boundaries, visible keyboard focus, 44px touch targets, reduced-motion support, and logical source order.

## 13. Safe implementation assumptions

- The new canonical profile route is additive; existing session routes remain unchanged.
- Text is the default start emphasis when no prior mode intent exists.
- A successful accepted upload is the latest successful profile persistence operation until the candidate attempts to save corrections.
- Existing Interview Session snapshots are not backfilled with new Profile Versions or evidence IDs.
- System backfill updates current Candidate Profile metadata only and never rewrites prior sessions or reports.

## 14. Related documentation

- `docs/UI_GUIDELINES.md`
- `docs/RESUME_UI_AUDIT.md`
- `docs/RESUME_REVIEW_TESTING_SEAMS.md`
- `docs/RESUME_REVIEW_IMPLEMENTATION_RISKS.md`
- `docs/adr/0001-reviewed-candidate-profile-source-of-truth.md`
- `docs/adr/0002-strict-candidate-profile-correction-contract.md`
- `docs/adr/0003-separate-profile-validity-from-interview-readiness.md`
- `docs/adr/0004-resume-upload-and-partial-extraction-contract.md`
- `docs/adr/0005-idempotent-atomic-resume-upload-retries.md`
- `docs/adr/0006-make-profile-review-a-durable-workspace.md`
- `docs/adr/0007-use-owned-versioned-candidate-profile-resources.md`
- `docs/adr/0008-preserve-profile-provenance-through-explicit-identities.md`
- `docs/adr/0009-use-recoverable-resume-upload-operations.md`
- `docs/adr/0010-standardize-resume-review-api-responses.md`
- `docs/adr/0011-use-shared-nfkc-text-normalization.md`
- `docs/adr/0012-select-professional-candidate-profile-workspace.md`
