"""
Multi-service launcher for the Food Shop application.
Starts Frontend, API, and Backend on different ports.
"""
import subprocess
import time
import sys
import os
from pathlib import Path

# Configuration
FRONTEND_PORT = 3000
API_PORT = 8001
BACKEND_HOST = "127.0.0.1"

# Colors for console output (disabled on Windows)
USE_COLORS = sys.platform != "win32"

class Colors:
    HEADER = '\033[95m' if USE_COLORS else ''
    OKBLUE = '\033[94m' if USE_COLORS else ''
    OKCYAN = '\033[96m' if USE_COLORS else ''
    OKGREEN = '\033[92m' if USE_COLORS else ''
    WARNING = '\033[93m' if USE_COLORS else ''
    FAIL = '\033[91m' if USE_COLORS else ''
    ENDC = '\033[0m' if USE_COLORS else ''
    BOLD = '\033[1m' if USE_COLORS else ''
    UNDERLINE = '\033[4m' if USE_COLORS else ''

def print_header(message):
    """Print header message."""
    print(f"\n{Colors.BOLD}{Colors.OKBLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}{message}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKBLUE}{'='*60}{Colors.ENDC}\n")

def print_success(message):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def check_port_available(port):
    """Check if a port is available."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

def start_api_server():
    """Start the FastAPI server."""
    print_info(f"Starting API server on http://{BACKEND_HOST}:{API_PORT}...")
    
    if not check_port_available(API_PORT):
        print_warning(f"Port {API_PORT} is already in use. Trying to use it anyway...")
    
    try:
        cmd = [
            sys.executable,
            "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", BACKEND_HOST,
            "--port", str(API_PORT)
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print_success(f"API server starting on port {API_PORT}")
        return process
    except Exception as e:
        print_error(f"Failed to start API server: {e}")
        return None

def start_frontend_server():
    """Start a simple HTTP server for the frontend."""
    print_info(f"Starting Frontend server on http://localhost:{FRONTEND_PORT}...")
    
    if not check_port_available(FRONTEND_PORT):
        print_warning(f"Port {FRONTEND_PORT} is already in use. Trying to use it anyway...")
    
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        cmd = [
            sys.executable,
            "-m", "http.server",
            str(FRONTEND_PORT),
            "--bind", "127.0.0.1"
        ]
        
        process = subprocess.Popen(
            cmd,
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print_success(f"Frontend server starting on port {FRONTEND_PORT}")
        return process
    except Exception as e:
        print_error(f"Failed to start Frontend server: {e}")
        return None

def initialize_database():
    """Initialize the database with sample data."""
    print_info("Initializing database...")
    
    try:
        from app.core.database import create_tables, SessionLocal
        from app.models.food import Food
        
        # Create tables
        create_tables()
        print_success("Database tables created")
        
        # Check if we need to seed data
        db = SessionLocal()
        existing_count = db.query(Food).count()
        db.close()
        
        if existing_count == 0:
            print_info("Seeding database with sample foods...")
            # Import and run the seed function
            from seed_foods import seed_foods
            seed_foods()
        else:
            print_success(f"Database already has {existing_count} food items")
            
    except Exception as e:
        print_error(f"Failed to initialize database: {e}")

def display_startup_info():
    """Display startup information."""
    print_header("🍔 FOOD SHOP - MULTI-SERVICE LAUNCHER")
    
    print(f"{Colors.BOLD}Service URLs:{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}Frontend:{Colors.ENDC}  http://localhost:{FRONTEND_PORT}/index.html")
    print(f"  {Colors.OKGREEN}API:{Colors.ENDC}       http://{BACKEND_HOST}:{API_PORT}")
    print(f"  {Colors.OKGREEN}API Docs:{Colors.ENDC}  http://{BACKEND_HOST}:{API_PORT}/docs")
    print(f"  {Colors.OKGREEN}Database:{Colors.ENDC}  ./food_shop.db\n")
    
    print(f"{Colors.BOLD}Features:{Colors.ENDC}")
    print(f"  ✓ Frontend serving static files")
    print(f"  ✓ FastAPI with auto-reload")
    print(f"  ✓ SQLite Database")
    print(f"  ✓ CORS enabled for all origins\n")
    
    print(f"{Colors.BOLD}How to Stop:{Colors.ENDC}")
    print(f"  Press Ctrl+C to stop all services\n")

def main():
    """Main launcher function."""
    display_startup_info()
    
    # Initialize database first
    print_header("STEP 1: Initialize Backend")
    initialize_database()
    
    # Wait a moment
    time.sleep(1)
    
    # Start services
    print_header("STEP 2: Start Services")
    
    processes = []
    
    # Start API server
    api_process = start_api_server()
    if api_process:
        processes.append(api_process)
        time.sleep(2)  # Give API time to start
    
    # Start Frontend server
    frontend_process = start_frontend_server()
    if frontend_process:
        processes.append(frontend_process)
        time.sleep(1)
    
    if not processes:
        print_error("No services could be started!")
        sys.exit(1)
    
    print_header("✨ All Services Started Successfully!")
    
    print(f"\n{Colors.BOLD}Ready to use:{Colors.ENDC}")
    print(f"  1. Open {Colors.OKGREEN}http://localhost:{FRONTEND_PORT}/index.html{Colors.ENDC} in your browser")
    print(f"  2. Browse the menu and place orders")
    print(f"  3. API docs: {Colors.OKGREEN}http://{BACKEND_HOST}:{API_PORT}/docs{Colors.ENDC}\n")
    
    print(f"{Colors.WARNING}Note: The frontend will need to make requests to the API.{Colors.ENDC}")
    print(f"{Colors.WARNING}The frontend is configured to use: http://localhost:{API_PORT}/api/v1{Colors.ENDC}\n")
    
    # Keep processes running
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        print_header("Shutting Down Services")
        print_info("Terminating all processes...")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print_success("Process terminated")
            except subprocess.TimeoutExpired:
                print_warning("Process did not terminate, killing...")
                process.kill()
            except Exception as e:
                print_error(f"Error terminating process: {e}")
        
        print_success("All services stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
