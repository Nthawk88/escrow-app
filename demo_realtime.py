#!/usr/bin/env python3
"""
Real-time Chat Demo Script
This script demonstrates the real-time functionality of the escrow system.
"""

import requests
import json
import time
import sys

def demo_realtime_chat():
    """Demonstrate real-time chat functionality"""
    print("🚀 Real-time Escrow Chat Demo")
    print("=" * 50)
    
    # Step 1: Create a room as seller
    print("1. Creating escrow room as seller...")
    seller_data = {
        'username': 'DemoSeller',
        'amount': 500000,
        'privilege': 'penjual'
    }
    
    response = requests.post('http://localhost:8080/create_room', json=seller_data)
    if response.status_code != 200:
        print("❌ Failed to create room")
        return
    
    room_data = response.json()
    room_uuid = room_data['uuid']
    print(f"✅ Room created: {room_uuid}")
    
    # Step 2: Join room as buyer
    print("\n2. Joining room as buyer...")
    buyer_data = {
        'uuid': room_uuid,
        'username': 'DemoBuyer',
        'privilege': 'pembeli'
    }
    
    response = requests.post('http://localhost:8080/join_room', json=buyer_data)
    if response.status_code != 200:
        print("❌ Failed to join room")
        return
    
    print("✅ Buyer joined room")
    
    # Step 3: Show initial messages
    print("\n3. Initial messages:")
    response = requests.post('http://localhost:8080/get_message', json={'uuid': room_uuid})
    messages = response.json()['message']
    
    for i, msg in enumerate(messages):
        print(f"   {i+1}. {msg[0]}")
    
    # Step 4: Simulate buyer confirming payment
    print("\n4. Buyer confirming payment...")
    payment_msg = '[Y][ADMIN SYSTEM] PEMBAYARAN TELAH DILAKUKAN OLEH PEMBELI'
    
    response = requests.post('http://localhost:8080/send_message', json={
        'uuid': room_uuid,
        'msg': payment_msg
    })
    
    if response.status_code == 200:
        print("✅ Payment confirmation sent")
    else:
        print("❌ Failed to send payment confirmation")
    
    # Step 5: Show updated messages
    print("\n5. Updated messages after payment confirmation:")
    time.sleep(1)  # Wait a moment for processing
    
    response = requests.post('http://localhost:8080/get_message', json={'uuid': room_uuid})
    messages = response.json()['message']
    
    for i, msg in enumerate(messages):
        print(f"   {i+1}. {msg[0]}")
    
    # Step 6: Simulate seller confirming receipt
    print("\n6. Seller confirming payment receipt...")
    receipt_msg = '[Y][ADMIN SYSTEM] PEMBAYARAN DIKONFIRMASI OLEH PENJUAL'
    
    response = requests.post('http://localhost:8080/send_message', json={
        'uuid': room_uuid,
        'msg': receipt_msg
    })
    
    if response.status_code == 200:
        print("✅ Payment receipt confirmation sent")
    else:
        print("❌ Failed to send receipt confirmation")
    
    # Step 7: Final message state
    print("\n7. Final message state:")
    time.sleep(1)
    
    response = requests.post('http://localhost:8080/get_message', json={'uuid': room_uuid})
    messages = response.json()['message']
    
    for i, msg in enumerate(messages):
        print(f"   {i+1}. {msg[0]}")
    
    print("\n" + "=" * 50)
    print("🎉 Real-time demo completed!")
    print("📱 Open http://localhost:8080 in your browser to see the web interface")
    print("🔗 Share the QR code or room UUID with others to test real-time chat")
    print("=" * 50)

if __name__ == "__main__":
    try:
        demo_realtime_chat()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        sys.exit(1) 