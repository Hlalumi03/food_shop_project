# Food Shop - Single-Server Launcher (PowerShell)

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   FOOD SHOP - Starting All Services" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Run the Python launcher
Write-Host "Starting the frontend and API on one server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Frontend:  http://127.0.0.1:8001/" -ForegroundColor Green
Write-Host "API:       http://127.0.0.1:8001/api/v1" -ForegroundColor Green
Write-Host "API Docs:  http://127.0.0.1:8001/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop all services." -ForegroundColor Yellow
Write-Host ""

python run.py
