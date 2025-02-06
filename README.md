# Coresoundai_homework
Home Assginment: Image Processing API with Celery, Redis, and Airflow


# Distributed Image Processing System

A scalable system for batch processing images using FastAPI, Celery, Redis, and PostgreSQL, orchestrated with Apache Airflow.

## Project Structure

```
.
├── README.md
├── docker-compose.yml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       └── routes.py
├── worker/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── tasks.py
│       └── celery_app.py
├── db/
│   ├── __init__.py
│   ├── models.py
│   └── database.py
└── dags/
    └── image_processing_dag.py
```

## Features

- Batch image processing API
- Asynchronous task processing with Celery
- Redis message queue
- PostgreSQL database for task tracking
- Airflow DAG for orchestration
- Docker containerization
- Database migrations with Alembic

## Prerequisites

- Docker & Docker Compose
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Git

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Omer8990/Coresoundai_homework.git
   cd coresoundai_homework
   ```

2. Create environment files:
```bash
cp .env.example .env
```

3. Start the services:
```bash
docker-compose up -d
```

4. Run database migrations:
```bash
docker-compose exec api alembic upgrade head
```

5. Initialize Airflow:
```bash
docker-compose exec airflow-webserver airflow db init
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

 ```

## Services

- FastAPI: http://localhost:8000
- Airflow: http://localhost:8080
- PostgreSQL: http://localhost:5432
- Redis: http://localhost:6379

## API Endpoints

### POST /submit_batch
Submit a batch of images for processing.

```bash
curl -X POST http://localhost:8000/submit_batch \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

### GET /status/{image_id}
Check the status of a processed image.

```bash
curl http://localhost:8000/status/123e4567-e89b-12d3-a456-426614174000
```

## Development

### Running Tests
```bash
docker-compose exec api pytest
```

### Database Migrations
```bash
# Create a new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec api alembic upgrade head
```

## Monitoring

- Celery tasks: Check worker logs
  ```bash
  docker-compose logs -f worker
  ```
- Airflow DAGs: Access the Airflow UI at http://localhost:8080

## Troubleshooting

1. If services fail to start:
   - Check logs: `docker-compose logs <service_name>`
   - Ensure all ports are available
   - Verify environment variables in .env

2. If tasks aren't processing:
   - Check Redis connection
   - Verify Celery worker is running
   - Check worker logs for errors
