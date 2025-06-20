#!/bin/bash
set -e

echo "⚙️ Running preflight check..."
python3 -m compileall main.py triage_model.py dispatch.py blockchain_access.py

echo "🚀 Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8080
