#!/bin/bash

pip freeze >  requirements.txt

echo "Uvmowa@2024" | sudo -S systemctl stop redis

celery -A src.celery_worker control shutdown

kill -9 $(lsof -i :8000)

# curl -X 'POST' 'http://127.0.0.1:8000/upload/'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'file=@data/data.csv'