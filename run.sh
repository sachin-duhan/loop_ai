#! /bin/bash
set -e

PYTHONPATH="/app" python3 /app/app/scripts/create_db.py
PYTHONPATH="/app" python3 /app/app/main.py