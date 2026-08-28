# AI Evaluation Framework

The framework in `backend/services/system_evaluation` benchmarks existing
production interfaces without changing interview behavior or exposing a public
API. It validates and skips individual bad samples, then produces an
aggregate-only validation file and JSON/Markdown evaluation reports.

## Dataset

The primary directory layout is documented in
`backend/evaluation_dataset/README.md`:

- CV: paired PDF/DOCX Resume files and ground-truth JSON.
- STT: WAV audio and `metadata.csv` reference transcripts.
- TTS: non-sensitive synthesis cases.
- LLM: synthetic profiles, expected topics and levels, and generated questions.
- Evaluator: synthetic answers with human-reviewed scores and feedback labels.
- Voice: content-free timestamps for successful and failed turns.

The previous single-manifest format remains supported for private benchmarks.
Paths in a legacy manifest are resolved relative to that file.

## Run

From the repository root, with ADC and speech dependencies configured:

```powershell
python backend/scripts/run_system_evaluation.py `
  --dataset backend/evaluation_dataset `
  --output-dir backend/evaluation_results `
  --evaluator-repetitions 3
```

The CLI loads `backend/.env` without overriding non-empty process environment
variables. To run only selected benchmark sections, pass one or more of `cv`,
`stt`, `tts`, `question`, `evaluator`, or `voice`:

```powershell
python backend/scripts/run_system_evaluation.py `
  --dataset backend/evaluation_dataset `
  --output-dir backend/evaluation_results/cloud_targeted `
  --sections cv question evaluator
```

The command uses the configured Resume Gemini model, faster-whisper, VieNeu-TTS,
Question Generator, Evaluator, and the benchmark-only Gemini question judge.
The production runner regenerates questions even when curated questions are
present in the dataset, then judges the generated output. Models remain lazy
and tests use fakes, so test execution does not download them.

Outputs:

- `dataset_validation.json`
- `evaluation_report.json`
- `evaluation_report.md`

## Metric definitions

- Skill precision/recall/F1 use normalized exact skill labels across valid CV
  cases. Profile field accuracy compares only supplied role, experience,
  project, and education annotations.
- CV metrics are calculated once and aggregated overall and separately for PDF
  and DOCX. Document parsing failures are also grouped by format.
- WER and CER use NFKC, case-folded text; CER excludes whitespace. The loader
  categorizes Vietnamese, English, and mixed technical samples and resamples
  supported mono PCM16 WAV input to 16 kHz.
- TTS real time factor is generation wall time divided by emitted PCM duration.
  RTF below 1 means faster than realtime. Subjective MOS is not inferred.
- Evaluator consistency is `1 - mean absolute deviation / 10`, clipped to
  `[0, 1]`. Evaluator MAE compares the mean repeated model score with the human
  label.
- Voice p50/p95 use successful turns; failed or incomplete turns contribute to
  failure rate. Total latency runs from speech end to first TTS audio.

The runner catches model failures per sample and records counts only. Generated
artifacts never include filenames, candidate names, emails, Resume content,
transcript text, audio, candidate answers, prompts, or tokens.
