FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN addgroup --system app \
    && adduser --system --ingroup app --home /home/app app

COPY app ./app
COPY core ./core
COPY gateway ./gateway
COPY infrastructure ./infrastructure
COPY orchestrator ./orchestrator
COPY services ./services
COPY shared ./shared
COPY crud.py database.py main.py models.py ./

RUN chown -R app:app /app

USER app

EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080} --log-level warning --no-access-log"]
