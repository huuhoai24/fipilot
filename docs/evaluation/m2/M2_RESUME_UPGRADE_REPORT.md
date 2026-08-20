# M2 Resume Processing Upgrade Report

Status: **CLOSED**

M2 changed only Resume document validation, native/OCR text recovery, bounded section-aware context construction, source verification/provenance, upload extraction status, and the evaluation harness. Retrieval, question generation, answer evaluation, reports, orchestration, and model selection were not changed.

## Acceptance results

| Metric | M1 | M2 |
|---|---:|---:|
| Experience F1 | 0.7213 | 1.0000 |
| Skills F1 | 0.9740 | 0.9772 |
| Micro F1 | 0.9478 | 0.9853 |
| Boundary recall after old cutoff | 0.0000 | 1.0000 |
| OCR success | not evaluated | 1.0000 |

## Document processing

PDF/DOCX acceptance now checks extension, declared MIME when available, magic bytes, DOCX container members, and parser validity. Internal extraction records expose source type, page count, character count, per-page method, tables, warnings, and explicit `complete`/`partial`/`failed` state. Image-only or sparse PDF pages deterministically trigger local RapidOCR; OCR failures are bounded and surfaced as safe warnings or structured rejection.

## Context and provenance

The former silent first-12,000-character slice is removed. English and Vietnamese headings are recognized, Experience receives the largest bounded allocation, and oversized sections preserve both head and tail with `content_omitted`. Verification emits `supported`, `normalized_match`, `unsupported`, or `uncertain`; uncertain facts are retained for review.

## Cost and reproducibility

The fixed model is `gemini-2.5-flash-lite` at temperature `0.1`. Provider usage is `partial_or_unavailable`: 54 of 55 paid attempts reported tokens. Exact total cost is therefore unavailable; the provider-reported known subtotal is $0.019958, and the conservative total estimate is $0.021275. Raw validated responses are cached by file/text/prompt/model/temperature/schema hashes and deterministic post-processing can be recomputed offline. Run ID: `m2-20260818-resume-upgrade`.

## Robustness scope and limitations

The fixed comparison contains the unchanged 30 M1 PDF/DOCX fixtures, including single-column, two-column, table, unusual-order, and old-cutoff layouts. Added robustness evidence contains 6 image-only PDFs, 6 long DOCX resumes (2 each with a marker before/near/after the old cutoff), and 4 invalid or mismatched files. All labels are synthetic controlled; OCR evidence is English and does not establish performance on noisy photos, handwriting, or production CV distributions. One timed-out Vertex attempt did not return usage metadata, so only a known subtotal and conservative estimate are reported—not an invented exact total.
