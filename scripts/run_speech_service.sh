#!/usr/bin/env sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BACKEND_ROOT="$REPO_ROOT/backend"
ENV_FILE="${SPEECH_ENV_FILE:-$BACKEND_ROOT/.env.speech}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing $ENV_FILE. Copy backend/.env.speech.example to backend/.env.speech first." >&2
  exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
  line=$(printf "%s" "$line" | tr -d '\r')
  case "$line" in
    ""|\#*) continue ;;
    *=*) export "$line" ;;
    *)
      echo "Invalid environment entry in $ENV_FILE: $line" >&2
      exit 1
      ;;
  esac
done < "$ENV_FILE"

if [ -f "$BACKEND_ROOT/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  . "$BACKEND_ROOT/.venv/bin/activate"
elif [ -f "$BACKEND_ROOT/venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  . "$BACKEND_ROOT/venv/bin/activate"
else
  echo "Backend virtual environment not found. Create backend/.venv first." >&2
  exit 1
fi

cd "$BACKEND_ROOT"
exec python -m speech_service.main
