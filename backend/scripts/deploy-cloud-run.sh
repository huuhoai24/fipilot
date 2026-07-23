#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID=""
FRONTEND_ORIGIN=""
REGION="us-central1"
ARTIFACT_REPOSITORY="ai-interview"
IMAGE_NAME="backend"
SERVICE_NAME="ai-interview-backend"
SERVICE_ACCOUNT=""
IMAGE_TAG="$(date -u +%Y%m%d-%H%M%S)"
TIMEOUT_SECONDS=300
MAX_INSTANCES=5
MIN_INSTANCES=0
CONCURRENCY=20

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-id) PROJECT_ID="$2"; shift 2 ;;
    --frontend-origin) FRONTEND_ORIGIN="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    --repository) ARTIFACT_REPOSITORY="$2"; shift 2 ;;
    --image-name) IMAGE_NAME="$2"; shift 2 ;;
    --service-name) SERVICE_NAME="$2"; shift 2 ;;
    --service-account) SERVICE_ACCOUNT="$2"; shift 2 ;;
    --image-tag) IMAGE_TAG="$2"; shift 2 ;;
    --timeout) TIMEOUT_SECONDS="$2"; shift 2 ;;
    --max-instances) MAX_INSTANCES="$2"; shift 2 ;;
    --min-instances) MIN_INSTANCES="$2"; shift 2 ;;
    --concurrency) CONCURRENCY="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$PROJECT_ID" || ! "$FRONTEND_ORIGIN" =~ ^https://[^/]+/?$ ]]; then
  echo "Usage: $0 --project-id PROJECT --frontend-origin https://frontend.example [options]" >&2
  exit 2
fi

SERVICE_ACCOUNT="${SERVICE_ACCOUNT:-ai-interview-runtime@$PROJECT_ID.iam.gserviceaccount.com}"
SERVICE_ACCOUNT_NAME="${SERVICE_ACCOUNT%%@*}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
IMAGE_REFERENCE="$REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"

gcloud config set project "$PROJECT_ID"
gcloud services enable \
  run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com \
  aiplatform.googleapis.com firestore.googleapis.com firebase.googleapis.com \
  identitytoolkit.googleapis.com --project="$PROJECT_ID"

if ! gcloud artifacts repositories describe "$ARTIFACT_REPOSITORY" \
  --location="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud artifacts repositories create "$ARTIFACT_REPOSITORY" \
    --repository-format=docker --location="$REGION" \
    --description="AI Interview production images" --project="$PROJECT_ID"
fi

if ! gcloud iam service-accounts describe "$SERVICE_ACCOUNT" \
  --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
    --display-name="AI Interview Cloud Run runtime" --project="$PROJECT_ID"
fi

for role in roles/aiplatform.user roles/datastore.user roles/firebaseauth.viewer roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SERVICE_ACCOUNT" --role="$role" --format=none --quiet
done

BUILD_SERVICE_ACCOUNT="$(gcloud builds get-default-service-account \
  --project="$PROJECT_ID" --format='value(serviceAccountEmail)')"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$BUILD_SERVICE_ACCOUNT" \
  --role=roles/cloudbuild.builds.builder --format=none --quiet

if ! gcloud firestore databases describe --database='(default)' \
  --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud firestore databases create --database='(default)' \
    --location="$REGION" --type=firestore-native --delete-protection \
    --project="$PROJECT_ID" --quiet
fi

gcloud builds submit "$BACKEND_DIR" --tag="$IMAGE_REFERENCE" --project="$PROJECT_ID"

ENV_FILE="$(mktemp)"
trap 'rm -f "$ENV_FILE"' EXIT
cat >"$ENV_FILE" <<EOF
APP_ENV: 'production'
DEBUG: 'false'
LOG_LEVEL: 'INFO'
GOOGLE_CLOUD_PROJECT: '$PROJECT_ID'
GOOGLE_CLOUD_LOCATION: '$REGION'
GEMINI_SIMPLE_MODEL: 'gemini-2.5-flash'
GEMINI_COMPLEX_MODEL: 'gemini-2.5-pro'
REPOSITORY_BACKEND: 'firestore'
FIRESTORE_DATABASE: '(default)'
FIRESTORE_USERS_COLLECTION: 'users'
FIRESTORE_CANDIDATES_COLLECTION: 'candidates'
FIRESTORE_INTERVIEWS_COLLECTION: 'interviews'
AUTH_ENABLED: 'true'
AUTH_PROVIDER: 'firebase'
FIREBASE_PROJECT_ID: '$PROJECT_ID'
CORS_ALLOWED_ORIGINS: '${FRONTEND_ORIGIN%/}'
EOF

gcloud run deploy "$SERVICE_NAME" --image="$IMAGE_REFERENCE" \
  --region="$REGION" --platform=managed --service-account="$SERVICE_ACCOUNT" \
  --execution-environment=gen2 --port=8080 --timeout="${TIMEOUT_SECONDS}s" \
  --max-instances="$MAX_INSTANCES" --min-instances="$MIN_INSTANCES" \
  --concurrency="$CONCURRENCY" --memory=1Gi --cpu=1 \
  --env-vars-file="$ENV_FILE" --allow-unauthenticated \
  --project="$PROJECT_ID" --quiet

SERVICE_URL="$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" \
  --project="$PROJECT_ID" --format='value(status.url)')"
echo "Image: $IMAGE_REFERENCE"
echo "Service URL: $SERVICE_URL"
python3 "$SCRIPT_DIR/smoke_test.py" "$SERVICE_URL"
