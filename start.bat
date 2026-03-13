@echo off
title Security Toolkit Launcher
color 0A

echo ==========================================
echo    SECURITY TOOLKIT LAUNCHER
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

:: Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found! Please install Node.js 18+ from nodejs.org
    pause
    exit /b 1
)

echo [OK] Python and Node.js detected
echo.

:: Setup backend if needed
if not exist "api\venv" (
    echo [1/5] Setting up Python virtual environment...
    cd api
    python -m venv venv
    cd ..
)

:: Activate and install backend dependencies
echo [2/5] Installing backend dependencies...
cd api
call venv\Scripts\activate
pip install -q -r requirements.txt
cd ..

:: Setup frontend if needed
if not exist "frontend\node_modules" (
    echo [3/5] Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

:: Start backend in new window
echo [4/5] Starting backend server...
start "Security Toolkit API" cmd /k "cd api && call venv\Scripts\activate && uvicorn main:app --reload --port 8000"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend in new window  
echo [5/5] Starting frontend server...
start "Security Toolkit UI" cmd /k "cd frontend && npm run dev"

:: Open browser automatically
echo.
echo [OK] Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:5173

echo.
echo ==========================================
echo    ALL SYSTEMS RUNNING
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close the two command windows to stop.
echo.
pause