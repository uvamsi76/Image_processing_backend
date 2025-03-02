#!/bin/bash

VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists."
else
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created successfully."
fi

source $VENV_DIR/bin/activate

pip install -r requirements.txt

echo "Uvmowa@2024" | sudo -S apt install redis-server -y

nohup redis-server > logs/redis.log 2>&1 &

nohup celery -A src.celery_worker worker --loglevel=info > logs/celery.log 2>&1 &

nohup uvicorn src.main:app --reload > logs/backend.log 2>&1 &