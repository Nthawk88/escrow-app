#!/usr/bin/env python3
"""
Escrow System Startup Script
This script provides a simple way to start the escrow system web application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        import flask_socketio
        import qrcode
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Install dependencies if needed"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_static_directory():
    """Create static directory if it doesn't exist"""
    static_dir = Path("static")
    if not static_dir.exists():
        static_dir.mkdir()
        print("📁 Created static directory")

def main():
    """Main startup function"""
    print("🚀 Starting Escrow System...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create static directory
    create_static_directory()
    
    # Check dependencies
    if not check_dependencies():
        print("\n🔧 Attempting to install dependencies...")
        if not install_dependencies():
            sys.exit(1)
        if not check_dependencies():
            sys.exit(1)
    
    print("\n🎯 Starting the application...")
    print("=" * 50)
    
    # Import and run the application
    try:
        from run import startFlask
        from config import Config
        
        print(f"🌐 Server will be available at: http://localhost:{Config.PORT}")
        print(f"🔧 Debug mode: {'Enabled' if Config.DEBUG else 'Disabled'}")
        print("=" * 50)
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        startFlask(Config.HOST, Config.PORT)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 