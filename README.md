# AI Interview Platform

Local development runs the React client, FastAPI gateway, and speech inference
service as three processes:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- Speech service: `http://localhost:9000`

Production architecture and API contracts are unchanged.

## Quick Start

### 1. Install dependencies

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt -r requirements-speech.txt

cd ..\frontend
npm ci
```

### 2. Configure local environment

```powershell
Copy-Item backend\.env.local.example backend\.env.local
Copy-Item backend\.env.speech.example backend\.env.speech
Copy-Item frontend\.env.local.example frontend\.env.local
```

Fill in the four public Firebase web configuration values in
`frontend/.env.local`. Do not add service-account credentials or private keys.

### 3. Authenticate Google Cloud

```powershell
gcloud auth login
gcloud auth application-default login
gcloud config set project project-7dffc340-f73f-4e62-aec
```

The backend uses Application Default Credentials. Do not set
`GOOGLE_APPLICATION_CREDENTIALS` to a downloaded service-account file.

### 4. Run backend

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_backend.ps1
```

### 5. Run speech service

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_speech_service.ps1
```

### 6. Run frontend

```powershell
cd frontend
npm run dev -- --host localhost
```

Open `http://localhost:5173`.

Linux/macOS equivalents:

```bash
./scripts/run_backend.sh
./scripts/run_speech_service.sh
cd frontend && npm run dev -- --host localhost
```

See [Local Development](docs/local-development.md) for Firebase, CUDA, Docker,
health checks, and end-to-end verification. See
[Local Architecture](docs/local-architecture.md) for service boundaries.
