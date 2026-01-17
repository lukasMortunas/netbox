#!/bin/bash
set -e

cd netbox

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start gunicorn
echo "Starting gunicorn..."
gunicorn netbox.wsgi --config ../contrib/gunicorn.py
