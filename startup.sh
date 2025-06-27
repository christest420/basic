#!/bin/bash

echo "🚀 Starter installasjon av dependencies..." >&2
pip install -r requirements.txt >&2

echo "✅ Dependencies installert, starter app..." >&2
gunicorn --bind=0.0.0.0:8000 api:app
