# Standardize Resume Review API responses

Profile reads and saves return the canonical Candidate Profile, backend readiness, warnings, and read-only metadata; upload success retains the existing top-level `candidate_id`, `profile`, and `confidence_score` fields while adding readiness, warnings, metadata, and an upload-operation descriptor. All new failures use one structured error object with stable `code`, user-safe `message`, `retryable`, and structured `issues`, with standard status mappings for validation, readiness, preconditions, idempotency conflicts, processing, document rejection, authentication, ownership, and transient failure.

Partial Extraction is represented only as a warning on a successful response. Processing is represented by a non-error `202` upload-operation response, and the authenticated upload-status resource returns the current operation state plus a terminal result or error.
