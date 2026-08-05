# InterviewOS repository instructions

These instructions apply to the entire repository. Read `CONTEXT.md`, the
relevant specification, testing-seam document, implementation-risk document,
and ADRs before changing a domain contract.

## Repository architecture

- `frontend/` is a React 18, TypeScript, Vite, React Router, TanStack Query, and
  Zustand application. Production routes are declared in `frontend/src/App.tsx`;
  reusable controls live in `frontend/src/components/ui`; feature and layout
  components live under `frontend/src/components`; API access is centralized in
  `frontend/src/lib/api.ts`; canonical client contracts live in
  `frontend/src/types`.
- `backend/gateway/` is the active FastAPI HTTP boundary. Routes obtain
  authentication and application dependencies from `backend/core/dependencies.py`.
- `backend/shared/schemas/` contains canonical Pydantic domain and transport
  schemas shared by the active backend.
- `backend/services/` and `backend/orchestrator/` contain application and
  interview workflow logic. Routes should stay thin.
- `backend/infrastructure/` contains Firebase authentication, document
  extraction, LLM/speech integrations, and the SQLite and Firestore repository
  implementations. Both repositories must honor the same public contract.
- `backend/app/tests/` contains the current backend test suite, including API,
  ownership, repository, interview, report, upload, and speech tests.
- `backend/app/` also contains older compatibility modules. Do not create a
  second implementation path there when the active `gateway`, `shared`,
  `services`, or `infrastructure` seam already owns the behavior.
- `docs/adr/` contains binding architectural decisions. `docs/RESUME_REVIEW_UI_SPEC.md`
  and `docs/RESUME_REVIEW_TESTING_SEAMS.md` are the normative Resume Review
  behavior and testing contracts.
- `frontend/prototypes/` is throwaway design evidence. It is not a production
  source directory.

There are currently no checked-in `.github/workflows` CI workflows. Local
validation described below is therefore mandatory.

## Development commands

Install dependencies:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt

cd ..\frontend
npm ci
```

Run the backend from `backend/`:

```powershell
python -m uvicorn gateway.main:app --reload --host 127.0.0.1 --port 8000
```

The repository-level helper is:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_backend.ps1
```

Run the frontend from `frontend/`:

```powershell
npm run dev -- --host localhost
```

The optional speech service is started from the repository root with
`scripts/run_speech_service.ps1`. See `docs/local-development.md` before running
the complete three-service environment.

## Typecheck, lint, test, and build

Frontend commands, run from `frontend/`:

```powershell
npm exec tsc -- -b
npm run lint
npm test
npm run build
```

Run one focused frontend test while implementing:

```powershell
npm test -- src/path/to/Feature.test.tsx
```

Backend commands, run from `backend/` with the virtual environment active:

```powershell
python -m pytest
python -m compileall -q core gateway infrastructure orchestrator services shared speech_service
```

Run focused backend tests while implementing:

```powershell
python -m pytest app/tests/test_target.py -q
python -m pytest app/tests/test_target.py::TestClass::test_behavior -q
```

No backend static type checker or linter is currently configured. Do not claim a
backend typecheck or lint pass that the repository does not provide. Python
compilation and pytest are the required checked-in validation seams.

## Firebase authentication and ownership

- Production HTTP requests require a Firebase ID token in
  `Authorization: Bearer <token>`. The frontend obtains it from the current
  Firebase user; the backend verifies it through Firebase Admin.
- Route handlers resolve `CurrentUser` with `get_current_user`. Do not accept a
  user ID, owner ID, or ownership change from an untrusted body.
- Every Candidate Profile, Resume, Interview Session, upload operation, status
  resource, and report lookup or mutation must be scoped to `current_user.uid`.
- Candidate IDs are resource identifiers, not proof of access. Resolve the
  resource through an ownership-checking repository call.
- Foreign and missing owned resources should use the documented indistinguishable
  `404` behavior. Never reveal another user's resource existence.
- `AUTH_ENABLED=false` and `AUTH_DEV_USER_ID` are local-development behavior,
  not authorization shortcuts for production code or tests.
- Never bypass ownership checks to make a test pass.

## Candidate Profile contract

The only canonical editable top-level `CandidateProfile` keys are:

- `name`
- `years_experience`
- `recent_role`
- `specialization`
- `skills`
- `skill_evidence`
- `projects`
- `experiences`
- `education`

Do not introduce parallel aliases such as `full_name`,
`years_of_experience`, or `work_experience` in requests, responses, frontend
state, schemas, repositories, tests, or persistence.

Use the existing nested names:

- Project: `name`, `description`, `technologies`, `role`
- Experience: `company`, `title`, `start_date`, `end_date`, `description`,
  `technologies`
- Structured education: `institution`, `degree`, `field_of_study`,
  `start_date`, `end_date`
- Skill Evidence: `skill`, `evidence`, and the server-issued `evidence_id`
  correlation key for existing entries

Friendly UI labels do not change canonical keys. Correction schemas must use a
strict allowlist and reject unknown, alias, and read-only fields with structured
validation errors. Never silently ignore or map them. Source, provenance,
ownership, derived, confidence, version, persistence, and audit metadata are
read-only. `evidence_id` and evidence source metadata remain server-controlled;
new evidence omits an ID.

Legacy string `education` remains readable. Do not invent structured fields from
it. The candidate may explicitly replace it with structured entries, and the
original string must remain in audit metadata.

## Profile Version and conditional mutation

- `profile_version` is a monotonically increasing server-controlled Profile
  Version exposed by profile responses.
- Profile GET returns the strong ETag for that version.
- Profile PATCH and Replacement Upload require the last-read strong version in
  `If-Match`. Do not send `profile_version` in the JSON body.
- Missing, weak, wildcard, unquoted, or multi-value preconditions fail with the
  documented structured response.
- Compare the version, persist the complete mutation and audit event, and
  increment exactly once in one repository transaction.
- A stale mutation returns `412 stale_profile_version`, preserves the current
  server state and local draft, and must not be automatically merged or retried.

## Profile Validity and Interview Readiness

Profile Validity and Interview Readiness are different:

- Valid incomplete profiles may be saved incrementally.
- The backend is the authoritative source for Interview Readiness.
- One shared backend validator must serve profile responses and both text and
  speech interview-start actions.
- A saved profile is interview-ready only when it has a nonblank nonfallback
  `name`, at least one normalized skill, and at least one interviewable evidence
  item from Skill Evidence, a meaningful project or experience, or qualifying
  structured education.
- The frontend displays and links the backend's complete structured readiness
  issue list. It may provide advisory validation but must not independently
  redefine readiness.
- `POST /api/v2/interview/start` must reject a non-ready profile even if the
  client enables the action incorrectly.

## Immutable Interview Session snapshots

- Interview start reloads the latest committed owned Candidate Profile; it never
  accepts local profile edits or profile data in the start body.
- Session creation atomically stores an immutable Candidate Profile snapshot and
  the exact `candidate_profile_version` selected.
- Orchestration uses the stored snapshot.
- Later Profile Corrections or Replacement Uploads must not modify existing
  Interview Session snapshots, session state, generated reports, or historical
  reports.
- Do not backfill new profile metadata into existing sessions or reports.

## Resume upload idempotency

- Initial and Replacement Uploads require an opaque `Idempotency-Key` header.
- Bind the key to authenticated user, operation, replacement target when
  applicable, expected Profile Version when applicable, SHA-256 content hash,
  detected document type, and file size.
- Persist the idempotency record before extraction. Supported states are
  `processing`, `completed`, `rejected`, and `retryable_failure`.
- Concurrent duplicates return `202 upload_in_progress` and the owned status
  resource. They never start another extraction.
- Reusing a key for different content, operation, target, or expected version
  returns `idempotency_key_reused`.
- Completed and deterministic rejected results replay for 24 hours.
  Retryable failures expire 24 hours after their last update.
- A processing lease inactive for 30 minutes is recoverable through a new fenced
  generation; a stale worker cannot commit.
- Selecting another file creates a new key. Explicit retry of the same in-memory
  file reuses the key. Only one authentication-token refresh may resubmit the
  same request automatically.
- Exactly one genuine PDF or DOCX up to 10 MB is accepted. More than one
  multipart file returns `multiple_files_not_allowed`.
- Failed, rejected, pending, or interrupted Replacement Uploads do not modify or
  reduce the readiness of the existing profile. Successful replacement is
  atomic. Partial Extraction is a successful replacement with a warning.

## Frontend design and component conventions

- Follow `docs/UI_GUIDELINES.md`, ADR 0012, and
  `docs/RESUME_REVIEW_UI_SPEC.md`.
- Reuse existing `Button`, `Input`, `Label`, `Select`, `Textarea`, `Card`, and
  `Badge` primitives where their semantics fit. Extend a primitive narrowly when
  necessary; do not introduce a new component library.
- Use the existing color tokens, Satoshi/Segoe UI typography, Tailwind setup,
  focus treatment, and `cn` utility.
- For Candidate Profile Review, Direction B is a behavioral and visual
  reference only: a compact desktop readiness/navigation rail, one continuous
  editor, restrained actions, and readiness above the editor on mobile.
- Do not copy throwaway prototype components, mock reducers, hardcoded data, or
  temporary CSS into production. Write production components against the real
  repository architecture and API contracts.
- Do not add gradients, glassmorphism, decorative shapes, decorative icons,
  oversized headings, unnecessary animation, or a rounded card for every
  section. Use one accent, the 8px spacing system, restrained dividers, and
  consistent content alignment.
- Keep one obvious primary action per state. Save, text start, and speech start
  remain separate controls.
- Do not redesign unrelated routes or global layout while implementing Resume
  Review.

## Accessibility

- Use one page `h1`, ordered section headings, semantic form and disclosure
  elements, visible labels, and logical source and keyboard order.
- Associate helper and error text with controls through `aria-describedby`; set
  `aria-invalid` for invalid fields.
- Readiness links must move focus to visible relevant controls without sticky
  UI covering them.
- Loading and progress announcements use polite live regions. Assertive alerts
  are reserved for conditions requiring immediate intervention.
- After failed save, focus the first invalid field. After add/remove/reorder,
  move focus predictably.
- All functionality must be keyboard operable. Drag and drop cannot be the only
  reorder mechanism.
- Maintain WCAG AA text contrast, visible focus, 3:1 control boundaries, 44px
  touch targets, reduced-motion support, and no status conveyed by color alone.
- Verify 1440px, 1024px, 768px, and 390px without horizontal overflow. At 768px
  and below, Profile Review is single-column with readiness before the editor.

## Required validation before completing a ticket

1. Start from the ticket's declared public testing seams and write focused
   behavioral tests. Do not test private implementation details.
2. Run the focused test after each small change.
3. Run relevant ownership, API contract, repository, and regression tests for
   every touched backend behavior.
4. Run relevant React Testing Library tests for every touched frontend behavior.
5. Run frontend TypeScript, lint, the full frontend test suite, and the
   production frontend build.
6. Run the full relevant backend pytest suite and Python compilation.
7. For user-visible responsive changes, capture or exercise 1440px, 1024px,
   768px, and 390px; complete keyboard and accessibility smoke checks.
8. Run any checked-in Playwright smoke or visual regression seam relevant to the
   route. If none exists, report that honestly rather than claiming it passed.
9. Review the final diff against the ticket, the applicable ADRs, documented
   standards, and unrelated-route scope.
10. Report commands run, results, unresolved risks, and meaningful visual or
    behavioral differences.

Use focused tests during implementation and the full relevant suites before
completion. Do not modify production code outside the approved ticket. Do not
commit unless the user explicitly instructs you to commit.
