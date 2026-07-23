# Production deployment report

Deployment date: 2026-07-23

## Deployment

- Status: deployed; automated backend/data E2E checks and manual Google Sign-In passed.
- Cloud Run service: `ai-interview-backend`
- Revision: `ai-interview-backend-00004-wwk` (100% traffic)
- Image: `us-central1-docker.pkg.dev/project-7dffc340-f73f-4e62-aec/ai-interview/backend@sha256:2473e07507705b07ab8c0ddca9c4244291461cd9fc491f988479ee0d78d7c59d`
- Region: `us-central1`
- Service URL: `https://ai-interview-backend-obfi25ugxa-uc.a.run.app`
- Service account: `ai-interview-runtime@project-7dffc340-f73f-4e62-aec.iam.gserviceaccount.com`
- Frontend URL: `https://project-7dffc340-f73f-4e62-aec.web.app`
- Firebase Hosting version: `6ddfa6ca156fb911`

Cloud Run uses generation 2, one Uvicorn process, 1 CPU, 1 GiB memory, concurrency 20, a 300-second timeout, minimum zero instances, and maximum five instances. Public Cloud Run invocation is intentional; Firebase authentication remains enforced by FastAPI on protected routes.

## Remote verification

| Check | Result |
| --- | --- |
| `GET /health` | PASS - 200 |
| `GET /ready` | PASS - 200 with Firestore readiness |
| Protected endpoint without token | PASS - 401 |
| Authenticated `/api/v2/auth/me` | PASS - 200 with a real Firebase ID token |
| Google Sign-In browser flow | PASS - provider enabled and production redirect completed |
| Firebase refresh token | PASS - refreshed token accepted |
| Resume upload and CandidateProfile | PASS - Vertex AI extraction and Firestore persistence |
| Interview planning and question generation | PASS - Vertex AI through Cloud Run ADC |
| Answer evaluation and configured completion limit | PASS - completed after 1 of 1 configured answers |
| Final report generation | PASS - persisted and idempotent |
| Interview history | PASS |
| Cross-user candidate isolation | PASS - 404 |
| Cross-user session isolation | PASS - 404 |
| Cross-user report isolation | PASS - 404 |
| Firestore hierarchy | PASS - data scoped below `users/{uid}` |
| Production CORS | PASS - exact Hosting origin accepted |
| Cloud Logging correlation | PASS - request ID found on revision `00003-g6p` |
| Log privacy sample | PASS - no authorization field or request body |
| Frontend root and SPA route | PASS - 200 and same SPA shell |
| Frontend cache policy | PASS - SPA no-cache; hashed assets immutable for one year |
| Interview mode default compatibility | PASS - omitted mode defaults to `text` |
| Voice mode contract and persistence | PASS - API response and Firestore top-level/nested state contain `voice` |
| Production mode selector bundle | PASS - Text and Speech choices plus Phase 2 boundary present |

The E2E accounts and Firestore documents were removed after verification. Email/password authentication was enabled only for the automated Firebase token test and restored to disabled.

## Security and infrastructure

- Firestore is Native mode in `us-central1` with delete protection enabled.
- The runtime service account has Vertex AI User, Cloud Datastore User, Firebase Authentication Viewer, and Logs Writer roles.
- The deployed service has no `GOOGLE_APPLICATION_CREDENTIALS` setting and uses ADC from its service identity.
- The Cloud Build upload contained 124 files and no `.env`, database, virtual environment, test, or credential-shaped files.
- The final local image runs as user `app` and contains no `.env`, SQLite database, or credential-shaped files.
- Authorized Domains contains only the Firebase Hosting `web.app` and `firebaseapp.com` domains.

## Build verification

- Backend: 104 tests passed with `unittest`.
- Python compile check: passed.
- Python dependency check: passed.
- Frontend TypeScript/Vite production build: passed.
- Production dependency audit: 0 vulnerabilities.
- Docker production build and local production smoke: passed.
- `git diff --check`: passed; Git only reports expected Windows line-ending notices.

## Frontend resume flow

The production Text Interview screen now accepts PDF/DOCX resumes, previews the extracted profile, keeps the returned `candidate_id` internal, and enables interview start only after a successful upload. A production API E2E run passed with a real PDF, a two-question interview, report/history persistence, and cross-user isolation.

The final browser click-through using the signed-in Google session remains a manual check because account credentials and browser sessions are not automated. The tester should upload a resume from the production page, review the preview, complete a short interview, and refresh the report/history views.

## Interview modes - Phase 1

The deployed API contract now supports `text` and `voice` interview modes. Requests that omit `mode` remain backward compatible and use `text`. The selected mode is preserved in SQLite state and in both the top-level and nested Firestore session documents.

After a resume is processed, the Text Interview page displays a mode selector. Text Interview continues through the existing production workflow. Speech Interview can be selected for product visibility, but its Start action is intentionally disabled and labeled for Phase 2.

No microphone capture, WebSocket voice session, speech-to-text, streaming Gemini response, text-to-speech, or separate speech service was introduced in this phase. Phase 2 will add the voice workspace UI and client-side interaction states without claiming a live speech pipeline.

## Rollback

The previous ready revision is `ai-interview-backend-00003-g6p`. Route traffic back with:

```bash
gcloud run services update-traffic ai-interview-backend \
  --project project-7dffc340-f73f-4e62-aec \
  --region us-central1 \
  --to-revisions ai-interview-backend-00003-g6p=100
```

After rollback, rerun `backend/scripts/smoke_test.py` and confirm that no Firestore data migration is needed.
