# Local Speech Interview Demo

This guide runs the existing local Fipilot architecture for a Speech
Interview demo. It does not change the Text Interview, Firebase authentication,
Gemini, Whisper, or VieNeu-TTS flows.

## Requirements

- Python 3.12
- Node.js 22 and npm
- Google Cloud CLI
- A microphone and a browser that supports `AudioWorklet`
- NVIDIA CUDA is optional; CPU speech inference is supported but slower

Install the application and speech dependencies:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt -r requirements-speech.txt
python -m pip check

cd ..\frontend
npm ci
cd ..
```

The standard PyPI install uses CPU Torch wheels. For an NVIDIA demo, install a
matched CUDA Torch/TorchAudio pair before the requirements command, using the
wheel index compatible with the installed driver. For example, CUDA 12.8:

```powershell
python -m pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r requirements-dev.txt -r requirements-speech.txt
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

Continue only when the final value is `True` for a CUDA configuration. Keep
Torch and TorchAudio on the same release.

Create local configuration from the tracked examples:

```powershell
Copy-Item backend\.env.local.example backend\.env.local
Copy-Item backend\.env.speech.example backend\.env.speech
Copy-Item frontend\.env.local.example frontend\.env.local
```

## Firebase localhost configuration

In Firebase Console, enable the Google sign-in provider and add `localhost` to
Authentication's authorized domains. Copy the public Firebase web application
values into `frontend/.env.local`:

```env
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
VITE_FIREBASE_APP_ID=
```

The browser continues to use Firebase ID tokens for HTTP and voice WebSocket
authentication. Do not enable an authentication bypass for the demo.

## Google ADC and Gemini

Authenticate the Google Cloud CLI and Application Default Credentials:

```powershell
gcloud auth login
gcloud auth application-default login
gcloud config set project project-7dffc340-f73f-4e62-aec
```

The backend uses ADC for Vertex Gemini. No API key or service-account JSON is
required. Keep the existing Gemini model settings in `backend/.env.local`.

## Run the demo

Use three terminals from the repository root.

Terminal 1 — backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn gateway.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2 — speech inference:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m speech_service.main
```

Terminal 3 — frontend:

```powershell
cd frontend
npm run dev -- --host localhost
```

Open `http://localhost:5173`.

## Speech model loading

The speech service loads Silero VAD, faster-whisper, and VieNeu-TTS lazily. The
first demo run can take longer while model artifacts are downloaded and cached.
Wait for the speech readiness endpoint before beginning:

```powershell
Invoke-RestMethod http://localhost:9000/health
Invoke-RestMethod http://localhost:9000/ready
Invoke-RestMethod http://localhost:8000/ready
```

For a CPU-only machine, set the following in `backend/.env.speech`:

```env
STT_DEVICE=cpu
STT_COMPUTE_TYPE=int8
TTS_DEVICE=cpu
```

## Demo checklist

1. Sign in with Google and start a Speech Interview.
2. Allow microphone access and wait for the first question audio.
3. Answer naturally; do not press a confirm or submit button.
4. Confirm the UI moves through speaking, understanding, evaluating, and AI
   speaking states.
5. Confirm VAD submits after silence and the next question plays automatically.
6. Speak while the AI is talking and confirm barge-in stops playback and
   returns to listening.
7. Briefly interrupt the local connection and confirm listening resumes after
   reconnect.

Only timing metadata is logged for local latency debugging. Audio, transcripts,
prompts, and candidate answers must not be logged. Set `LOG_LEVEL=DEBUG` in
`backend/.env.local` to show the `voice_turn_latency` debug event.
