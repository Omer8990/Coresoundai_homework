#!/bin/bash
set -e

# Connect to the default 'postgres' database and create the 'airflow' database
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE airflow;"


