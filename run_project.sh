# Stop everything and clean up
docker-compose down -v

# Start everything up again
docker-compose up -d

# Wait for postgres to be ready (about 10-15 seconds)
sleep 15

# Run your API migrations
docker-compose exec api alembic upgrade head

# Start the rest of the services
docker-compose up -d

# Initialize Airflow DB
docker-compose exec airflow-webserver airflow db init

# Create Airflow user
docker-compose exec airflow-webserver airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
