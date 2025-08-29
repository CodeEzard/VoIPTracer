#!/usr/bin/env python3
"""
Simple status check for VoIP Tracer services
"""

import requests
import sys

def check_services():
    """Check if both frontend and backend are accessible"""
    
    print("🔍 VoIP Tracer Status Check")
    print("=" * 40)
    
    # Check backend
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Backend: RUNNING (http://localhost:8000)")
            print(f"   Status: {response.json()}")
        else:
            print(f"❌ Backend: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend: NOT ACCESSIBLE")
        print(f"   Error: {e}")
        return False
    
    # Check demo endpoint
    try:
        response = requests.get('http://localhost:8000/demo', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Demo Endpoint: WORKING")
            print(f"   Calls: {len(data.get('calls', []))}")
            print(f"   Stats: {data.get('stats', {})}")
        else:
            print(f"❌ Demo Endpoint: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Demo Endpoint: FAILED")
        print(f"   Error: {e}")
    
    # Check frontend accessibility (simple check)
    try:
        response = requests.get('http://localhost:5173/', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend: ACCESSIBLE (http://localhost:5173)")
        else:
            print(f"❌ Frontend: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: NOT ACCESSIBLE")
        print(f"   Error: {e}")
    
    print("\n🎯 Access URLs:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    check_services()
