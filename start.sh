#!/bin/bash

echo "Starting HealthCore..."

# Activate venv
source venv/bin/activate

# Start Django
python manage.py runserver &
DJANGO_PID=$!
echo "Django started (PID: $DJANGO_PID)"

# Start Celery Worker
celery -A healthcore worker --loglevel=info --pool=solo &
WORKER_PID=$!
echo "Celery worker started (PID: $WORKER_PID)"

# Start Celery Beat
celery -A healthcore beat --loglevel=info &
BEAT_PID=$!
echo "Celery beat started (PID: $BEAT_PID)"

echo ""
echo "All backend services running!"
echo "Press Ctrl+C to stop everything"

# Stop all on Ctrl+C
trap "kill $DJANGO_PID $WORKER_PID $BEAT_PID; exit" INT
wait