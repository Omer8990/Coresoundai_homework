FROM python:3.9-slim

# Change working directory to include the api folder
WORKDIR /app/api

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy files maintaining the correct structure
COPY api/app ./app
COPY db /app/db
COPY worker/app/tasks.py /app/worker/app/tasks.py
COPY alembic.ini /app/
COPY alembic /app/alembic

RUN mkdir -p /app/uploads /app/processed

# Set PYTHONPATH to include both /app and /app/api
ENV PYTHONPATH=/app:/app/api

# Change working directory to /app/api where our app module is located
WORKDIR /app/api

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
