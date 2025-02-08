#!/bin/bash

docker-compose down -v

docker-compose up -d postgres

echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U user -h localhost; do
  sleep 2
done
echo "PostgreSQL is ready!"

docker-compose run --rm airflow-webserver airflow db init

docker-compose up -d

sleep 5

docker-compose exec api alembic upgrade head

docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
