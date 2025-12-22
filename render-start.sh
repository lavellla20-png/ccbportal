#!/usr/bin/env bash
# Render.com start script

set -o errexit  # Exit on error

echo "=== Starting Django Application ==="

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn ccb_portal_backend.wsgi:application --bind 0.0.0.0:$PORT

