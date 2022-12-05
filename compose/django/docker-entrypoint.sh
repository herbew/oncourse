#!/bin/sh
# Migrate the database first
export DJANGO_SETTINGS_MODULE="config.settings.production" &
python3 manage.py collectstatic --no-input &
python3 manage.py migrate sites & 

python3 manage.py collectstatic --noinput

python3 manage.py loaddata 001001_user & 
python3 manage.py runserver 0.0.0.0:9999 &

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 
    
