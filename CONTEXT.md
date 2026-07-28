# InterviewOS

InterviewOS turns a candidate's resume into a reviewed profile that can be used to create text or speech interview sessions.

## Language

**Resume**:
The candidate-provided PDF or DOCX document used as source material for profile extraction.
_Avoid_: CV file, profile document

**Upload Rejection**:
The outcome when a Resume cannot be accepted or does not contain enough readable content to create a Candidate Profile. An Upload Rejection never creates or replaces a Candidate Profile.
_Avoid_: Partial extraction, upload warning

**Partial Extraction**:
The outcome when an accepted Resume produces a persisted, editable Candidate Profile but some document content may not have been processed. Partial Extraction is a warning and does not permanently prevent Interview Readiness after review and correction.
_Avoid_: Upload rejection, successful extraction

**Upload Attempt**:
A single user-initiated effort to upload one selected Resume. Explicit retries of the same Resume continue the same Upload Attempt; selecting a different file begins a new one.
_Avoid_: Extraction attempt, automatic retry

**Replacement Upload**:
An Upload Attempt intended to replace an existing Candidate Profile. The existing profile remains authoritative until the replacement is extracted and persisted successfully as one atomic change.
_Avoid_: Profile edit, partial replacement

**Candidate Profile**:
The persisted, candidate-owned structured record produced from a Resume and then reviewed and corrected by the candidate. The latest successfully saved Candidate Profile is the source of truth for future interviews.
_Avoid_: Extracted profile, resume profile, client profile

**Profile Version**:
The monotonically increasing revision of a Candidate Profile. It identifies the exact committed profile used for correction conflict checks and an Interview Session Snapshot.
_Avoid_: Draft version, client version

**Profile Audit Event**:
An immutable record of a committed Candidate Profile change, including its Profile Version, time, and source.
_Avoid_: Activity log, ownership record

**Profile Correction**:
An explicitly supported change made by the candidate to editable Candidate Profile information and persisted before an interview can start.
_Avoid_: Client override, temporary edit

**Profile Review**:
The durable workspace where a candidate examines and corrects a Candidate Profile before using it to start an interview. It may be left and revisited; only successfully saved information is treated as part of the Candidate Profile.
_Avoid_: Profile preview, extraction preview

**Profile Validity**:
The condition in which Candidate Profile data has acceptable field types, shapes, values, and relationships and can therefore be saved. A valid Candidate Profile may still be incomplete and not ready for an interview.
_Avoid_: Interview readiness, complete profile

**Interview Readiness**:
The condition in which the latest saved Candidate Profile contains the minimum identity, skill, and evidence required to create an Interview Session. Interview Readiness is determined authoritatively by the backend.
_Avoid_: Profile validity, extraction success

**Readiness Issue**:
A structured reason that the latest saved Candidate Profile is not interview-ready. Readiness Issues identify every missing or invalid requirement that must be resolved before an interview can start.
_Avoid_: Validation error, generic profile error

**Skill Evidence**:
Candidate Profile information that connects a skill to supporting resume text. Each item has a stable identity; its skill and text may be corrected, while its source metadata remains bound to that identity and immutable.
_Avoid_: Skill proof, generated evidence

**Legacy Education**:
Unstructured education text retained from an existing Candidate Profile. It remains readable until the candidate explicitly replaces it with structured education entries.
_Avoid_: Parsed education, inferred education

**Extraction Warning Acknowledgement**:
The record that a candidate successfully saved a Profile Review after Partial Extraction. It changes warning prominence without erasing the original extraction warning.
_Avoid_: Warning deletion, extraction correction

**Interview Session**:
A text or speech interview created for a candidate from a saved Candidate Profile and an interview configuration.
_Avoid_: Interview run, practice run

**Interview Session Snapshot**:
The immutable copy of the saved Candidate Profile stored when an Interview Session starts. Later Profile Corrections do not alter this snapshot or reports derived from it.
_Avoid_: Live profile, profile reference
