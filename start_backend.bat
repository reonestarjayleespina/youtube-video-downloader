@echo off
REM ====================================================================
REM Start Backend Server (Windows)
REM ====================================================================

echo.
echo Starting YouTube Downloader Backend...
echo.

cd /d "%~dp0backend"

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

REM Start the server
echo Backend server starting on http://127.0.0.1:8000
echo.
uvicorn main:app --reload --host 127.0.0.1 --port 8000
