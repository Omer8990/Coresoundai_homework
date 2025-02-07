FROM python:3.9-slim

# Set working directory to /app
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app folder and related files
COPY api/app /app/api
COPY db /app/db
COPY worker/app/tasks.py /app/worker/app/tasks.py
COPY alembic.ini /app/
COPY alembic /app/alembic

# Create necessary directories
RUN mkdir -p /app/uploads /app/processed

# Set PYTHONPATH to include /app/api
ENV PYTHONPATH=/app/api

# Use the correct working directory
WORKDIR /app

# Run Uvicorn with correct path
CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
