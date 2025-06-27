#!/bin/bash

echo "🚀 Starter installasjon av dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installert, starter app..."
gunicorn --bind=0.0.0.0:8000 api:app
