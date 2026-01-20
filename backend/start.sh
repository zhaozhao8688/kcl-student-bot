#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Starting FastAPI app (simple test version)..."
exec python main_simple.py
