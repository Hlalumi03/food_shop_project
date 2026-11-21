#!/bin/bash
# Food Shop - Single-Server Launcher (Linux/Mac)

echo ""
echo "========================================================"
echo "   FOOD SHOP - Starting All Services"
echo "========================================================"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run the Python launcher
echo "Starting the frontend and API on one server..."
echo ""
echo "Frontend:  http://127.0.0.1:8001/"
echo "API:       http://127.0.0.1:8001/api/v1"
echo "API Docs:  http://127.0.0.1:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services."
echo ""

python run.py
