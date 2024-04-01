#!/bin/ash

echo  "Running successfully"
python manage.py runserver

exec "$@"