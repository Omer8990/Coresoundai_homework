FROM python:3.9-slim

# Set working directory to /app (not /app/api)
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files properly
COPY api/app /app
COPY db /app/db
COPY worker/app/tasks.py /app/worker/app/tasks.py
COPY alembic.ini /app/
COPY alembic /app/alembic

# Create necessary directories
RUN mkdir -p /app/uploads /app/processed

# Set correct PYTHONPATH
ENV PYTHONPATH=/app

# Use the correct working directory
WORKDIR /app

# Run Uvicorn with correct path
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
