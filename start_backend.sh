#!/bin/bash

# ====================================================================
# Start Backend Server (macOS/Linux)
# ====================================================================

echo ""
echo "Starting YouTube Downloader Backend..."
echo ""

cd "$(dirname "$0")/backend"

# Activate virtual environment
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Start the server
echo "Backend server starting on http://127.0.0.1:8000"
echo ""
uvicorn main:app --reload --host 127.0.0.1 --port 8000
