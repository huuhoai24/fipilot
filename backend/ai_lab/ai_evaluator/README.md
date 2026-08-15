# AI Evaluator Lab

## Purpose

Score one candidate answer against the Candidate Profile, Interview Question rubric, and interview configuration.

## Production source

Copied from `services/answer_evaluator/agent.py`, `prompts.py`, and the canonical evaluation schemas.

## System prompt

The independent copy is `SYSTEM_INSTRUCTION` in `prompt.py`; `build_prompt` retains the production text/voice prompt differences.

## Input contract

`EvaluatorInput`: `candidate_profile`, `interview_question`, `answer`, and `interview_config`.

## Output contract

`AnswerEvaluation`-compatible JSON, including nested and top-level scores, evidence-based feedback, missing concepts, and follow-up decision.

## Current model route

Text uses `EVALUATOR_TASK_TYPE` (default `complex`, therefore `GEMINI_COMPLEX_MODEL`, default `gemini-2.5-pro`). Voice uses the `simple` route (`GEMINI_SIMPLE_MODEL`, default `gemini-2.5-flash`) and a zero thinking budget.

## Temperature

`0.1` for text and voice.

## How to run

From `backend/`:

```powershell
python -m ai_lab.ai_evaluator.runner ai_lab/ai_evaluator/input.example.json
python -m ai_lab.ai_evaluator.runner ai_lab/ai_evaluator/input.example.json --model gemini-2.5-flash --temperature 0.2
```

## Example input

See `input.example.json`.

## Example output

See `output.example.json`.

## Known limitations

- Model routing changes with `interview_config.mode`, matching production; compare text and voice runs separately.
- Raw provider text is not exposed by `BaseLLMService.generate_json`; the artifact records that limitation.
- A real run requires Google Application Default Credentials and a configured project.

## Things safe to optimize

- prompt
- temperature
- model
- schema strictness
- few-shot examples
- reasoning instructions
