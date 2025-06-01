#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations tools
python manage.py makemigrations quiz
python manage.py migrate tools --noinput
python manage.py migrate quiz --noinput
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput 