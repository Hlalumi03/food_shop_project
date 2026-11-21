import requests
import sys

BASE_URL = "http://127.0.0.1:8001"

try:
    health_response = requests.get(f"{BASE_URL}/health", timeout=5)
    health_response.raise_for_status()
    print(f"Health check: {health_response.json()}")

    frontend_response = requests.get(f"{BASE_URL}/", timeout=5)
    frontend_response.raise_for_status()
    if "text/html" not in frontend_response.headers.get("content-type", ""):
        raise RuntimeError("The application root did not return the frontend HTML.")
    print("Frontend: served by the application")

    foods_response = requests.get(f"{BASE_URL}/api/v1/foods", timeout=5)
    foods_response.raise_for_status()
    foods = foods_response.json()
    if not isinstance(foods, list):
        raise RuntimeError("The foods API did not return a list.")
    print(f"Foods API: returned {len(foods)} foods")

    print("\nFrontend and API are available on the same server.")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
