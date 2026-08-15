# AI Planner Lab

## Purpose

Build an Interview Plan from a Candidate Profile, interview configuration, and explicit curated knowledge topics.

## Production source

Copied from `services/interview_planner/agent.py`, `prompts.py`, and the canonical interview schemas. Knowledge retrieval itself stays outside this lab; its resulting topic strings are an explicit input.

## System prompt

The independent copy is `SYSTEM_INSTRUCTION` in `prompt.py`. `build_prompt` also contains a local copy of production's language and prompt-envelope behavior.

## Input contract

`PlannerInput`: `candidate_profile`, `interview_config`, and `knowledge_topics`.

## Output contract

`InterviewPlan`-compatible JSON containing duration, rounds, coverage goals, risk areas, and planner summary.

## Current model route

Production `simple` route: `GEMINI_SIMPLE_MODEL` (default `gemini-2.5-flash`).

## Temperature

`0.1`.

## How to run

From `backend/`:

```powershell
python -m ai_lab.ai_planner.runner ai_lab/ai_planner/input.example.json
python -m ai_lab.ai_planner.runner ai_lab/ai_planner/input.example.json --model gemini-2.5-pro --temperature 0.2
```

## Example input

See `input.example.json`.

## Example output

See `output.example.json`.

## Known limitations

- Curated knowledge retrieval is not run automatically; callers supply `knowledge_topics` so experiments remain deterministic.
- The LLM infrastructure does not expose raw provider responses; `raw_response.txt` documents that limitation.
- A real run requires Google Application Default Credentials and a configured project.

## Things safe to optimize

- prompt
- temperature
- model
- schema strictness
- few-shot examples
- reasoning instructions
