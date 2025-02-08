#!/bin/bash
set -e
psql -U "$POSTGRES_USER" -d postgres <<-EOSQL
  CREATE DATABASE airflow;
EOSQL
