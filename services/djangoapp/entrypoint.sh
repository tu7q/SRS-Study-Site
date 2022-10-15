#!/bin/sh

set -e

cd web

# collect the static files.
python3 manage.py collectstatic --noinput
# run gunicorn webserver
gunicorn -c ./WebApp/gunicorn.py WebApp.wsgi
