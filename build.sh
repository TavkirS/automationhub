#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create database directory if it doesn't exist
mkdir -p data

# Run migrations
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput 