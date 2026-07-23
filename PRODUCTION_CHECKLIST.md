# Production E2E checklist

Record the tester, timestamp, frontend URL, backend revision, and anonymized test user IDs. Never paste tokens, full email addresses, resume content, interview answers, or model prompts into this file.

## User workflow

- [ ] Google Sign-In opens the configured provider and returns to the production frontend.
- [ ] Authentication is restored after a full browser refresh.
- [ ] A supported resume file uploads successfully.
- [ ] The upload creates a user-owned `CandidateProfile` with expected non-sensitive fields.
- [ ] An interview starts from the uploaded candidate.
- [ ] A candidate answer can be submitted.
- [ ] A weak or incomplete answer produces an adaptive follow-up where expected.
- [ ] The configured interview reaches completion.
- [ ] Final report generation succeeds once and remains idempotent on retry.
- [ ] The report remains available after browser refresh.
- [ ] Interview history lists the completed session newest first.
- [ ] Logout clears the application session and protected views are no longer accessible.
- [ ] An expired Firebase token is refreshed by the frontend and the request succeeds once retried.

## Ownership and security

- [ ] User A cannot read or start an interview with user B's candidate ID.
- [ ] User A cannot read, answer, or report on user B's session ID.
- [ ] User A cannot read user B's final report.
- [ ] Firestore data appears only under `users/{uid}/candidates` and `users/{uid}/interviews`.
- [ ] Public `/health` and `/ready` return 200; `/api/v2/auth/me` without a token returns 401.
- [ ] Firebase Authorized Domains contains the production Hosting domain and approved custom domains only.

## Observability and privacy

- [ ] The response `X-Request-ID` can be found in Cloud Logging.
- [ ] Interview route logs include status, duration, and session ID where applicable.
- [ ] Logs contain no Firebase token, authorization header, full email, CV body, answer, prompt, or raw Gemini response.

## Cloud dependencies

- [ ] A Firestore write made through Cloud Run can be read after a separate request or refresh.
- [ ] A real interview operation confirms Vertex Gemini generation through the Cloud Run service account and ADC.
- [ ] Browser requests from the production origin have no CORS errors.

## Rollback

- [ ] Identify the last known-good revision: `gcloud run revisions list --service SERVICE --region REGION`.
- [ ] Route all traffic back: `gcloud run services update-traffic SERVICE --region REGION --to-revisions REVISION=100`.
- [ ] Re-run `backend/scripts/smoke_test.py` against `/health`, `/ready`, and authenticated `/api/v2/auth/me`.
- [ ] Confirm no Firestore schema rollback or data migration is required before declaring recovery complete.
