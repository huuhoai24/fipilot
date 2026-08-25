# M0 Evaluation Audit

## Executive finding

FiPilot has a real evaluation framework, deterministic metric tests, historical
aggregate claims, an unlabelled Resume corpus inventory, and a preserved
synthetic RAGAS-style pilot. It does **not** have a populated, approved,
human-labelled dataset that can reproduce production CV, retrieval, question,
answer, report, STT, or TTS accuracy.

No new accuracy, benchmark, label, model output, or aggregate was generated in
M0.

## Artifact inventory

| Artifact | What exists | Classification |
| --- | --- | --- |
| `backend/services/system_evaluation/` | Dataset loader, metrics, benchmarks, judge, runner, reporting | IMPLEMENTED methodology |
| `backend/evaluation_dataset.example.json` | Six empty case arrays | REPRODUCIBLE `no_data`, not an evaluation result |
| `backend/evaluation_report.md` and deleted-at-audit tracked JSON in `HEAD` | Zero samples, all quality metrics null | REPRODUCED/HISTORICAL `no_data` behavior only |
| `evaluation/evidence/*.json` | Resume, STT, question, answer aggregate summaries | HISTORICAL ONLY |
| `evaluation/evidence/unlabeled_resume_inventory_summary.json` | Aggregate inventory of 2,604 PDFs | VERIFIED inventory; NOT a model benchmark |
| `evaluation/ragas_pilot/` | Synthetic cases, raw JSONL outputs/calls, summaries, run manifest | Historical preserved synthetic smoke run |
| `backend/scripts/benchmark_stt_codeswitch.py` | Four-case recipe | NOT REPRODUCIBLE; required WAV fixtures absent |
| `backend/app/tests/test_system_evaluation.py` | Fake/synthetic unit cases | Deterministic methodology tests |
| `evaluation/ragas_pilot/tests/` | Metric/dataset/reconciliation tests | Deterministic methodology tests |
| `backend/interview_app.db` | 81 operational sessions and 45 nonempty report payloads at audit time | Operational history; NOT labelled evaluation data |
| `backend/ai_lab/**/output.example.json` | Examples for lab CLI contracts | Examples, not benchmark outputs |

Operational Resume, answer, transcript, or report data was not repurposed as
ground truth.

## Metric implementations

### CV extraction

- Ground truth shape: expected skill labels plus explicitly selected profile
  fields per case.
- Skill metric: NFKC + casefold exact normalized set matching, micro-aggregated
  precision/recall/F1.
- Profile fields: exact normalized strings/collections; numeric tolerance 0.25.
- Latency: document extraction time plus model extraction time.
- Current populated dataset: none.

### STT

- Input contract: mono, uncompressed PCM16 WAV at 16 kHz plus UTF-8 reference.
- WER/CER: edit distance after NFKC/casefold; CER removes whitespace.
- Category breakdown: `vi`, `en`, `mixed_technical`.
- Current populated labelled dataset: none.

### TTS

- First-audio latency, generation duration, and generation/audio duration ratio.
- No intelligibility, naturalness, MOS, pronunciation, or human listening metric.
- Current populated dataset: none.

### Question generation

- Benchmark-only Gemini judge scores relevance, difficulty alignment, and CV
  alignment from 0 to 1.
- The framework judge uses the complex route at temperature 0.
- Current populated framework dataset: none.
- The separate 10-case synthetic pilot judged role relevance, CV alignment,
  technical validity, RAG grounding, difficulty, clarity, and unsupported
  candidate claims.

### Answer evaluation

- Framework repeats scoring (default three times).
- Consistency is `1 - mean_absolute_deviation / 10`, clipped to [0,1].
- Human MAE compares mean model score to a provided 0–10 human score.
- No human-labelled cases are present.
- The synthetic pilot preserved 40 outputs and judge results, but its proposed
  weak→strong answer ladder was declared invalid; controlled monotonicity is
  explicitly NOT EVALUATED.

### Retrieval

- The main system framework has no retrieval benchmark section.
- The RAGAS-style pilot uses synthetic expected catalog topic IDs, local
  top-8 retrieval, controlled HitRate/Recall/MRR@8, latency, empty rate, and an
  LLM-judged reference-free context precision.
- Reference-based context recall/precision from human-approved chunks is not
  available.
- Vector-adapter retrieval has no quality result.

### Report

No report-specific dataset, human rubric, factuality metric, score consistency
check, or judge script is wired. **NOT EVALUATED**.

## Preserved historical results

These numbers are recorded because they exist, not endorsed as verified:

| Component | Recorded aggregate | Evidence status |
| --- | --- | --- |
| Resume skill extraction | 235 CVs; precision 90.88%; recall 85.67% | HISTORICAL ONLY; conflicts with presentation 49.88%/51.37% |
| STT | 200 WAV; WER 5.93%; CER 4.33% | HISTORICAL ONLY |
| Question generation | relevance 99.33%; CV alignment 100% | HISTORICAL ONLY; dataset/judge unknown |
| Answer evaluation | MAE 0.7/10; consistency 97.34% | HISTORICAL ONLY; samples/raters/definition linkage absent |

No raw sample records, labels, predictions, TP/FP/FN rows, human ratings, or
historical judge configuration supporting those aggregates were found.

## Synthetic RAGAS-style pilot

The preserved run targets commit `1249cc50a6995ac0a72465fdfb2d708d2cde5c1c`
and used 10 synthetic controlled profile groups. `model_calls.jsonl` and
component sample JSONL files preserve raw inputs/outputs and judge records.

Valid claims from that artifact are limited to that run:

- local lexical retrieval executed successfully on the synthetic cases;
- deterministic controlled topic-ID arithmetic and latency were recorded;
- question/answer rubric results are LLM-as-judge on synthetic cases;
- answer repeatability arithmetic exists;
- no real user Resume text or human ground truth was used;
- official `ragas` was not installed and no official Ragas metric was used;
- controlled answer monotonicity was invalid and is not a production result.

The artifact is preserved and internally auditable, but it is historical with
respect to the current dirty tree and does not validate the optional Firestore
vector path.

## Accuracy status table

| Component | Ground Truth | Existing Metric | Reproducible | Accuracy Status |
| --- | --- | --- | --- | --- |
| CV Parsing | No populated labelled Resume/profile set | Skill P/R/F1; selected field accuracy; latency | Framework yes, claimed results no | **HISTORICAL ONLY** |
| Retrieval | Synthetic catalog-derived expected IDs only; no human reference chunks | Hit/Recall/MRR@8, reference-free context precision, latency | Synthetic local pilot artifacts only | **NOT EVALUATED** for production accuracy |
| Question Generation | No human-labelled production set | LLM-judge relevance/difficulty/CV alignment; pilot rubrics | Synthetic pilot artifacts only | **HISTORICAL ONLY** |
| Answer Evaluation | No verified human scores | Consistency/MAD, MAE framework; synthetic judge rubrics | Methodology yes, human metrics no | **NOT EVALUATED** |
| Final Report | None | None | No | **NOT EVALUATED** |
| STT | No available 200-WAV references | WER/CER/latency | Claimed result no | **HISTORICAL ONLY** |
| TTS | None | Latency/ratio only | No populated dataset | **NOT EVALUATED** |

`VERIFIED` is not assigned to any model-quality component. The unlabelled
Resume inventory is verified only as file/hash/text-layer inventory.

## Reproducibility blockers

- No approved populated evaluation manifest.
- No sample-level source for historical aggregate claims.
- No frozen model/prompt/config versions attached to those claims.
- Gemini and speech artifacts can change independently of source commit.
- The current working tree differs from both the historical aggregate audit
  commit and the synthetic pilot commit.
- Firestore vector collection contents/index deployment are external and were
  not captured in a checked-in manifest.

## Evaluation-only prompts/models

The system question-quality judge is in
`backend/services/system_evaluation/judges.py`. The pilot judge and versioned
rubrics are in `evaluation/ragas_pilot/judges.py`. Both are separate from
production routes. There is no production LLM-as-judge call.
