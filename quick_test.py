#!/usr/bin/env python3
"""
Quick backend test
"""
import requests

try:
    response = requests.get('http://localhost:8000/', timeout=3)
    print(f"Backend Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✅ Backend is running successfully!")
except Exception as e:
    print(f"❌ Backend test failed: {e}")
