from flask import request, Response, jsonify, make_response, send_file, render_template_string, send_from_directory
from flask_socketio import emit, join_room, leave_room
from time import strftime, time
import os
from shutil import copyfile
from uuid import uuid4
from random import randint
from backend.dbquery import DBSQLite
import mysql.connector, io
from base64 import b64decode,b64encode
from zipfile import ZipFile
from datetime import datetime
from . import app, socketio
import qrcode
import json
from config import Config

# Serve the main HTML page
@app.route("/")
def index():
    # Get the absolute path to the static directory
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    return send_from_directory(static_dir, 'index.html')

@app.route("/create_room", methods=['POST'])
def create_room():
    data = request.get_json()
    
    # Validate input
    if not data.get('username') or not data.get('amount'):
        return jsonify({"status": "error", "message": "Username and amount are required"}), 400
    
    amount = int(data['amount'])
    if amount < Config.MIN_TRANSACTION_AMOUNT or amount > Config.MAX_TRANSACTION_AMOUNT:
        return jsonify({
            "status": "error", 
            "message": f"Amount must be between Rp.{Config.MIN_TRANSACTION_AMOUNT:,} and Rp.{Config.MAX_TRANSACTION_AMOUNT:,}"
        }), 400
    
    dbr = DBSQLite(Config.DATABASE_PATH)
    cursorObj = dbr.conn.cursor()

    try:
        room_uuid = str(uuid4())
        
        cursorObj.execute('''
            INSERT INTO chatbot(uuid, privilege, amount_seller, username_seller, username_buyer)
            VALUES(?, ?, ?, ?, ?)''', (
            room_uuid,
            'penjual',
            amount,
            data['username'],
            'none'
        ))
        
        # Use message template from config
        msg = Config.SYSTEM_MESSAGES['seller_welcome'].format(
            username=data['username'],
            amount=amount,
            bank_account=Config.BANK_ACCOUNT,
            bank_name=Config.BANK_NAME,
            account_holder=Config.ACCOUNT_HOLDER
        )
        
        cursorObj.execute('''
            INSERT INTO chatroom(uuid, msg_iter, msg_text)
            VALUES(?, ?, ?)''', (
            room_uuid,
            0,
            msg
        ))

        dbr.conn.commit()
        dbr.conn.close()

        return jsonify({
            "status": "success",
            "uuid": room_uuid,
            "message": f"Room '{room_uuid}' created successfully"
        }), 200

    except Exception as e:
        dbr.conn.rollback()
        dbr.conn.close()
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/join_room", methods=['POST'])
def join_room_api():
    data = request.get_json()
    
    # Validate input
    if not data.get('uuid') or not data.get('username'):
        return jsonify({"status": "error", "message": "UUID and username are required"}), 400
    
    dbr = DBSQLite(Config.DATABASE_PATH)
    cursorObj = dbr.conn.cursor()

    try:
        # Check if room exists
        cursorObj.execute('SELECT * FROM chatbot WHERE uuid = ?', (data['uuid'],))
        room = cursorObj.fetchone()
        
        if not room:
            return jsonify({"status": "error", "message": "Room not found"}), 404

        cursorObj.execute('''
            UPDATE chatbot SET username_buyer = ?
            WHERE uuid = ?''', (
            data['username'],
            data['uuid']
        ))
        
        msg = Config.SYSTEM_MESSAGES['buyer_joined'].format(username=data['username'])
        cursorObj.execute('''
            INSERT INTO chatroom(uuid, msg_iter, msg_text)
            VALUES(?, ?, ?)''', (
            data['uuid'],
            0,
            msg
        ))

        dbr.conn.commit()
        dbr.conn.close()

        return jsonify({
            "status": "success",
            "message": f"Joined room '{data['uuid']}' successfully"
        }), 200

    except Exception as e:
        dbr.conn.rollback()
        dbr.conn.close()
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/get_message", methods=['POST'])
def get_message():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data.get('uuid'):
            return jsonify({"status": "error", "message": "UUID is required"}), 400
            
        dbr = DBSQLite(Config.DATABASE_PATH)
        cursorObj=dbr.conn.cursor()
        cursorObj.execute('SELECT msg_text FROM chatroom WHERE uuid = ? ORDER BY msg_iter', (
                data['uuid'],
            )
        )
        rows = cursorObj.fetchall()
        dbr.conn.commit()
        dbr.conn.close()
        return jsonify({
                "status": "success",
                "message": rows
            }), 200 

@app.route("/send_message", methods=['POST'])
def send_message():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data.get('uuid') or not data.get('msg'):
            return jsonify({"status": "error", "message": "UUID and message are required"}), 400
            
        dbr = DBSQLite(Config.DATABASE_PATH)
        cursorObj = dbr.conn.cursor()
        
        # Get next message iteration
        cursorObj.execute('SELECT MAX(msg_iter) FROM chatroom WHERE uuid = ?', (data['uuid'],))
        max_iter = cursorObj.fetchone()[0] or 0
        
        cursorObj.execute('''
            INSERT INTO chatroom(uuid, msg_iter, msg_text)
            VALUES(?, ?, ?)''', (
            data['uuid'],
            max_iter + 1,
            data['msg']
        ))
        dbr.conn.commit()
        dbr.conn.close()
        
        # Enhanced real-time broadcasting
        message_data = {
            'room': data['uuid'],
            'message': data['msg'],
            'timestamp': datetime.now().isoformat(),
            'type': 'system' if '[SYSTEM]' in data['msg'] else 'payment' if '[ADMIN SYSTEM]' in data['msg'] else 'user'
        }
        
        # Emit to all users in the room
        socketio.emit('message', message_data, room=data['uuid'])
        
        # Additional notification for payment confirmations
        if '[ADMIN SYSTEM]' in data['msg']:
            if '[Y]' in data['msg']:
                # Payment confirmed
                socketio.emit('payment_status', {
                    'room': data['uuid'],
                    'status': 'confirmed',
                    'message': 'Payment has been confirmed successfully!',
                    'timestamp': datetime.now().isoformat()
                }, room=data['uuid'])
            elif '[N]' in data['msg']:
                # Payment cancelled
                socketio.emit('payment_status', {
                    'room': data['uuid'],
                    'status': 'cancelled',
                    'message': 'Transaction has been cancelled.',
                    'timestamp': datetime.now().isoformat()
                }, room=data['uuid'])
        
        return jsonify({
                "status": "success",
                "message": "send message success full"
            }), 200

@app.route("/generate_qr/<uuid>")
def generate_qr(uuid):
    # Generate QR code for room UUID
    qr = qrcode.QRCode(
        version=Config.QR_CODE_VERSION, 
        box_size=Config.QR_CODE_BOX_SIZE, 
        border=Config.QR_CODE_BORDER
    )
    qr.add_data(f"http://localhost:{Config.PORT}/join?uuid={uuid}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Serve as direct image file for better performance
    import io
    img_buffer = io.BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)
    
    return send_file(
        img_buffer,
        mimetype='image/png',
        as_attachment=False,
        download_name=f'qr_{uuid}.png'
    )

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    print(f"User joined room: {room}")
    emit('status', {'msg': f'Joined room: {room}'}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    print(f"User left room: {room}")
    emit('status', {'msg': f'Left room: {room}'}, room=room)

@socketio.on('disconnect')
def on_disconnect():
    print(f"User disconnected: {request.sid}")

@socketio.on('connect')
def on_connect():
    print(f"User connected: {request.sid}")
    emit('status', {'msg': 'Connected to server'})

@app.errorhandler(404)
def page_404(e):
    resp = make_response(jsonify({"msg":request.headers.get('User-Agent')}), 404)
    resp.headers = {
        'Date': strftime("%a, %d %b %Y %H:%M:%S UTC"),#'Tue, 06 Apr 2021 21:37:44 GMT',
        "Accept-Ranges": "bytes",
        "Content-Type": "application/json",
        "X-Frame-Options": "SAMEORIGIN",
        "Content-Security-Policy": "frame-ancestors 'self'",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
    }
    return resp