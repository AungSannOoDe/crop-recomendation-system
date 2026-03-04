#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Running Migrations ---"
python manage.py migrate --noinput

echo "--- Collecting Static Files ---"
python manage.py collectstatic --noinput

echo "--- Starting Gunicorn ---"
# Replace 'myproject' with the folder name containing your wsgi.py
exec gunicorn crop_recommendation.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120