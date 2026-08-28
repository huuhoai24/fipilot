# AI Interview Platform Evaluation Dataset

This directory contains offline benchmark inputs for the evaluation tooling in
`backend/services/system_evaluation`. The runner validates every sample before
loading it, skips invalid samples, and writes aggregate-only results. It never
repairs labels or generates replacement samples.

## Layout and formats

- `cv/resumes/`: PDF and DOCX Resume files. Each file is paired by stem with a
  JSON annotation under `cv/ground_truth/` or the existing
  `cv/ground-truth/` directory. An annotation must contain an ID, explicit
  skills, experience, projects, education, and an explicit or
  experience-derived role.
- `stt/audio/` and `stt/metadata.csv`: mono PCM16 WAV recordings and reference
  metadata. Required CSV columns are `filename` and `text`; `language` and
  `duration` are recommended. WAV inputs between 8 kHz and 48 kHz are
  resampled to 16 kHz for the production STT interface.
- `tts/cases.json`: non-sensitive synthesis text cases.
- `llm/interview_cases.json`: synthetic Candidate Profiles, expected topics and
  levels, and previously generated questions for the benchmark-only LLM judge.
- `evaluator/human_labels.json`: synthetic questions and answers with reviewed
  human scores and feedback categories.
- `voice/latency_samples.json`: content-free timing observations. Successful
  samples contain the five ordered timestamps; failed samples contain no
  transcript or audio content.

JSON case files use a top-level object with `synthetic`, `description`, and a
`cases` array. Every case needs a unique `case_id`. Existing annotations are
authoritative and must never be overwritten by the evaluation runner.

## Adding samples

1. Assign a stable, opaque ID that contains no person name or contact detail.
2. Add the source file and its independently reviewed ground truth.
3. Record provenance, consent or licence, annotation method, and reviewer in a
   private dataset register; do not place personal data in public metadata.
4. Run the evaluation command. Resolve validation issues in the source dataset
   rather than inventing missing labels.
5. Use at least 30 samples per important language or document-format slice
   before treating percentile or quality metrics as representative.

## Privacy rules

- Never add a real user's Resume, candidate answer, interview transcript,
  prompt, token, or audio recording.
- Use consented, licensed, anonymized, or fully synthetic benchmark material
  according to project policy. Keep provenance outside generated reports.
- Do not use names, emails, phone numbers, or source filenames as case IDs.
- Generated reports may contain counts, averages, rates, percentiles, statuses,
  and aggregate validation issue categories only.
- Review `dataset_validation.json`, `evaluation_report.json`, and
  `evaluation_report.md` before sharing them.

## Run

From the repository root:

```powershell
python backend/scripts/run_system_evaluation.py `
  --dataset backend/evaluation_dataset `
  --output-dir backend/evaluation_results
```

The production model credentials and local speech dependencies must be
configured to obtain real model metrics. Hardware and network conditions are
part of every latency result.
