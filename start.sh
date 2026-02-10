#!/bin/bash
# Food Shop - Multi-Service Launcher (Linux/Mac)

echo ""
echo "========================================================"
echo "   FOOD SHOP - Starting All Services"
echo "========================================================"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Run the Python launcher
echo "Starting services on different ports..."
echo ""
echo "Frontend:  http://localhost:3000/index.html"
echo "API:       http://localhost:8001"
echo "API Docs:  http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

python run.py
