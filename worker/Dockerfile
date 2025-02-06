FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY worker/app ./app
COPY db ./db

# Create upload and processed directories
RUN mkdir -p uploads processed

CMD ["celery", "-A", "app.tasks", "worker"]
