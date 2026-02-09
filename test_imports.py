#!/usr/bin/env python
import sys
sys.path.insert(0, r'c:\Users\sabas\Desktop\FOOD')

try:
    from app.models import Food, Order, Payment
    print("Models imported successfully")
    
    from app.schemas import PaymentCreate, PaymentResponse
    print("Payment schemas imported successfully")
    
    from app.services import PaymentService
    print("Payment service imported successfully")
    
    from main import app
    print("Main app imported successfully")
    
    print("\nAll imports successful!")
    print(f"App title: {app.title}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
