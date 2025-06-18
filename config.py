import os

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 8080
    
    # Database Configuration
    DATABASE_PATH = 'chatbot.sqlite'
    
    # QR Code Configuration
    QR_CODE_VERSION = 1
    QR_CODE_BOX_SIZE = 10
    QR_CODE_BORDER = 5
    
    # Payment Configuration
    BANK_ACCOUNT = '13371337'
    BANK_NAME = 'BCA'
    ACCOUNT_HOLDER = 'RekBerSama'
    
    # Security Configuration
    CORS_ORIGINS = ['*']  # In production, specify actual origins
    
    # WebSocket Configuration
    SOCKETIO_CORS_ALLOWED_ORIGINS = '*'
    
    # Application Settings
    MAX_TRANSACTION_AMOUNT = 1000000000  # 1 billion IDR
    MIN_TRANSACTION_AMOUNT = 1000  # 1 thousand IDR
    
    # Message Templates
    SYSTEM_MESSAGES = {
        'seller_welcome': '[SYSTEM] HELLO INI INITIAL MESSAGE DARI "{username}", HARAP SELESAIKAN PEMBAYARAN SENILAI Rp.{amount:,} KE REKENING KAMI DI {bank_account} {bank_name} A/N {account_holder}',
        'buyer_joined': '[SYSTEM] USER "{username}" TELAH MASUK KEDALAM CHATBOT ...',
        'payment_confirmed_seller': '[Y][ADMIN SYSTEM] PEMBAYARAN DIKONFIRMASI OLEH PENJUAL',
        'payment_confirmed_buyer': '[Y][ADMIN SYSTEM] PEMBAYARAN TELAH DILAKUKAN OLEH PEMBELI',
        'transaction_cancelled_seller': '[N][ADMIN SYSTEM] CHATROOM DITUTUP PAKSA OLEH PENJUAL',
        'transaction_cancelled_buyer': '[N][ADMIN SYSTEM] CHATROOM DITUTUP PAKSA OLEH PEMBELI'
    } 