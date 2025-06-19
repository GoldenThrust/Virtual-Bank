#!/bin/bash

set -e

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
echo "Applying database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Ensure staticfiles directory exists and run collectstatic again
echo "Ensuring staticfiles directory exists and collecting static files..."
mkdir -p /app/api/staticfiles
python manage.py collectstatic --noinput --clear

# Create superuser if DJANGO_SUPERUSER_* environment variables are set
if [[ -n "${DJANGO_SUPERUSER_USERNAME}" && -n "${DJANGO_SUPERUSER_PASSWORD}" && -n "${DJANGO_SUPERUSER_EMAIL}" ]]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || true
fi

# Execute the command passed to docker run
exec "$@"
