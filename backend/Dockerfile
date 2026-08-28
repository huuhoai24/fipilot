FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends libglib2.0-0 libgomp1 libgl1 ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
COPY fipilot ./fipilot
COPY api ./api
COPY core ./core
COPY gateway ./gateway
COPY services ./services
COPY infrastructure ./infrastructure
COPY shared ./shared
COPY app ./app
COPY main.py ./main.py
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic
COPY Knowledge ./Knowledge
COPY models/best.onnx ./models/best.onnx

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
  && pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
