#!/usr/bin/env python3
"""
Development startup script for VoIP Tracer
Starts both backend and frontend in development mode
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting VoIP Tracer Backend...")
    
    # Change to project root directory
    os.chdir(Path(__file__).parent)
    
    try:
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped")
        return True

def run_frontend():
    """Start the React frontend development server"""
    print("🎨 Starting VoIP Tracer Frontend...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Start Vite development server
        subprocess.run([
            "npm", "run", "dev"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend failed to start: {e}")
        return False
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")
        return True

def main():
    """Main startup function"""
    print("🔧 VoIP Tracer Development Environment")
    print("=" * 50)
    
    # Check if running from correct directory
    if not Path("src/api.py").exists():
        print("❌ Please run this script from the VoIP Tracer root directory")
        sys.exit(1)
    
    # Check if frontend directory exists
    if not Path("frontend").exists():
        print("❌ Frontend directory not found")
        sys.exit(1)
    
    print("\nStarting services...")
    print("• Backend will be available at: http://localhost:8000")
    print("• Frontend will be available at: http://localhost:5173")
    print("• API documentation at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both services\n")
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Give backend time to start
        time.sleep(3)
        
        # Start frontend (this will block until interrupted)
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down VoIP Tracer development environment...")
        
    print("✅ Development environment stopped")

if __name__ == "__main__":
    main()
