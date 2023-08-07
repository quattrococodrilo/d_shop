#!/usr/bin/env bash

if [ ! -d "/code/venv" ]; then
    python3.11 -m venv venv
fi

venv/bin/pip install --no-cache-dir -r requirements.txt

export PYTHONPATH="${PYTHONPATH}:/code/venv"

/wait-for-it.sh -t 0 $DB_HOST:$DB_PORT --strict -- venv/bin/python manage.py runserver 0.0.0.0:8000
