#!/bin/bash
set -e
# Wait for DB to be ready
host="${DB_HOST:-db}"
port="${DB_PORT:-5432}"

echo "Waiting for PostgreSQL at $host:$port..."
until nc -z -v -w30 "$host" "$port"
do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up! Running migrations..."
python manage.py migrate --no-input

echo "Attempting to create superuser if not exists..."
cat <<EOF | python manage.py shell
import os
import sys
from django.conf import settings
from django.contrib.auth import get_user_model
from store.models import City

User = get_user_model()

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "")
last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "")
role = os.environ.get("DJANGO_SUPERUSER_ROLE", "")

if not all([email, password, first_name, last_name, role]):
    print("Missing required environment variables for superuser (email, password, first_name, last_name).")
    sys.exit(1)

# Check if user exists
if not User.objects.filter(email=email).exists():
    try:
        user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_superuser=True,
            is_staff=True
        )
        print(f"Superuser {email} created successfully.")
    except Exception as e:
        print(f"Error creating superuser: {e}")
else:
    print(f"Superuser {email} already exists. Skipping creation.")
EOF

echo "Starting Gunicorn..."
exec gunicorn warehouse.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 2
