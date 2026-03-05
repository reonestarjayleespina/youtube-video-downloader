#!/bin/bash

# ====================================================================
# Start Frontend Development Server (macOS/Linux)
# ====================================================================

echo ""
echo "Starting YouTube Downloader Frontend..."
echo ""

cd "$(dirname "$0")/frontend"

echo "Frontend dev server starting on http://127.0.0.1:5173"
echo ""
npm run dev
