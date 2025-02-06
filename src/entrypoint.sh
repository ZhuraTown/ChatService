#!/bin/bash
echo "Start Applying migrations"
alembic upgrade head

echo "create default chat"
python manage.py create-first-chat

echo "Start service"
gunicorn main:app --workers ${API_WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${API_PORT}

exec "$@"
