#!/usr/bin/env python
import time
time.sleep(2)
print("Testing API...")

import requests
try:
    r = requests.get('http://localhost:8001/api/v1/foods', timeout=5)
    print(f'Status: {r.status_code}')
    data = r.json()
    print(f'Foods: {len(data)}')
    print('SUCCESS!')
except Exception as e:
    print(f'FAILED: {e}')
