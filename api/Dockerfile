FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/app /app/api
COPY db /app/db
COPY worker/app/tasks.py /app/worker/app/tasks.py
COPY alembic.ini /app/
COPY alembic /app/alembic

RUN mkdir -p /app/uploads /app/processed

ENV PYTHONPATH=/app/api

WORKDIR /app

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
