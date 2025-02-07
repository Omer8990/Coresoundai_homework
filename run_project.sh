#!/bin/bash

# Stop everything and clean up
docker-compose down -v

# Start only PostgreSQL first
docker-compose up -d postgres

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U user -h localhost; do
  sleep 2
done
echo "PostgreSQL is ready!"

# Start only the Airflow initialization container
docker-compose run --rm airflow-webserver airflow db init

# Now start all services
docker-compose up -d

# Wait for services to settle
sleep 5

# Run API migrations
docker-compose exec api alembic upgrade head

# Create Airflow user
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
