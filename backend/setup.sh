#!/bin/bash
# Backend Setup Script

echo "🔧 Setting up backend..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
