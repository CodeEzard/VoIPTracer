#!/usr/bin/env python3
"""
Test script to verify VoIP Tracer frontend-backend connectivity
"""

import requests
import time

def test_backend():
    """Test backend API directly"""
    print("🔧 Testing Backend API...")
    try:
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: PASSED")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend health check: FAILED (Connection refused)")
        print("   Make sure backend is running: python -m uvicorn src.api:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Backend health check: FAILED ({e})")
        return False

def test_demo_endpoint():
    """Test demo endpoint"""
    print("\n🧪 Testing Demo Endpoint...")
    try:
        response = requests.get('http://localhost:8000/demo', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Demo endpoint: PASSED")
            print(f"   Calls found: {len(data.get('calls', []))}")
            print(f"   Stats: {data.get('stats', {})}")
            return True
        else:
            print(f"❌ Demo endpoint: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Demo endpoint: FAILED ({e})")
        return False

def test_frontend():
    """Test frontend accessibility"""
    print("\n🎨 Testing Frontend...")
    try:
        response = requests.get('http://localhost:5173/', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessibility: PASSED")
            print(f"   Content length: {len(response.text)} bytes")
            if 'VoIP Meta Tracer' in response.text:
                print("✅ Frontend content: Valid HTML with title")
            else:
                print("⚠️  Frontend content: HTML received but title not found")
            return True
        else:
            print(f"❌ Frontend accessibility: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend accessibility: FAILED (Connection refused)")
        print("   Make sure frontend is running: cd frontend && npm run dev")
        return False
    except Exception as e:
        print(f"❌ Frontend accessibility: FAILED ({e})")
        return False

def test_proxy():
    """Test frontend proxy to backend"""
    print("\n🔗 Testing Frontend Proxy...")
    try:
        response = requests.get('http://localhost:5173/api/', timeout=5)
        if response.status_code == 200:
            print("✅ Frontend proxy: PASSED")
            print(f"   Proxy response: {response.json()}")
            return True
        else:
            print(f"❌ Frontend proxy: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Frontend proxy: FAILED ({e})")
        print("   This might be normal if Vite proxy isn't configured for GET requests")
        return False

def main():
    print("🚀 VoIP Tracer Connectivity Test")
    print("=" * 50)
    
    tests = [
        test_backend,
        test_demo_endpoint,
        test_frontend,
        test_proxy,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    if passed == total:
        print("🎉 All tests passed! Your VoIP Tracer is ready to use.")
        print("\n📱 Access your application:")
        print("   Frontend: http://localhost:5173")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
        if not results[0]:  # Backend failed
            print("\n🔧 To start backend:")
            print("   python -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload")
            
        if not results[2]:  # Frontend failed
            print("\n🎨 To start frontend:")
            print("   cd frontend")
            print("   npm run dev")

if __name__ == "__main__":
    main()
