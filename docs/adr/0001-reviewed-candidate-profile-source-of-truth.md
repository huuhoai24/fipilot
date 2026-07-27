# Use the reviewed Candidate Profile as the source of truth

Resume upload persists the initial Candidate Profile, and authenticated, ownership-checked profile corrections update only explicitly editable fields on that persisted record. Interview start reloads the latest successfully saved Candidate Profile and stores an immutable snapshot in the new Interview Session, so later corrections cannot change existing sessions or reports. Interview start remains separate from saving corrections and is available only when the profile is valid, has no unsaved corrections, and the latest save succeeded.

This requires a small profile-update API contract because client-only corrections would not affect the existing interview-start contract.
