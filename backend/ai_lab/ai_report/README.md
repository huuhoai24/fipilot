# AI Report Lab

## Purpose

Generate the same evidence-based practice coaching report as the production Report Generator.

## Production source

Copied from `services/report_generator/agent.py`, `prompts.py`, and `schemas.py`, with the exact production agent inputs represented by `candidate_profile` and `interview_state`.

## System prompt

The independent copy is `SYSTEM_INSTRUCTION` in `prompt.py`. `build_prompt` locally copies the production payload selection: Candidate Profile, Interview Config, Interview Plan, and completed Interview Turns.

## Input contract

`ReportInput`: a `candidate_profile` plus the full `InterviewSessionState` supplied to the production agent. The state includes its own immutable Candidate Profile snapshot, configuration, plan, and completed turns.

## Output contract

The local `InterviewReport` exactly mirrors the production Report Generator schema, including scores, coaching narrative, skill assessments, learning plan, recommendation enum, confidence, and generated time. Like production, the lab replaces provider placeholders for `id`, `session_id`, and `generated_at` after generation.

## Current model route

Production `complex` route: `GEMINI_COMPLEX_MODEL` (default `gemini-2.5-pro`).

## Temperature

`0.1`.

## How to run

From `backend/`:

```powershell
python -m ai_lab.ai_report.runner ai_lab/ai_report/input.example.json
python -m ai_lab.ai_report.runner ai_lab/ai_report/input.example.json --model gemini-2.5-flash --temperature 0.2
```

## Example input

See `input.example.json`.

## Example output

See `output.example.json`.

## Known limitations

- The input intentionally preserves both the separately loaded Candidate Profile and the Candidate Profile snapshot inside session state because production currently passes both.
- Raw provider text is not exposed by `BaseLLMService.generate_json`; the artifact records that limitation.
- A real run requires Google Application Default Credentials and a configured project.

## Things safe to optimize

- prompt
- temperature
- model
- schema strictness
- few-shot examples
- reasoning instructions
