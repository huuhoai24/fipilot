# InterviewOS

InterviewOS turns a candidate's resume into a reviewed profile that can be used to create text or speech interview sessions.

## Language

**Resume**:
The candidate-provided PDF or DOCX document used as source material for profile extraction.
_Avoid_: CV file, profile document

**Candidate Profile**:
The persisted, candidate-owned structured record produced from a Resume and then reviewed and corrected by the candidate. The latest successfully saved Candidate Profile is the source of truth for future interviews.
_Avoid_: Extracted profile, resume profile, client profile

**Profile Correction**:
An explicitly supported change made by the candidate to editable Candidate Profile information and persisted before an interview can start.
_Avoid_: Client override, temporary edit

**Interview Session**:
A text or speech interview created for a candidate from a saved Candidate Profile and an interview configuration.
_Avoid_: Interview run, practice run

**Interview Session Snapshot**:
The immutable copy of the saved Candidate Profile stored when an Interview Session starts. Later Profile Corrections do not alter this snapshot or reports derived from it.
_Avoid_: Live profile, profile reference
