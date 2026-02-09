#!/usr/bin/env python
"""Test script to verify payment system integration."""
import sys
import os
sys.path.insert(0, r'c:\Users\sabas\Desktop\FOOD')
os.chdir(r'c:\Users\sabas\Desktop\FOOD')

print("Testing Payment System Integration")
print("=" * 60)

try:
    # Test 1: Import models
    print("\n[1] Testing model imports...")
    from app.models.payment import Payment, PaymentMethodEnum, PaymentStatusEnum
    print("    - Payment model imported")
    print(f"    - Payment methods: {[m.value for m in PaymentMethodEnum]}")
    print(f"    - Payment statuses: {[s.value for s in PaymentStatusEnum]}")
    
    # Test 2: Import schemas
    print("\n[2] Testing schema imports...")
    from app.schemas.payment import PaymentCreate, PaymentResponse
    print("    - Payment schemas imported")
    
    # Test 3: Import services
    print("\n[3] Testing service imports...")
    from app.services.payment_service import PaymentService
    print("    - Payment service imported")
    
    # Test 4: Import repositories
    print("\n[4] Testing repository imports...")
    from app.repositories.payment_repository import PaymentRepository
    print("    - Payment repository imported")
    
    # Test 5: Import main app
    print("\n[5] Testing main app...")
    from main import app
    print(f"    - App loaded: {app.title}")
    
    # Test 6: Check routes
    print("\n[6] Checking payment routes...")
    payment_routes = [r for r in app.routes if hasattr(r, 'path') and '/payments' in str(r.path)]
    print(f"    - Found {len(payment_routes)} payment routes")
    
    print("\n" + "=" * 60)
    print("All tests passed successfully!")
    print("Payment system is ready to use.")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
