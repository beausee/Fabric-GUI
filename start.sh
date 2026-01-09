#!/bin/bash

# Fabric GUI Startup Script

echo "🚀 Starting Fabric GUI..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if fabric is installed
if ! command -v fabric &> /dev/null && [ ! -f ~/go/bin/fabric ]; then
    echo "⚠️  Warning: fabric command not found!"
    echo "Please install fabric: go install github.com/danielmiessler/fabric@latest"
    echo "Or ensure it's in your PATH"
fi

echo "✓ Starting FastAPI server on http://127.0.0.1:8000"
echo "✓ Press Ctrl+C to stop"
echo ""

uvicorn main:app --host 127.0.0.1 --port 8000
