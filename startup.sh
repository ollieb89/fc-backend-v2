#!/bin/bash
# startup.sh is used by infra/resources.bicep to automate database migrations and isn't used by the sample application

echo "Starting database migrations..."
python manage.py migrate

python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn --workers 2 --threads 4 --timeout 60 \
         --access-logfile '-' --error-logfile '-' \
         --bind=0.0.0.0:8000 \
         --chdir=/home/site/wwwroot fc_backend_v2.wsgi
