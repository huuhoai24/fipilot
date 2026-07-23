# CV-Driven AI Interviewer Backend

FastAPI backend for the V2 text interview architecture.

## Main APIs

- `POST /api/v2/resume/upload`
- `POST /api/v2/interview/start`
- `POST /api/v2/interview/{session_id}/answer`
- `GET /api/v2/interview/{session_id}`
- `GET /health`

## Local Development

The complete three-service setup, ADC authentication, Firestore configuration,
and speech runtime instructions are documented in
[`../docs/local-development.md`](../docs/local-development.md).

## Run Backend Only

```bash
pip install -r requirements.txt
uvicorn gateway.main:app --reload --host 0.0.0.0 --port 8000
```

## Architecture

- `app/agents` - resume extraction, planning, question generation, answer evaluation
- `app/api/routes` - V2 FastAPI routes
- `app/prompts` - language-aware prompt builders
- `app/repositories` - SQLite repository abstraction
- `app/schemas` - Pydantic contracts
- `app/services` - document extraction, language instructions, decision engine, orchestrator
