#!/bin/bash

# Activate Python virtual environment for dependency isolation
source /opt/venv/bin/activate

# Go into code folder
cd /code

# Set runtime variables
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

# Run application
gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app
