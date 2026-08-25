# M0 CV / Resume Processing Audit

## Actual pipeline

```text
multipart UploadFile
  -> trust filename extension (`pdf` or `docx`)
  -> copy entire file to temporary disk file
  -> reject if file size > 10 MiB
  -> SHA-256 file content
  -> pypdf page text OR python-docx paragraph/table text
  -> reject if stripped text < 50 characters
  -> in-memory/persistent extraction-artifact lookup
  -> JSON-encode only the first 12,000 characters
  -> Vertex Gemini Resume classification + extraction
  -> Pydantic ResumeExtractionResult
  -> document type/confidence gate
  -> CandidateProfile conversion/caps
  -> create Candidate + save Resume text + save profile
```

Sources: `gateway/api/resume.py:39-178`,
`infrastructure/documents/pdf_service.py:8-43`,
`services/profile_scanner/agent.py:13-34`, and
`services/profile_scanner/schemas.py:15-81`.

## Format support and parsing

| Question | Evidence-backed answer |
| --- | --- |
| PDF supported? | Yes, when filename suffix is `.pdf` |
| DOCX supported? | Yes, when filename suffix is `.docx` |
| Parser | PDF: `pypdf.PdfReader`; DOCX: `python-docx` |
| Actual-type/MIME/magic validation | **NOT IMPLEMENTED**; extension is trusted |
| Multiple multipart files | FastAPI declares one `file` parameter, but explicit request-wide file cardinality detection and `multiple_files_not_allowed` are **NOT IMPLEMENTED** |
| Encrypted/malformed distinction | **NOT IMPLEMENTED** as structured rejection codes; underlying parser errors can escape |
| PDF text extraction | Iterate pages, call `page.extract_text()`, append nonempty text with newline |
| DOCX text extraction | Nonblank paragraphs followed by table rows; nonblank cell text is joined with ` | `; duplicate cell strings within a row are removed |
| PDF table extraction | No specialized table parser; only whatever pypdf emits as page text |
| DOCX table extraction | Yes, cell text only; merged/layout semantics are not preserved |
| Images | **NOT PROCESSED** |
| Portrait/logo/decorative filtering | **NOT IMPLEMENTED** because images are ignored entirely |
| OCR | **NOT IMPLEMENTED** |

An image-only/scanned PDF normally produces no or insufficient text and returns
HTTP 422 `"Could not extract enough resume text."`. There is no OCR attempt,
image extraction, partial-success path, or specific `no_extractable_text` code.

## Preprocessing, chunking, and tokenization

- Parser output is stripped. No Unicode NFKC normalization is applied to the
  complete Resume text before the 50-character gate.
- There is no header/footer removal, dehyphenation, column reconstruction,
  layout analysis, language detection, or deterministic section detection.
- There is no Resume chunking.
- There is no tokenizer and no model token count.
- `build_resume_extraction_prompt` silently slices `resume_text[:12000]` by
  Python characters. This is neither token-aware nor a complete-document
  strategy.
- The full parsed text is persisted, but only the first 12,000 characters reach
  the extraction model.
- No `partial_extraction` warning records that omitted tail content.

The only section-like interpretation is performed probabilistically by Gemini.
`source_section` may be returned on skill evidence but is not validated against
an actual detected section.

## Model extraction

| Property | Value |
| --- | --- |
| Provider | Google Vertex AI Gemini via `google-genai` |
| Model | `gemini-2.5-flash-lite` |
| Location | `global` |
| Temperature | 0.1 |
| Thinking budget | 0 |
| Timeout | 60 seconds |
| Attempts | 1 |
| Prompt | `services/profile_scanner/prompts.py` |
| Output schema | `ResumeExtractionResult` |
| Classification threshold | `document_type == "resume"` and confidence ≥ 0.7 |

The prompt restricts accepted resumes to 10 technology domains, treats the
document as untrusted input, asks the model to ignore embedded instructions,
and asks it to extract only supported facts. Non-Resume categories include
portfolio, job description, academic/project report, research paper,
certificate, and other.

Caps applied in code:

- 30 skills;
- 8 skill-evidence entries;
- 6 projects;
- 6 experiences.

An evidence item survives conversion only when it is nonblank and its skill
matches an extracted skill after strip/casefold. This verifies internal
cross-reference consistency, not that the evidence or skill occurs in the
Resume source.

## Candidate Profile schema

The actual shared `CandidateProfile` contains:

- `candidate_id`
- `name`
- `years_experience`
- `recent_role`
- `skills`
- `skill_evidence`
- `projects`
- `experiences`
- `education` (legacy string, structured list, or null)
- `specialization`
- `seniority_signal`
- `confidence`
- `confidence_score`
- `extraction_method`

Nested fields:

- Project: `name`, `description`, `technologies`, `role`
- Experience: `company`, `title`, `start_date`, `end_date`, `description`,
  `technologies`
- Education: `institution`, `degree`, `field_of_study`, `start_date`, `end_date`
- Skill evidence: `skill`, `evidence: list[str]`, `source_section`

The Resume extraction boundary itself outputs name, years, recent role, skills,
evidence, projects, experiences, structured education, specialization, and
confidence. It does not issue `candidate_id`, `profile_version`, evidence IDs,
audit metadata, or provenance identities.

## Missing-field behavior

- Name defaults to the literal fallback `Candidate`.
- Lists default to empty.
- Years, role, specialization, and structured education details may be null.
- Confidence defaults to 0.
- Pydantic validates field shapes/ranges but accepted incomplete profiles can
  be persisted.
- `CandidateProfile` mirrors `confidence` and `confidence_score` for backwards
  compatibility.
- A later profile GET computes readiness issues, but upload success does not
  include readiness and interview start does not enforce it.

## Hallucination controls and residual risk

Implemented controls:

- Explicit “extract only supported facts” system/prompt instructions.
- Resume text is JSON-encoded and identified as untrusted data.
- Provider JSON schema and Pydantic validation.
- Supported-domain classification and 0.7 confidence threshold.
- Output caps and internal evidence-to-skill matching.

Not implemented:

- source-span offsets or quotes validated against parser output;
- deterministic field-to-source checks;
- confidence calibration against labels;
- a second-pass verifier;
- an “unknown” requirement for every absent scalar;
- post-model hallucination detection;
- complete-document processing.

Therefore hallucinated but schema-valid facts can be persisted. The prompt is a
guardrail, not a factual guarantee.

## Cache and persistence behavior

The file SHA-256 is used for extraction reuse, not upload idempotency. The
in-memory cache key includes authenticated user, content hash, and extraction
version `resume-extraction-v1`; TTL is one hour and capacity is 256. A matching
persistent artifact can also be reused. Neither mechanism prevents concurrent
duplicate Candidate creation or implements upload-operation states.

Persistence happens after extraction by sequential repository calls. There is
no documented atomic unit spanning candidate creation, raw Resume save,
profile save, and extraction artifact save.

## Evaluation status

- The framework can compute normalized exact-match skill precision/recall/F1,
  selected profile-field accuracy, failures, and processing latency.
- `backend/evaluation_dataset.example.json` has zero CV cases.
- The 2,604-file Resume corpus inventory is unlabelled. Its pypdf/PyMuPDF text
  extractability statistics do not evaluate this Gemini extraction pipeline.
- Claimed 235-CV aggregates have no sample labels or predictions and conflict
  across evidence (90.88/85.67 versus 49.88/51.37).

Accuracy status: **HISTORICAL ONLY / NOT REPRODUCIBLE**, not verified.
