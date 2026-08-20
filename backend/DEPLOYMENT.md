# Cloud Run deployment

The backend is one FastAPI container. Cloud Run provides the listening port through `PORT`; the image defaults to port `8080`. Production uses the Cloud Run service account through Application Default Credentials (ADC), so do not set or ship `GOOGLE_APPLICATION_CREDENTIALS`.

Production startup fails clearly unless Firestore is selected, Firebase authentication is enabled, a Google Cloud project is configured, and exactly one HTTPS CORS origin is supplied.

## Automated deployment

From the repository root on Windows:

```powershell
.\backend\scripts\deploy-cloud-run.ps1 `
  -ProjectId "your-project-id" `
  -Region "us-central1" `
  -ArtifactRepository "ai-interview" `
  -ImageName "backend" `
  -ServiceName "ai-interview-backend" `
  -ServiceAccount "ai-interview-runtime@your-project-id.iam.gserviceaccount.com" `
  -FrontendOrigin "https://your-project-id.web.app"
```

On macOS or Linux:

```bash
./backend/scripts/deploy-cloud-run.sh \
  --project-id "your-project-id" \
  --region "us-central1" \
  --repository "ai-interview" \
  --image-name "backend" \
  --service-name "ai-interview-backend" \
  --service-account "ai-interview-runtime@your-project-id.iam.gserviceaccount.com" \
  --frontend-origin "https://your-project-id.web.app"
```

Both scripts enable required APIs, create missing Artifact Registry, runtime service account, and default Firestore resources, grant runtime IAM roles, submit a versioned image through Cloud Build, deploy, print the service URL, and run the smoke test. Existing resources are reused.

The scripts query Cloud Build's selected default build identity and grant that identity `roles/cloudbuild.builds.builder`. New Google Cloud projects may select the Compute Engine default service account instead of the legacy Cloud Build account. This build permission is separate from the Cloud Run runtime roles.

`.gcloudignore` excludes local environment files, SQLite data, tests, caches, and credential-shaped JSON files from the Cloud Build source upload. `.dockerignore` independently enforces the same boundary for the container build context.

The deployment uses one Uvicorn process per container, Cloud Run's `$PORT`, generation 2 execution, a 300-second request timeout, concurrency 20, maximum 5 instances, and minimum 0 instances by default. PowerShell parameters or shell arguments can override scaling and timeout values.

## Firestore data model

All candidate and interview data is scoped below its Firebase user document:

```text
users/{user_id}
  candidates/{candidate_id}
  interviews/{session_id}
```

The final report is embedded in the corresponding interview document under `report`. This keeps report reads and idempotent report generation atomic at the session boundary. Firestore timestamps are used for creation and update fields.

## Required configuration

```text
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
GOOGLE_CLOUD_PROJECT=<project-id>
GOOGLE_CLOUD_LOCATION=us-central1
GEMINI_SIMPLE_MODEL=gemini-2.5-flash
GEMINI_COMPLEX_MODEL=gemini-2.5-pro
DATABASE_URL=sqlite:///./interview_app.db
REPOSITORY_BACKEND=firestore
FIRESTORE_DATABASE=(default)
FIRESTORE_USERS_COLLECTION=users
FIRESTORE_CANDIDATES_COLLECTION=candidates
FIRESTORE_INTERVIEWS_COLLECTION=interviews
AUTH_ENABLED=true
AUTH_PROVIDER=firebase
FIREBASE_PROJECT_ID=<project-id>
CORS_ALLOWED_ORIGINS=https://<frontend-domain>
```

Optional Firestore vector retrieval remains disabled by default. After its
index and catalog are provisioned according to
[`docs/FIRESTORE_VECTOR_KNOWLEDGE.md`](../docs/FIRESTORE_VECTOR_KNOWLEDGE.md),
enable it with:

```text
INTERVIEW_KNOWLEDGE_BACKEND=firestore_vector
INTERVIEW_KNOWLEDGE_COLLECTION=interview_knowledge_chunks
INTERVIEW_KNOWLEDGE_VECTOR_FIELD=embedding
INTERVIEW_KNOWLEDGE_EMBEDDING_MODEL=gemini-embedding-001
INTERVIEW_KNOWLEDGE_EMBEDDING_LOCATION=global
INTERVIEW_KNOWLEDGE_EMBEDDING_DIMENSIONS=768
INTERVIEW_KNOWLEDGE_TOP_K=5
```

`DATABASE_URL` remains required for SQLite development and rollback. It is not used by interview persistence when `REPOSITORY_BACKEND=firestore`. Keep CORS origins explicit in production.

## Build locally

From the repository root:

```bash
docker build -t ai-interview-backend:local ./backend
docker run --rm -p 8080:8080 \
  -e GOOGLE_CLOUD_PROJECT=local-project \
  -e AUTH_ENABLED=false \
  -e REPOSITORY_BACKEND=sqlite \
  ai-interview-backend:local
```

Check `http://127.0.0.1:8080/health` for liveness and `http://127.0.0.1:8080/ready` for dependency readiness.

## Google Cloud setup

Set deployment values first:

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export REPOSITORY="ai-interview"
export IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/backend:latest"
export SERVICE="ai-interview-backend"
export SERVICE_ACCOUNT="ai-interview-runtime@$PROJECT_ID.iam.gserviceaccount.com"
export FRONTEND_ORIGIN="https://your-frontend.example"

gcloud config set project "$PROJECT_ID"
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  aiplatform.googleapis.com \
  firestore.googleapis.com \
  identitytoolkit.googleapis.com

gcloud artifacts repositories create "$REPOSITORY" \
  --repository-format=docker \
  --location="$REGION"

gcloud iam service-accounts create ai-interview-runtime \
  --display-name="AI Interview runtime"
```

Create the Firestore `(default)` database in Native mode before deployment if the project does not already have one.

Grant only the runtime roles used by this service:

```bash
for ROLE in roles/aiplatform.user roles/datastore.user roles/firebaseauth.viewer roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="$ROLE"
done
```

`roles/firebaseauth.viewer` supplies `firebaseauth.users.get`, which is required because backend token verification checks revocation state as well as token signature and expiry.

Build and deploy:

```bash
gcloud builds submit ./backend --tag "$IMAGE"

gcloud run deploy "$SERVICE" \
  --image="$IMAGE" \
  --region="$REGION" \
  --service-account="$SERVICE_ACCOUNT" \
  --allow-unauthenticated \
  --set-env-vars="APP_ENV=production,DEBUG=false,LOG_LEVEL=INFO,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$REGION,GEMINI_SIMPLE_MODEL=gemini-2.5-flash,GEMINI_COMPLEX_MODEL=gemini-2.5-pro,REPOSITORY_BACKEND=firestore,FIRESTORE_DATABASE=(default),AUTH_ENABLED=true,AUTH_PROVIDER=firebase,FIREBASE_PROJECT_ID=$PROJECT_ID,CORS_ALLOWED_ORIGINS=$FRONTEND_ORIGIN"
```

Cloud Run is public at the transport layer so the browser can submit a Firebase ID token. Protected application routes still reject requests without a valid token.

Verify the deployed service:

```bash
SERVICE_URL="$(gcloud run services describe "$SERVICE" --region="$REGION" --format='value(status.url)')"
curl --fail "$SERVICE_URL/health"
curl --fail "$SERVICE_URL/ready"
curl --fail -H "Authorization: Bearer $FIREBASE_ID_TOKEN" "$SERVICE_URL/api/v2/auth/me"
```

## Frontend configuration

Set these at frontend build time. Do not append `/api` to the backend base URL.

```text
VITE_API_BASE_URL=https://<cloud-run-service-url>
VITE_FIREBASE_API_KEY=<firebase-web-api-key>
VITE_FIREBASE_AUTH_DOMAIN=<project-id>.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=<project-id>
VITE_FIREBASE_APP_ID=<firebase-web-app-id>
```

The Firebase web API key identifies the Firebase project and is not a server credential. Backend credentials are supplied only by the Cloud Run service identity.

Production builds fail when any required variable is empty or when `VITE_API_BASE_URL` is not HTTPS. Firebase is initialized once using `getApps()`/`getApp()`. No ID token is embedded at build time; the frontend obtains the current user's token at request time.

After Hosting deployment, add the generated `PROJECT_ID.web.app` domain, `PROJECT_ID.firebaseapp.com`, and any approved custom frontend domain under Firebase Console > Authentication > Settings > Authorized domains. Remove obsolete development or preview domains for a strict production allowlist.

Deploy the existing React SPA from `frontend`:

```bash
npm run build:production
npx firebase-tools deploy --only hosting --project "$PROJECT_ID"
```

`frontend/firebase.json` rewrites unknown paths to `index.html`, applies immutable one-year caching to hashed assets, and prevents caching of `index.html`.

Run remote checks without printing credentials:

```bash
python backend/scripts/smoke_test.py "$SERVICE_URL"
FIREBASE_ID_TOKEN="..." python backend/scripts/smoke_test.py "$SERVICE_URL"
```

The token can instead be entered with `--prompt-token`, which uses hidden input.

## Operational notes

- `/health` is process liveness and does not access external services.
- `/ready` checks the selected repository and returns `503` when it is unavailable.
- Logs are single-line JSON on stdout and include `request_id`, status, duration, route, and interview `session_id` when present.
- Send `X-Request-ID` to correlate a client operation; otherwise the backend generates one and returns it in the response.
- Never place resume text, candidate answers, prompts, Firebase ID tokens, or service account keys in logs.

References: [Cloud Run service identity](https://docs.cloud.google.com/run/docs/securing/service-identity), [Firestore IAM](https://docs.cloud.google.com/firestore/native/docs/security/iam), [Vertex AI access control](https://cloud.google.com/vertex-ai/docs/general/access-control), and [Cloud Logging IAM](https://docs.cloud.google.com/logging/docs/access-control).
