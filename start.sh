#!/bin/bash

echo "🟣 Installing dependencies..."
pip install -r requirements/production_psg.txt 2>/dev/null || \
pip install -r requirements/production_msql.txt 2>/dev/null || \
pip install -r requirements/base.txt

echo "🟣 Running migrations..."
python manage.py migrate --noinput

echo "🟣 Starting Gunicorn server..."
gunicorn core.wsgi:application --bind 0.0.0.0:${PORT}
