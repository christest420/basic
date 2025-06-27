#!/bin/bash

echo "🚀 Starter installasjon av dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installert, starter app..."
exec gunicorn --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 api:app
