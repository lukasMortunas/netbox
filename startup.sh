#!/bin/bash
set -e

echo "Starting NetBox deployment..."

cd /home/site/wwwroot

# Copy example config to configuration.py if it doesn't exist
if [ ! -f netbox/netbox/configuration.py ]; then
    echo "Creating configuration.py from example..."
    cp netbox/netbox/configuration.py.example netbox/netbox/configuration.py
fi

echo "Running migrations..."
cd netbox
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating cache table..."
python manage.py createcachetable 2>/dev/null || true

echo "Starting gunicorn..."
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 60 netbox.wsgi:application
