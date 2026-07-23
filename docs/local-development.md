# Local Development

This guide runs the production-compatible application architecture on
localhost. It does not use API keys for Vertex AI, service-account files, local
authentication bypasses, or persisted audio.

## Services

| Service | URL | Purpose |
| --- | --- | --- |
| React frontend | `http://localhost:5173` | Firebase login and interview UI |
| FastAPI backend | `http://localhost:8000` | API gateway and interview orchestration |
| Speech inference | `http://localhost:9000` | VAD, STT, and streaming TTS |

The backend still uses Firebase Authentication, Firestore, and Vertex Gemini in
Google Cloud. Only the application processes run locally.

## Prerequisites

- Python 3.12
- Node.js 22 and npm
- Google Cloud CLI
- A Firestore database in project `project-7dffc340-f73f-4e62-aec`
- NVIDIA driver and CUDA-compatible GPU for the default speech configuration
- Docker Desktop with NVIDIA Container Toolkit for GPU-enabled Compose

Install the Google Cloud CLI from the official Google Cloud documentation, then
authenticate both the CLI and the application:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project project-7dffc340-f73f-4e62-aec
```

The second command creates user Application Default Credentials (ADC). The
backend and Google client libraries discover ADC automatically. Do not download
a service-account key and do not set `GOOGLE_APPLICATION_CREDENTIALS`.

## Install Dependencies

Windows PowerShell:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt -r requirements-speech.txt

cd ..\frontend
npm ci
cd ..
```

Linux/macOS:

```bash
python3.12 -m venv backend/.venv
. backend/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements-dev.txt -r backend/requirements-speech.txt
cd frontend && npm ci && cd ..
```

Speech packages are large. The Whisper and VieNeu model artifacts are loaded
into the user cache at runtime and are never committed to the repository.

## Configure Environment

Create ignored local files from the tracked examples:

```powershell
Copy-Item backend\.env.local.example backend\.env.local
Copy-Item backend\.env.speech.example backend\.env.speech
Copy-Item frontend\.env.local.example frontend\.env.local
```

Linux/macOS:

```bash
cp backend/.env.local.example backend/.env.local
cp backend/.env.speech.example backend/.env.speech
cp frontend/.env.local.example frontend/.env.local
```

`backend/.env.local` selects:

- Firestore persistence with `REPOSITORY_BACKEND=firestore`
- Firebase token verification
- Vertex Gemini through ADC
- Remote speech through `http://localhost:9000`
- Exact CORS/WebSocket origin `http://localhost:5173`

`backend/.env.speech` configures faster-whisper `small`, Vietnamese, CUDA
`float16`, Silero VAD, and VieNeu-TTS.

For CPU-only development, change these values:

```env
STT_DEVICE=cpu
STT_COMPUTE_TYPE=int8
TTS_DEVICE=cpu
```

CPU speech inference is substantially slower.

## Firebase Local Login

In Firebase Console, open:

`Authentication -> Settings -> Authorized domains`

Ensure `localhost` is present. Enable the Google sign-in provider under:

`Authentication -> Sign-in method`

Copy the Firebase web app configuration from:

`Project settings -> General -> Your apps -> Web app`

Set these values in `frontend/.env.local`:

```env
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_APP_ID=
```

Firebase web configuration identifies the public web application; it is not a
Firebase Admin credential. It is still kept out of source control in this
project.

For every HTTP API request, the frontend obtains the signed-in user's Firebase
ID token and sends:

```http
Authorization: Bearer <Firebase ID token>
```

For voice WebSockets, the same token is sent through the `firebase-auth`
subprotocol. The backend verifies it with Firebase Admin and checks session
ownership before accepting the connection.

## Run Natively

Use three terminals from the repository root.

Terminal 1, backend:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_backend.ps1
```

Terminal 2, speech:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_speech_service.ps1
```

Terminal 3, frontend:

```powershell
cd frontend
npm run dev -- --host localhost
```

Linux/macOS:

```bash
./scripts/run_backend.sh
./scripts/run_speech_service.sh
cd frontend && npm run dev -- --host localhost
```

The scripts activate `backend/.venv` or `backend/venv`, load only the matching
local env file into the child process, and start the requested service.

## Run With Docker Compose

Create the three local env files first. Compose mounts the existing user ADC
directory read-only; it does not copy credentials into an image.

Windows PowerShell:

```powershell
$env:GOOGLE_ADC_DIR="$env:APPDATA\gcloud"
docker compose -f docker-compose.local.yml up --build
```

Linux/macOS:

```bash
export GOOGLE_ADC_DIR="$HOME/.config/gcloud"
docker compose -f docker-compose.local.yml up --build
```

Inside Compose, the backend overrides the speech URL to
`http://speech-service:9000`. No model weights, `.env` files, Firebase private
keys, or Google credentials are included in the images.

The Compose speech service requests a GPU. For CPU-only Docker development,
remove `gpus: all` locally and use the CPU speech settings listed above.

## Health Checks

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/ready
Invoke-RestMethod http://localhost:9000/health
Invoke-RestMethod http://localhost:9000/ready
```

Bash:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:9000/health
curl http://localhost:9000/ready
```

`/health` confirms the process is serving requests. Backend `/ready` also checks
the configured repository. Speech `/ready` confirms speech runtime
configuration; models remain lazily loaded until first use.

## Verification

Automated:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q core gateway infrastructure orchestrator services shared speech_service

cd ..\frontend
npm run build
```

Text Interview checklist:

1. Sign in with Google.
2. Upload a CV.
3. Start a Text Interview.
4. Answer at least one question.
5. Complete the interview and generate the report.

Speech Interview checklist:

1. Sign in and upload a CV.
2. Select Speech Interview.
3. Allow microphone access.
4. Confirm the AI question is streamed and spoken.
5. Speak an answer and confirm partial/final transcript updates.
6. Confirm VAD submits automatically.
7. Confirm evaluation and the next spoken question arrive.
8. Interrupt AI speech and confirm barge-in returns to listening.

## Security

Never commit:

- `.env` or `.env.*` runtime files
- Firebase Admin credentials
- Google service-account JSON
- Application Default Credential files
- API keys, private keys, certificates, or model weights

Local environment examples contain names, project identifiers, model choices,
and empty public Firebase web fields only.
