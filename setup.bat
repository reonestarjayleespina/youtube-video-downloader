@echo off
REM ====================================================================
REM YouTube Video Downloader - Setup Script for Windows
REM ====================================================================

echo.
echo ========================================
echo YouTube Video Downloader - Setup
echo ========================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg is not installed or not in PATH
    echo Audio/video merging may not work
    echo Install FFmpeg from https://ffmpeg.org/download.html
    echo.
)

echo.
echo [1/4] Setting up Backend...
echo.

REM Navigate to backend folder
cd /d "%~dp0backend"

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
echo Installing backend dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Setup Backend - COMPLETE
echo.

REM Navigate to frontend folder
cd /d "%~dp0frontend"

echo.
echo [3/4] Setting up Frontend...
echo.

REM Install frontend dependencies
echo Installing frontend dependencies...
call npm install

if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo [4/4] Setup Frontend - COMPLETE
echo.

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo Terminal 1 - Start Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --reload
echo.
echo Terminal 2 - Start Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://127.0.0.1:5173
echo.
pause
