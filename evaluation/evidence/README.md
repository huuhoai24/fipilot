# FiPilot Evaluation Evidence

## Purpose

This directory packages available evaluation evidence used for the FiPilot
Capstone presentation. It was prepared from a repository audit at Git revision
`51fc3b57b2fc98e03023b4ccd90c249f300d9f3b`.

All four metric groups in this package are **reconstructed aggregate summary
from previously recorded evaluation results**. They record the aggregate
values supplied by the project owner on 2026-08-15. They are not reconstructed
sample data, raw experiment logs, or independently reproduced results.

Repository discovery result:

- `FOUND_RAW_DATA = YES` (unlabeled Resume corpus added after the initial audit)
- `FOUND_ELIGIBLE_LABELED_RAW_EVALUATION_DATA = NO`
- `FOUND_EVAL_SCRIPT = YES`
- `FOUND_SAMPLE_RESULTS = NO`
- `FOUND_ONLY_AGGREGATE_RESULTS = YES`

An unlabeled Resume corpus was added after the initial audit. It is valid raw
inventory evidence, but it is not labelled evaluation data and therefore does
not change the four benchmark evidence classifications above.

## Evidence Levels

### Verified raw evidence

Original dataset and predictions or results are available and can be traced to
the reported metric.

### Reproduced evidence

The metric has been rerun from an existing dataset using an identified
evaluation script.

### Historical aggregate

Only previously recorded aggregate results remain available. Historical
aggregate files MUST NOT be interpreted as recreated raw experiment logs.

This package contains only Historical aggregate evidence. It contains no
sample-level result files.

## Metrics

Resume Extraction:

- 235 CVs
- Precision 90.88%
- Recall 85.67%

Speech-to-Text:

- 200 WAV samples
- WER 5.93%
- CER 4.33%

Question Generation:

- Relevance 99.33%
- CV Alignment 100%

Answer Evaluation:

- MAE 0.7/10
- Consistency 97.34%

## Resume Extraction

- Source files found: the project-owner task brief contains the packaged
  aggregate values. The repository contains an empty evaluation manifest, a
  `no_data` report, and unrelated or unlabelled Resume artifacts, but no
  235-case labelled benchmark.
- Evaluation script found: yes. The current framework implements normalized
  exact-match skill precision and recall in
  `backend/services/system_evaluation/`.
- Sample outputs found: no qualifying labelled expected-skill/prediction pairs
  or TP/FP/FN records.
- Reproducible now: no. The required labelled dataset is absent.
- Known limitations: the inspected slide 22 of
  `FiPilot_Capstone_Presentation (1).pptx.pptx` records 49.88% precision and
  51.37% recall, not 90.88% and 85.67%. No primary artifact resolves this
  discrepancy. The package preserves the values explicitly supplied for this
  task and does not claim that either pair was reproduced.

### Unlabeled Resume corpus inventory

The local `resumes/` directory was scanned without sending documents to an
external model and without writing filenames or document text to the evidence
package. Aggregate inventory results are recorded in
`unlabeled_resume_inventory_summary.json`:

- 2,604 PDF files across five supplied categories
- 2,311 unique SHA-256 content hashes (88.75%)
- 293 duplicate files beyond the first copy (11.25%)
- 2,602 files with a standard `%PDF-` header (99.92%)
- 2,604 files opened by PyMuPDF without an exception (100%)
- 2,491 files with extractable text (95.66%)
- 113 files without extractable text (4.34%)
- 7,569 pages in total; 2.91 pages per PDF on average
- all 2,604 files are at or below the application's 10 MB size limit

These are corpus quality and processing-readiness statistics. They are not
skill-extraction Precision, Recall, accuracy, or human-labelled benchmark
results.

## Speech-to-Text

- Source files found: slide 22 contains the same 200 WAV, 5.93% WER, and 4.33%
  CER aggregates, but no linked dataset or per-sample output.
- Evaluation script found: yes. The current framework implements NFKC- and
  casefold-normalized edit-distance WER and whitespace-excluded CER.
- Sample outputs found: no qualifying 200-sample WAV/reference/prediction set.
- Reproducible now: no. The four-case code-switch recipe is also missing all
  four required WAV fixtures and is not the claimed 200-sample evaluation.
- Known limitations: local speech traces are ad-hoc diagnostics, not the
  claimed benchmark, and are excluded from this package.

## Question Generation

- Source files found: the project-owner task brief and slide 22 contain the
  aggregate values only.
- Evaluation script found: yes. The current framework has a benchmark-only
  Gemini question-quality judge, but no evidence links that judge to the
  historical 99.33% and 100% results.
- Sample outputs found: no qualifying questions, judgments, or result rows.
- Reproducible now: no. Dataset size and historical judge type remain unknown.
- Known limitations: the current framework methodology must not be presented as
  the recovered methodology for these historical aggregates.

## Answer Evaluation

- Source files found: the project-owner task brief and slide 22 contain the
  aggregate values only.
- Evaluation script found: yes. The current framework supports repeated model
  scoring, MAE against a human label, and a consistency calculation, but no
  evidence links it to the historical result.
- Sample outputs found: no qualifying human/model score pairs or rater records.
- Reproducible now: no. Benchmark size, rater count, repeat count, and the
  historical consistency definition remain unknown.
- Known limitations: MAE and consistency should not be presented as fully
  reproducible human-benchmark evidence until sample-level methodology is
  recovered.

## Repository Sources Consulted

- `backend/evaluation_dataset.example.json`
- `backend/evaluation_report.json`
- `backend/evaluation_report.md`
- `backend/scripts/run_system_evaluation.py`
- `backend/scripts/benchmark_stt_codeswitch.py`
- `backend/services/system_evaluation/`
- `backend/app/tests/test_system_evaluation.py`
- `docs/SYSTEM_EVALUATION.md`
- `docs/presentation/EVALUATION_EVIDENCE_AUDIT.md`
- `FiPilot_Capstone_Presentation (1).pptx.pptx`, slide 22 (read-only inspection)

The checked-in manifest has zero cases, the checked-in report has
`status: "no_data"`, and the safe empty-manifest rerun under
`.scratch/evaluation-evidence-pass-20260814/` also produced `no_data`. Unit-test
fixtures use fake components and synthetic constants and therefore are
methodology tests rather than product performance evidence.
