@echo off
REM ====================================================================
REM Start Frontend Development Server (Windows)
REM ====================================================================

echo.
echo Starting YouTube Downloader Frontend...
echo.

cd /d "%~dp0frontend"

echo Frontend dev server starting on http://127.0.0.1:5173
echo.
npm run dev
