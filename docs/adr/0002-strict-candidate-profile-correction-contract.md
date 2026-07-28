# Use a strict allowlisted Candidate Profile correction contract

The authenticated profile-update contract accepts only the existing editable CandidateProfile keys: `name`, `years_experience`, `recent_role`, `specialization`, `skills`, `skill_evidence`, `projects`, `experiences`, and `education`. It rejects aliases, unknown keys, read-only fields, candidate or ownership changes, validates and normalizes nested data, recomputes derived fields server-side, preserves immutable evidence source metadata, and records when evidence text was user-corrected.

Existing `skill_evidence` entries may echo their server-issued `evidence_id` only as an immutable correlation key; new entries omit it, and all source, provenance, version, ownership, and audit fields remain prohibited in the body. Conditional mutation uses `If-Match`, not a body field.

This feature does not rename CandidateProfile fields or introduce compatibility aliases. Any future naming change requires a separate ADR, data migration, and explicit compatibility or API-versioning strategy.
