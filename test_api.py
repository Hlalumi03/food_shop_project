import requests
import sys
import time

# Give server time to start
time.sleep(2)

try:
    # Test health check
    response = requests.get("http://localhost:8000/health")
    print(f"Health Check: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test root endpoint
    response = requests.get("http://localhost:8000/")
    print(f"\nRoot Endpoint: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n✅ API is running successfully!")
    sys.exit(0)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
