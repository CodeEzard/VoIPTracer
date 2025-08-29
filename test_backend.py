#!/usr/bin/env python3
"""
Test the fixed backend
"""
import requests

try:
    print("Testing backend on port 8001...")
    response = requests.get('http://localhost:8001/', timeout=5)
    print(f"Health check: {response.status_code} - {response.json()}")
    
    print("\nTesting demo endpoint...")
    response = requests.get('http://localhost:8001/demo', timeout=10)
    print(f"Demo status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Demo response keys: {list(data.keys())}")
        if 'calls' in data:
            print(f"Number of calls: {len(data['calls'])}")
        if 'stats' in data:
            print(f"Stats: {data['stats']}")
        print("✅ Backend is working correctly!")
    else:
        print(f"❌ Demo failed: {response.text}")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
