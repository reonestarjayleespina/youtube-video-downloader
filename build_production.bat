@echo off
REM ====================================================================
REM Build for Production (Windows)
REM ====================================================================

echo.
echo ========================================
echo Building YouTube Downloader for Production
echo ========================================
echo.

REM Navigate to frontend folder
cd /d "%~dp0frontend"

echo [1/2] Building Frontend...
echo.

REM Build frontend
call npm run build

if errorlevel 1 (
    echo ERROR: Frontend build failed
    pause
    exit /b 1
)

echo.
echo [1/2] Frontend build complete
echo Output: frontend/dist/
echo.

echo [2/2] Production ready!
echo.
echo Backend: Ensure backend/main.py has:
echo   app = FastAPI()
echo   from fastapi.staticfiles import StaticFiles
echo   app.mount("/", StaticFiles(directory="frontend/dist", html=True))
echo.
echo To run in production:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --host 0.0.0.0 --port 8000
echo.
pause
