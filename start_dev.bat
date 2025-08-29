@echo off
echo Starting VoIP Tracer Development Environment...
echo.

REM Check if we're in the right directory
if not exist "src\api.py" (
    echo Error: Please run this script from the VoIP Tracer root directory
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo Error: Frontend directory not found
    pause
    exit /b 1
)

echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop services
echo.

REM Start backend in a new window
start "VoIP Tracer Backend" cmd /k "python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
cd frontend
npm run dev

echo.
echo Development environment stopped.
pause
