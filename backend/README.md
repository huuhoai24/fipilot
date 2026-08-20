# FiPilot backend

## 1. PostgreSQL

The local development database uses PostgreSQL 17 and stores its data in the
`fipilot-postgres` Docker volume.

Start it with Docker Compose when the Compose plugin is available:

```bash
docker compose up -d postgres
```

On a Docker installation without Compose, use:

```bash
docker run --name fipilot-postgres \
  -e POSTGRES_DB=fipilot \
  -e POSTGRES_USER=fipilot \
  -e POSTGRES_PASSWORD=fipilot \
  -p 5432:5432 \
  -v fipilot-postgres:/var/lib/postgresql/data \
  -d postgres:17-alpine
```

## 2. Setup & Run with `uv`

Install dependencies and sync the virtual environment using `uv`:

```bash
uv sync
```

Apply database migrations:

```bash
uv run alembic upgrade head
```

Start the API server:

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## 3. Architecture & Persistence

The persistence layer stores resumes, interview sessions, answer turns with
their evaluations, and final reports. If `DATABASE_URL` is absent, AI endpoints
continue to work without persistence so the frontend cache remains a fallback.

Authentication uses bcrypt password hashes and opaque, random session tokens.
Only the SHA-256 hash of a session token is stored in PostgreSQL; the raw token
is sent to the browser in an HttpOnly `fipilot_session` cookie. The frontend
proxies `/api/auth/login`, `/api/auth/register`, `/api/auth/me`, and
`/api/auth/logout` to the backend.
