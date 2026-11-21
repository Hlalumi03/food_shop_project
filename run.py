"""Start the Food Shop frontend and API from one FastAPI server."""
import subprocess
import sys

# Configuration
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
    print(f"{Colors.OKGREEN}[OK] {message}{Colors.ENDC}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.OKCYAN}[INFO] {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message."""
    print(f"{Colors.WARNING}[WARN] {message}{Colors.ENDC}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.FAIL}[ERROR] {message}{Colors.ENDC}")

def check_port_available(port):
    """Check if a port is available."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0

    
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
    print_header("FOOD SHOP")
    
    print(f"  Frontend:  http://{BACKEND_HOST}:{API_PORT}/")
    print(f"  API:       http://{BACKEND_HOST}:{API_PORT}/api/v1")
    print(f"  API docs:  http://{BACKEND_HOST}:{API_PORT}/docs")
    print(f"  Database:  ./food_shop.db\n")

def main():
    """Initialize the database and run the combined frontend/API server."""
    display_startup_info()
    initialize_database()

    if not check_port_available(API_PORT):
        print_warning(f"Port {API_PORT} is already in use.")
        sys.exit(1)

    print_info("Starting the combined frontend and API server...")
    process = subprocess.Popen([
        sys.executable,
        "-m", "uvicorn",
        "main:app",
        "--reload",
        "--host", BACKEND_HOST,
        "--port", str(API_PORT)
    ])

    try:
        return_code = process.wait()
        if return_code:
            print_error(f"Server exited with status {return_code}.")
        return return_code
    except KeyboardInterrupt:
        print_info("Stopping the server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        return 0

if __name__ == "__main__":
    sys.exit(main())
