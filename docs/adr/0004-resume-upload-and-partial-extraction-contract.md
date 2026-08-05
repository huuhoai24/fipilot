# Define Resume upload rejection and Partial Extraction separately

Resume upload accepts exactly one genuine PDF or DOCX up to 10 MB and requires at least 50 normalized meaningful text characters without OCR or a page-count limit. The document's primary purpose must be presenting one person's qualifications for employment. Project and capstone reports, theses, research papers, product documentation, job descriptions, certificates, and team portfolios are rejected even when they contain names, technologies, projects, or role descriptions. Unsupported, oversized, empty, encrypted, malformed, image-only, insufficient-text, or non-resume documents return structured rejection codes and never create or replace a Candidate Profile.

The system must not silently represent truncated processing as complete. Until complete-document extraction is available, incomplete processing returns a structured `partial_extraction` warning and may persist an editable Candidate Profile; the warning does not block interview start once the latest saved profile satisfies the shared backend Interview Readiness validator.

Rejected uploads use `unsupported_file_type`, `file_too_large`, `empty_file`, `encrypted_document`, `invalid_document`, `no_extractable_text`, `insufficient_text`, or `not_a_resume`. Format validation uses the actual document content rather than trusting its extension. Semantic classification treats document content as untrusted data and completes before any Candidate Profile mutation. The 50-character threshold is calculated after normalization and removal of meaningless whitespace.

Multipart cardinality is a request-contract concern rather than a document rejection: more than one file returns `multiple_files_not_allowed` before extraction or profile mutation.
