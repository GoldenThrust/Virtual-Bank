#!/bin/bash

set -e

# Wait for API service to be ready
echo "Waiting for API service..."
until curl -s http://api:8030/api/ > /dev/null 2>&1; do
  echo "API service is unavailable - sleeping"
  sleep 2
done

# Wait for database to be ready
echo "Waiting for database..."
python -c "
import sys
import psycopg2
import os
import time
host = os.environ.get('DB_HOST', 'db')
user = os.environ.get('DB_USER', 'postgres')
password = os.environ.get('DB_PASSWORD', 'postgres')
dbname = os.environ.get('DB_NAME', 'postgres')
port = os.environ.get('DB_PORT', '5432')

for i in range(30):  # Try for 30 seconds
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            port=port
        )
        conn.close()
        sys.exit(0)
    except psycopg2.OperationalError:
        time.sleep(1)
sys.exit(1)
"

# Apply database migrations
echo "Applying database migrations for client app..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if DJANGO_SUPERUSER_* environment variables are set
if [[ -n "${DJANGO_SUPERUSER_USERNAME}" && -n "${DJANGO_SUPERUSER_PASSWORD}" && -n "${DJANGO_SUPERUSER_EMAIL}" ]]; then
    echo "Creating superuser for client app..."
    python manage.py createsuperuser --noinput || true
fi

# Execute the command passed to docker run
exec "$@"
