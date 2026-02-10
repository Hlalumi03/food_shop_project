# Food Shop - Multi-Service Launcher (PowerShell)

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   FOOD SHOP - Starting All Services" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Run the Python launcher
Write-Host "Starting services on different ports..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Frontend:  http://localhost:3000/index.html" -ForegroundColor Green
Write-Host "API:       http://localhost:8001" -ForegroundColor Green
Write-Host "API Docs:  http://localhost:8001/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop all services." -ForegroundColor Yellow
Write-Host ""

python run.py
