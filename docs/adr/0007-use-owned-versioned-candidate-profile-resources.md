# Use owned, versioned Candidate Profile resources

The repositories allow one authenticated user to own multiple Candidate Profiles, so a Replacement Upload targets `POST /api/v2/candidates/{candidate_id}/resume` and verifies route ownership rather than selecting an implicit current profile or accepting ownership in the body. Candidate Profiles expose a monotonically increasing `profile_version`; profile corrections and replacements require a strong `If-Match` version, atomically compare and increment it, and return a structured stale-version conflict instead of overwriting a newer profile.

Interview start atomically reads the latest committed owned profile and records both its immutable snapshot and exact `profile_version` in the new Interview Session before later profile mutations can intervene. A pending or failed replacement retains the existing profile and version.
