# Security Toolkit Auto-Setup and Launch
$host.ui.RawUI.WindowTitle = "Security Toolkit Launcher"

Write-Host "==========================================" -ForegroundColor Green
Write-Host "   SECURITY TOOLKIT LAUNCHER" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
try {
    $py = python --version 2>&1
    Write-Host "[OK] $py" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found! Install from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

try {
    $node = node --version 2>&1
    Write-Host "[OK] Node.js $node" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js not found! Install from nodejs.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host ""

# Setup backend
if (-not (Test-Path "api\venv")) {
    Write-Host "[1/5] Creating Python virtual environment..." -ForegroundColor Cyan
    cd api
    python -m venv venv
    cd ..
}

Write-Host "[2/5] Installing backend dependencies..." -ForegroundColor Cyan
cd api
.\venv\Scripts\Activate.ps1
pip install -q -r requirements.txt
cd ..

# Setup frontend
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[3/5] Installing frontend dependencies..." -ForegroundColor Cyan
    cd frontend
    npm install
    cd ..
}

# Start backend
Write-Host "[4/5] Starting backend server..." -ForegroundColor Cyan
$backend = Start-Process powershell -ArgumentList "-Command cd api; .\venv\Scripts\Activate.ps1; uvicorn main:app --reload --port 8000" -PassThru

Start-Sleep -Seconds 3

# Start frontend
Write-Host "[5/5] Starting frontend server..." -ForegroundColor Cyan
$frontend = Start-Process powershell -ArgumentList "-Command cd frontend; npm run dev" -PassThru

# Open browser
Write-Host ""
Write-Host "[OK] Opening browser..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "   ALL SYSTEMS RUNNING!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Gray
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host ""
Write-Host "Close the backend and frontend windows to stop." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit this launcher"