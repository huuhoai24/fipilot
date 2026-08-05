FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/app \
    HF_HOME=/home/app/.cache/huggingface \
    HF_HUB_DISABLE_XET=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        ffmpeg \
        libgomp1 \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-speech.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir \
        --index-url https://download.pytorch.org/whl/cpu \
        "torch>=2.5,<2.12" \
        "torchaudio>=2.5,<2.12" \
    && python -m pip install --no-cache-dir -r requirements-speech.txt \
    && python -m pip check

COPY scripts/cache_speech_models.py /tmp/cache_speech_models.py
RUN python /tmp/cache_speech_models.py \
        --stt-model small \
        --stt-output-dir /opt/fipilot/models/faster-whisper-small \
    && rm /tmp/cache_speech_models.py

ENV STT_MODEL=/opt/fipilot/models/faster-whisper-small \
    HF_HUB_OFFLINE=1

RUN addgroup --system app \
    && adduser --system --ingroup app --home /home/app app \
    && mkdir -p /home/app/.cache/huggingface

COPY app ./app
COPY core ./core
COPY gateway ./gateway
COPY infrastructure ./infrastructure
COPY orchestrator ./orchestrator
COPY services ./services
COPY shared ./shared
COPY scripts ./scripts
COPY crud.py database.py main.py models.py ./

RUN chown -R app:app /app /home/app

USER app

EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --log-level warning --no-access-log"]
