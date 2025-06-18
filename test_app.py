#!/usr/bin/env python3
"""
Test script for the Escrow System web application
"""

import requests
import json
import time
import sys

def test_server_connection():
    """Test if the server is running"""
    try:
        response = requests.get('http://localhost:8080/', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responding")
            return True
        else:
            print(f"❌ Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on port 8080")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def test_create_room():
    """Test room creation functionality"""
    try:
        data = {
            'username': 'test_seller',
            'amount': 100000,
            'privilege': 'penjual'
        }
        response = requests.post('http://localhost:8080/create_room', 
                               json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print("✅ Room creation test passed")
                return result['uuid']
            else:
                print(f"❌ Room creation failed: {result['message']}")
                return None
        else:
            print(f"❌ Room creation request failed with status: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error testing room creation: {e}")
        return None

def test_join_room(room_uuid):
    """Test room joining functionality"""
    try:
        data = {
            'uuid': room_uuid,
            'username': 'test_buyer',
            'privilege': 'pembeli'
        }
        response = requests.post('http://localhost:8080/join_room', 
                               json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print("✅ Room joining test passed")
                return True
            else:
                print(f"❌ Room joining failed: {result['message']}")
                return False
        else:
            print(f"❌ Room joining request failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing room joining: {e}")
        return False

def test_get_messages(room_uuid):
    """Test message retrieval functionality"""
    try:
        data = {'uuid': room_uuid}
        response = requests.post('http://localhost:8080/get_message', 
                               json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print(f"✅ Message retrieval test passed (found {len(result['message'])} messages)")
                return True
            else:
                print(f"❌ Message retrieval failed: {result['message']}")
                return False
        else:
            print(f"❌ Message retrieval request failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing message retrieval: {e}")
        return False

def test_send_message(room_uuid):
    """Test message sending functionality"""
    try:
        data = {
            'uuid': room_uuid,
            'msg': '[TEST] This is a test message from the test script'
        }
        response = requests.post('http://localhost:8080/send_message', 
                               json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result['status'] == 'success':
                print("✅ Message sending test passed")
                return True
            else:
                print(f"❌ Message sending failed: {result['message']}")
                return False
        else:
            print(f"❌ Message sending request failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing message sending: {e}")
        return False

def test_qr_generation(room_uuid):
    """Test QR code generation"""
    try:
        response = requests.get(f'http://localhost:8080/generate_qr/{room_uuid}', 
                              timeout=10)
        
        if response.status_code == 200:
            # Check if it's an image response
            if 'image/png' in response.headers.get('Content-Type', ''):
                print("✅ QR code generation test passed")
                return True
            else:
                print("❌ QR code generation returned invalid content type")
                return False
        else:
            print(f"❌ QR code generation request failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing QR code generation: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Escrow System Web Application")
    print("=" * 50)
    
    # Test server connection
    if not test_server_connection():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python start.py")
        sys.exit(1)
    
    print("\n📋 Running functionality tests...")
    
    # Test room creation
    room_uuid = test_create_room()
    if not room_uuid:
        print("❌ Cannot proceed with tests without room creation")
        sys.exit(1)
    
    # Test room joining
    if not test_join_room(room_uuid):
        print("❌ Room joining test failed")
        sys.exit(1)
    
    # Test message retrieval
    if not test_get_messages(room_uuid):
        print("❌ Message retrieval test failed")
        sys.exit(1)
    
    # Test message sending
    if not test_send_message(room_uuid):
        print("❌ Message sending test failed")
        sys.exit(1)
    
    # Test QR code generation
    if not test_qr_generation(room_uuid):
        print("❌ QR code generation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! The application is working correctly.")
    print("🌐 You can now access the web interface at: http://localhost:8080")
    print("=" * 50)

if __name__ == "__main__":
    main() 