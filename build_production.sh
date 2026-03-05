#!/bin/bash

# ====================================================================
# Build for Production (macOS/Linux)
# ====================================================================

echo ""
echo "========================================"
echo "Building YouTube Downloader for Production"
echo "========================================"
echo ""

# Navigate to frontend folder
cd "$(dirname "$0")/frontend"

echo "[1/2] Building Frontend..."
echo ""

# Build frontend
npm run build

if [ $? -ne 0 ]; then
    echo "ERROR: Frontend build failed"
    exit 1
fi

echo ""
echo "[1/2] Frontend build complete"
echo "Output: frontend/dist/"
echo ""

echo "[2/2] Production ready!"
echo ""
echo "Backend: Ensure backend/main.py has:"
echo "  app = FastAPI()"
echo "  from fastapi.staticfiles import StaticFiles"
echo "  app.mount(\"/\", StaticFiles(directory=\"frontend/dist\", html=True))"
echo ""
echo "To run in production:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
