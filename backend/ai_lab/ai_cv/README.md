# AI CV Lab

## Purpose

Classify Resume text and extract Candidate Profile-compatible JSON without changing the production Resume AI.

## Production source

Copied from `services/profile_scanner/agent.py`, `prompts.py`, and `schemas.py`. The production dependency wiring in `core/dependencies.py` is mirrored for its Resume-specific model and Vertex location.

## System prompt

The independent copy is `SYSTEM_INSTRUCTION` in `prompt.py`; the complete user prompt is built by `build_prompt`. It treats the Resume as untrusted text and retains production's 12,000-character prompt limit.

## Input contract

`CVInput`: one non-empty `resume_text` string.

## Output contract

`CandidateProfile`-compatible JSON. The provider response first validates as the local `ResumeExtractionResult`, then uses the copied production normalization and limits to create `CandidateProfile`.

## Current model route

Production Resume route: `GEMINI_RESUME_MODEL` (default `gemini-2.5-flash-lite`) through the `simple` task route at `GEMINI_RESUME_LOCATION` (default `global`), with one provider attempt.

## Temperature

`0.1`.

## How to run

From `backend/`:

```powershell
python -m ai_lab.ai_cv.runner ai_lab/ai_cv/input.example.json
python -m ai_lab.ai_cv.runner ai_lab/ai_cv/samples/cv_without_skills_heading.json --model gemini-2.5-flash --temperature 0.2
```

## Example input

See `input.example.json` and `samples/`.

## Example output

See `output.example.json`.

## Known limitations

- The production-compatible prompt truncates Resume text after 12,000 characters.
- `BaseLLMService.generate_json` exposes the validated model, not the provider's raw response. `raw_response.txt` records this limitation instead of fabricating raw data.
- Running the CLI requires Google Application Default Credentials and a configured Google Cloud project.

## Things safe to optimize

- prompt
- temperature
- model
- schema strictness
- few-shot examples
- reasoning instructions
