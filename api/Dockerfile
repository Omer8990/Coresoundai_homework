FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api/app ./app
COPY db ./db
COPY worker/app/tasks.py ./worker/app/tasks.py

RUN mkdir -p uploads processed

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
