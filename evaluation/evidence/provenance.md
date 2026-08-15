# FiPilot Evaluation Evidence Provenance

The values in this package are a **reconstructed aggregate summary from
previously recorded evaluation results** supplied in the project-owner task
brief dated 2026-08-15. No sample-level results, human annotations, reference
transcripts, predictions, or TP/FP/FN records were created during packaging.

| Module | Aggregate Result | Raw Dataset | Sample Output | Script | Status |
| --- | --- | --- | --- | --- | --- |
| Resume Extraction | 235 CVs; precision 90.88%; recall 85.67% | Not found | Not found | Current framework found; historical linkage not established | Historical Aggregate |
| Speech-to-Text | 200 WAV; WER 5.93%; CER 4.33% | Not found | Not found | Current framework found; historical linkage not established | Historical Aggregate |
| Question Generation | relevance 99.33%; CV alignment 100% | Not found; size unknown | Not found | Current framework and judge found; historical linkage not established | Historical Aggregate |
| Answer Evaluation | MAE 0.7/10; consistency 97.34% | Not found; size unknown | Not found | Current framework found; historical linkage not established | Historical Aggregate |

## Supplemental Unlabeled Corpus Evidence

| Evidence | Raw Input | Labels | Measurement | Status |
| --- | --- | --- | --- | --- |
| Resume corpus inventory | 2,604 local PDFs under `resumes/` | None | File/header/hash/size counts and local PDF text-layer inspection | Verified Raw Inventory, not a model benchmark |

The corpus inventory is reproducible from the local files and is recorded in
`unlabeled_resume_inventory_summary.json`. It does not support Precision,
Recall, accuracy, or any comparison against human ground truth.

## Primary Repository Evidence

| Source | Finding | Evidentiary Use |
| --- | --- | --- |
| `backend/evaluation_dataset.example.json` | All six evaluation case arrays are empty. | Proves that the available public manifest cannot reproduce any metric. |
| `backend/evaluation_report.json` and `.md` | `status` is `no_data`; every sample count is zero and requested metrics are null/N/A. | Records the actual checked-in framework result. |
| `.scratch/evaluation-evidence-pass-20260814/evaluation_report.json` and `.md` | A safe empty-manifest rerun also returned `no_data`. | Confirms runner behavior only; not empirical performance evidence. |
| `backend/scripts/run_system_evaluation.py` | Real evaluation runner wiring the current application components. | Establishes that evaluation code exists. |
| `backend/services/system_evaluation/` | Dataset loaders, metric definitions, evaluators, runner, schemas, and reporting. | Establishes current methodology, not provenance of historical aggregates. |
| `backend/scripts/benchmark_stt_codeswitch.py` | Four-case recipe whose required WAV fixtures are absent; its score is not the framework WER/CER metric. | Incomplete recipe, not evidence for the 200-WAV aggregate. |
| `backend/app/tests/test_system_evaluation.py` | Uses fake components, private sentinels, and synthetic numeric constants. | Unit/methodology evidence only; excluded from product metrics. |
| `FiPilot_Capstone_Presentation (1).pptx.pptx`, slide 22 | Contains aggregate-only claims. Resume values are 49.88%/51.37%, while the other requested aggregate values match. | Secondary claim record only; no raw or sample evidence. |

## Resume Metric Discrepancy

The project-owner task brief specifies 90.88% skill precision and 85.67% skill
recall. Read-only inspection of the presentation in this workspace found
49.88% and 51.37% on slide 22. Repository and available Git-history searches
found no primary result artifact for either pair. This package preserves the
explicitly requested historical values, records the conflict, and does not
resolve it by modifying either result.

## Reproduction Decision

No real evaluation was rerun because the approved labelled inputs are absent.
Running the empty manifest would only reproduce `no_data`; running paid model
calls without ground truth would not establish any requested quality metric.
No `reproduced/` directory or sample-level JSONL file was therefore created.

## Provenance Boundaries

- Operational application data is not an independently labelled benchmark.
- Local speech traces and isolated WAV files are diagnostics, not the claimed
  200-sample STT dataset.
- Historical Resume/layout-model artifacts are incomplete, unlabelled for the
  active skill extraction contract, or tied to an obsolete task.
- A current metric implementation does not prove that a historical aggregate
  was calculated with that implementation.
- Historical Aggregate does not mean Verified Benchmark.
