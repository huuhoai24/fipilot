# AI Question Lab

## Purpose

Generate one evidence-grounded adaptive Interview Question for a selected interview round.

## Production source

Copied from `services/question_generator/agent.py`, `prompts.py`, and the canonical interview schemas. This lab exercises the structured non-streaming production path.

## System prompt

The independent copy is `SYSTEM_INSTRUCTION` in `prompt.py`; `build_prompt` includes the local language and voice-personality instructions.

## Input contract

`QuestionInput`: `candidate_profile`, `interview_round`, and `interview_config`.

## Output contract

`InterviewQuestion`-compatible JSON with one primary question, language, topic, difficulty, reasoning, expected answer points, and optional follow-ups.

## Current model route

Production `simple` route: `GEMINI_SIMPLE_MODEL` (default `gemini-2.5-flash`).

## Temperature

`0.2`.

## How to run

From `backend/`:

```powershell
python -m ai_lab.ai_question.runner ai_lab/ai_question/input.example.json
python -m ai_lab.ai_question.runner ai_lab/ai_question/input.example.json --model gemini-2.5-pro --temperature 0.1
```

## Example input

See `input.example.json`.

## Example output

See `output.example.json`.

## Known limitations

- This runner validates the structured `generate_json` path; it does not reproduce the separate streaming transport path.
- Raw provider text is not exposed by `BaseLLMService.generate_json`; the artifact records that limitation.
- A real run requires Google Application Default Credentials and a configured project.

## Things safe to optimize

- prompt
- temperature
- model
- schema strictness
- few-shot examples
- reasoning instructions
