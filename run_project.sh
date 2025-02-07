#!/bin/bash

# Stop everything and clean up
docker-compose down -v

# Start only PostgreSQL first
docker-compose up -d postgres

# Wait for PostgreSQL to be ready (check using pg_isready)
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U user -h localhost; do
  sleep 2
done
echo "PostgreSQL is ready!"

# Now start the rest of the services
docker-compose up -d

# Wait a few more seconds to be extra safe
sleep 5

# Run your API migrations
docker-compose exec api alembic upgrade head

# Initialize Airflow DB (make sure database exists first!)
docker-compose exec postgres psql -U user -c "CREATE DATABASE airflow;" 2>/dev/null || echo "Database airflow already exists"
docker-compose exec airflow-webserver airflow db migrate

# Create Airflow user
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

docker-compose up -d
