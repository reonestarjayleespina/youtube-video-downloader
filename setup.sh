#!/bin/bash

# ====================================================================
# YouTube Video Downloader - Setup Script for macOS/Linux
# ====================================================================

echo ""
echo "========================================"
echo "YouTube Video Downloader - Setup"
echo "========================================"
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Check Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "WARNING: FFmpeg is not installed"
    echo "Audio/video merging may not work"
    echo "Install FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Linux: sudo apt-get install ffmpeg"
    echo ""
fi

echo ""
echo "[1/4] Setting up Backend..."
echo ""

# Navigate to backend folder
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install backend dependencies"
    exit 1
fi

echo ""
echo "[2/4] Setup Backend - COMPLETE"
echo ""

# Navigate to frontend folder
cd ../frontend

echo ""
echo "[3/4] Setting up Frontend..."
echo ""

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install frontend dependencies"
    exit 1
fi

echo ""
echo "[4/4] Setup Frontend - COMPLETE"
echo ""

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "Terminal 1 - Start Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open: http://127.0.0.1:5173"
echo ""
