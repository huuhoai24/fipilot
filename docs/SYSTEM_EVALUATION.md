# AI Evaluation Framework

The framework in `backend/services/system_evaluation` benchmarks existing
production interfaces without changing interview behavior or exposing a public
API. It produces aggregate-only `evaluation_report.json` and
`evaluation_report.md` files.

## Dataset

Copy `backend/evaluation_dataset.example.json` to a private benchmark workspace.
Do not commit candidate Resume files, audio, reference transcripts, candidate
answers, or production prompts. Paths in the manifest are resolved relative to
the manifest file.

- `cv_cases`: `resume_path`, expected skills, and selected expected profile fields.
- `stt_cases`: mono PCM16 16 kHz WAV, a UTF-8 reference text file, and category
  `vi`, `en`, or `mixed_technical`.
- `tts_cases`: benchmark text used only as synthesis input.
- `question_cases`: synthetic Candidate Profile, round, and interview config.
- `evaluator_cases`: synthetic labelled answer plus a human score from 0 to 10.
- `voice_turns`: content-free successful/failed turn observations and total latency.

Use at least 30 representative samples per language/domain slice for a useful
p95 and failure rate. Human labels should be reviewed by more than one evaluator.

## Run

From `backend/`, with ADC and the speech dependencies configured:

```powershell
python scripts/run_system_evaluation.py `
  --dataset C:\private-benchmark\evaluation_dataset.json `
  --output-dir . `
  --evaluator-repetitions 3
```

The command uses the configured Resume Gemini model, faster-whisper, VieNeu-TTS,
Question Generator, Evaluator, and a benchmark-only Gemini question judge.
Models remain lazy and tests use mocks, so test execution does not download them.

## Metric Definitions

- Skill precision/recall/F1 use normalized exact skill labels across all CV cases.
- Profile field accuracy compares only ground-truth fields supplied by each case.
- WER and CER use NFKC, case-folded text; CER excludes whitespace.
- TTS audio duration ratio is generation wall time divided by emitted PCM duration.
- Evaluator consistency is `1 - mean absolute deviation / 10`, clipped to `[0, 1]`.
- Evaluator MAE compares the mean repeated model score with the human label.
- Voice p50/p95 use successful turns; failed or missing-latency turns contribute
  to failure rate.

The runner catches failures per sample and records counts only. It never writes
audio, transcript text, Resume content, candidate answers, prompts, or tokens to
reports or logs.
