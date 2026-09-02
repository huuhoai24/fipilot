# FiPilot

FiPilot is an AI-powered technical interview platform. It analyzes resumes, generates experience-based questions, evaluates answers, and produces interview reports.

## Demo

[![Watch the FiPilot demo](docs/demo-cover.jpg)](docs/demo.mp4?raw=true)

**[▶ Watch or download the demo](docs/demo.mp4?raw=true)**

## Features

- PDF and DOCX resume analysis with OCR fallback.
- Questions tailored to the selected role, level, and resume.
- Adaptive follow-up questions and answer evaluation.
- Voice input and output through Azure Speech.
- Authentication and interview history.
- PostgreSQL persistence.

## Stack

- Frontend: Next.js 16, React 19, TypeScript
- Backend: Python 3.12, FastAPI, Pydantic
- AI: Azure OpenAI, Azure Speech, RapidOCR
- Database: PostgreSQL, SQLAlchemy, Alembic

## Architecture

```text
Next.js → FastAPI → DocumentService → ResumeAgent → Azure OpenAI
                  ↘ Interview Engine + Knowledge Base
                  ↘ Azure Speech
                  ↘ PostgreSQL
```

## Setup

Requirements: Python 3.12+, Node.js 24+, [uv](https://docs.astral.sh/uv/), Docker, and ffmpeg.

### 1. Environment variables

```bash
cp backend/.env.example backend/.env
```

Configure `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://fipilot:fipilot@127.0.0.1:5432/fipilot
COOKIE_SECURE=false

AZURE_OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/v1/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT=your-chat-deployment
AZURE_OPENAI_SIMPLE_DEPLOYMENT=your-chat-deployment
AZURE_OPENAI_COMPLEX_DEPLOYMENT=your-chat-deployment

AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=your-speech-region
AZURE_SPEECH_VOICE=vi-VN-HoaiMyNeural
```

Create `frontend/.env.local`:

```env
RESUME_API_URL=http://127.0.0.1:8000
```

### 2. PostgreSQL

```bash
cd backend
docker compose up -d postgres
```

### 3. Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Swagger UI: <http://127.0.0.1:8000/docs>

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:3000>.

## Tests

```bash
cd backend
uv run python -m unittest discover -s test -p 'test_*.py' -v

cd ../frontend
npm run typecheck -- --incremental false
```

## Deployment

See [docs/AZURE_DEPLOY.md](docs/AZURE_DEPLOY.md).
