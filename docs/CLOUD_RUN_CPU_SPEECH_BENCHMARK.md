# Cloud Run CPU Speech Interview Benchmark

This runbook deploys the existing FastAPI application as one Cloud Run CPU
container. It is a latency benchmark, not a production sizing recommendation.
It does not use a separate speech service or a GPU.

## Prerequisites

Set the project, region, Artifact Registry repository, image, service, and
runtime service account:

```bash
PROJECT_ID="your-google-cloud-project"
REGION="us-central1"
REPOSITORY="interview-images"
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/interviewos:cpu-speech"
SERVICE="interviewos-cpu-speech"
SERVICE_ACCOUNT="interviewos-runtime@$PROJECT_ID.iam.gserviceaccount.com"

gcloud config set project "$PROJECT_ID"
gcloud services enable artifactregistry.googleapis.com run.googleapis.com \
  cloudbuild.googleapis.com aiplatform.googleapis.com firestore.googleapis.com
gcloud artifacts repositories create "$REPOSITORY" \
  --repository-format=docker \
  --location="$REGION"
```

If the repository already exists, the final command can be skipped.

## Build The CPU Image

Run from the repository root. The Docker build installs both
`requirements.txt` and `requirements-speech.txt`, uses CPU PyTorch wheels, and
runs `python -m pip check` before the image is produced.

```bash
gcloud builds submit backend --tag "$IMAGE"
```

Optional local validation, without loading or downloading speech models:

```bash
docker build -t interviewos:cpu-speech backend
docker run --rm \
  --entrypoint python \
  -e GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \
  -e AUTH_ENABLED=false \
  -e STT_MODEL=small \
  -e STT_DEVICE=cpu \
  -e STT_COMPUTE_TYPE=int8 \
  -e STT_LANGUAGE=vi \
  -e TTS_DEVICE=cpu \
  interviewos:cpu-speech scripts/check_speech_runtime.py
```

## Deploy The Benchmark

The recommended isolated benchmark shape is 8 vCPU, 32 GiB memory,
concurrency 1, and a 3600-second request timeout for the WebSocket session.
Start with zero minimum instances for cold-start measurements:

```bash
gcloud run deploy "$SERVICE" \
  --image="$IMAGE" \
  --region="$REGION" \
  --execution-environment=gen2 \
  --service-account="$SERVICE_ACCOUNT" \
  --cpu=8 \
  --memory=32Gi \
  --concurrency=1 \
  --timeout=3600 \
  --min-instances=0 \
  --max-instances=1 \
  --port=8080 \
  --allow-unauthenticated \
  --set-env-vars="APP_ENV=production,DEBUG=false,LOG_LEVEL=INFO,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,GEMINI_SIMPLE_MODEL=gemini-2.5-flash,GEMINI_COMPLEX_MODEL=gemini-2.5-pro,EVALUATOR_TASK_TYPE=simple,GEMINI_RESUME_MODEL=gemini-2.5-flash-lite,GEMINI_RESUME_LOCATION=global,AUTH_ENABLED=true,AUTH_PROVIDER=firebase,FIREBASE_PROJECT_ID=$PROJECT_ID,REPOSITORY_BACKEND=firestore,FIRESTORE_DATABASE=(default),STT_MODEL=/opt/fipilot/models/faster-whisper-small,STT_DEVICE=cpu,STT_COMPUTE_TYPE=int8,STT_LANGUAGE=vi,TTS_MODE=v3turbo,TTS_DEVICE=cpu,TTS_PREWARM=true,SPEECH_BENCHMARK_MODE=true,SPEECH_PREWARM_MODELS=true"
```

Set the production frontend origin separately because its URL contains commas
poorly suited to a long inline command:

```bash
gcloud run services update "$SERVICE" \
  --region="$REGION" \
  --update-env-vars="CORS_ALLOWED_ORIGINS=https://your-frontend.example.com"
```

For a warm-model demo, retain one idle instance:

```bash
gcloud run services update "$SERVICE" \
  --region="$REGION" \
  --min-instances=1
```

Return to cold-start benchmarking with `--min-instances=0`. Keep
`SPEECH_SERVICE_URL` unset so STT, VAD, and TTS run inside this application
container.

`TTS_PREWARM=true` starts a minimal internal VieNeu warm-up in the background
during process startup without making health/readiness depend on optional TTS.
It never generates or caches candidate-specific question audio.
The model remains process-local: every Uvicorn worker and every Cloud Run
instance loads its own copy. Multiple workers therefore multiply VieNeu's RAM
or VRAM footprint; this benchmark intentionally uses one process per container.
Scale-to-zero still creates a fresh process and a fresh model cold start.
Keeping a minimum instance warm can reduce candidate-facing cold starts at an
idle-cost tradeoff, but does not share model memory with newly scaled instances.

## Authentication And ADC

`--allow-unauthenticated` only permits the browser to reach Cloud Run. The
application still requires and verifies a Firebase ID token for protected HTTP
and WebSocket operations, and existing session ownership checks remain active.
Add the frontend domain to Firebase Authentication authorized domains and set
the exact HTTPS frontend origin in `CORS_ALLOWED_ORIGINS`.

Do not configure an API key or ship a service-account JSON file. Cloud Run
supplies Application Default Credentials through `SERVICE_ACCOUNT`. Grant that
identity the minimum roles already required by this application, including
Vertex AI User for Gemini and Firestore access for interview persistence.

## Benchmark Logs

With `SPEECH_BENCHMARK_MODE=true`, each measured turn emits a structured
`speech_latency` event containing only status, request/session identifiers, and
these durations:

- `speech_to_stt_final_ms`
- `audio_queue_drain_ms`
- `stt_decode_ms`
- `stt_to_evaluation_ms`
- `evaluation_to_question_ms`
- `question_to_tts_first_audio_ms`
- `total_turn_latency_ms`

Audio, transcript text, candidate answers, prompts, and tokens are not included.
Filter Cloud Logging with:

```text
resource.type="cloud_run_revision"
jsonPayload.event="speech_latency"
```

The image downloads the Faster Whisper and VieNeu-TTS artifacts during Cloud
Build and sets Hugging Face Hub to offline mode at runtime. A cold run includes
instance startup and model initialization, but it must not download model
artifacts. Keep `STT_MODEL=/opt/fipilot/models/faster-whisper-small` in the
Cloud Run service; the remote alias `small` defeats the baked-model guarantee.
A warm run starts after both STT and TTS have completed at least one real turn.

## Expected Limitations

- `small` improves CPU latency but may recognize Vietnamese technical terms less
  accurately than `large-v3-turbo`.
- faster-whisper and VieNeu-TTS compete for the same CPU and memory bandwidth.
- Keep the benchmark service at 8 vCPU/32 GiB. In the measured combined
  VAD/STT pipeline, reducing it to 4 vCPU/16 GiB increased processing for a
  15-second, 469-chunk fixture from 2.316 seconds to 37.041 seconds.
- A new instance must initialize both baked models again, increasing cold-start
  time even though their artifacts are already present in the image.
- Optional TTS prewarm runs once per process. A multi-worker container repeats
  both initialization time and model memory for every worker.
- Min instances set to 1 reduces demo cold starts but incurs idle cost; it does
  not make this a production deployment.
- Concurrency 1 isolates benchmark samples and intentionally limits throughput.
- A WebSocket is bounded by the configured 3600-second request timeout.

If warm CPU `total_turn_latency_ms` remains outside the product target, preserve
these measurements and use them as the baseline for a separate GPU benchmark
milestone. Do not infer GPU sizing from cold-start samples.
