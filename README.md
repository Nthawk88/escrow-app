# Escrow System - Web Application

A secure escrow payment system with real-time chat functionality, built with Flask and modern web technologies.

## Features

- **Secure Escrow Transactions**: Create and manage secure payment escrows
- **Real-time Chat**: Live messaging between buyers and sellers
- **QR Code Sharing**: Easy room sharing via QR codes
- **Modern Web Interface**: Beautiful, responsive UI built with Tailwind CSS
- **WebSocket Support**: Real-time updates and notifications
- **SQLite Database**: Lightweight, reliable data storage

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd escrow-app-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Access the web application**
   Open your browser and navigate to: `http://localhost:8080`

## Usage

### For Sellers (Creating Escrow Rooms)

1. **Open the web application** in your browser
2. **Fill in the seller information**:
   - Username: Your seller username
   - Transaction Amount: The amount in Indonesian Rupiah (IDR)
3. **Click "Create Room"** to generate a new escrow room
4. **Share the QR code** or room UUID with the buyer
5. **Wait for buyer confirmation** in the chat room
6. **Confirm payment** when the buyer has made the payment

### For Buyers (Joining Escrow Rooms)

1. **Get the room UUID** from the seller (via QR code or direct sharing)
2. **Open the web application** in your browser
3. **Fill in the buyer information**:
   - Room UUID: The escrow room identifier
   - Username: Your buyer username
4. **Click "Join Room"** to enter the escrow chat
5. **Review the payment details** in the chat
6. **Confirm payment** after making the transfer
7. **Wait for seller confirmation**

### Real-time Features

- **Live Chat**: Messages appear instantly for all participants
- **Status Updates**: Real-time connection status indicators
- **Payment Confirmations**: Instant notification of payment status
- **Room Management**: Automatic room joining and leaving

## API Endpoints

### Core Endpoints

- `GET /` - Main web interface
- `POST /create_room` - Create a new escrow room
- `POST /join_room` - Join an existing escrow room
- `POST /get_message` - Retrieve chat messages
- `POST /send_message` - Send a new message
- `GET /generate_qr/<uuid>` - Generate QR code for room

### WebSocket Events

- `join` - Join a chat room
- `leave` - Leave a chat room
- `message` - Receive real-time messages

## Database Schema

### Tables

**chatbot** - Room information
- `uuid` (TEXT, UNIQUE) - Room identifier
- `privilege` (TEXT) - User role (penjual/pembeli)
- `amount_seller` (INTEGER) - Transaction amount
- `username_seller` (TEXT) - Seller username
- `username_buyer` (TEXT) - Buyer username

**chatroom** - Chat messages
- `uuid` (TEXT) - Room identifier
- `msg_iter` (INTEGER) - Message sequence number
- `msg_text` (TEXT) - Message content

## Security Features

- **UUID-based Rooms**: Secure room identification
- **Input Validation**: Server-side validation of all inputs
- **CORS Protection**: Cross-origin request protection
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Content Security Policy headers

## Technology Stack

### Backend
- **Flask** - Web framework
- **Flask-SocketIO** - WebSocket support
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database
- **qrcode** - QR code generation

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling (Tailwind CSS)
- **JavaScript** - Client-side functionality
- **Socket.IO** - Real-time communication
- **Font Awesome** - Icons

## Development

### Project Structure
```
aol-softeng-main/
├── backend/
│   ├── __init__.py      # Flask app initialization
│   ├── routes.py        # API routes and WebSocket handlers
│   └── dbquery.py       # Database operations
├── static/
│   └── index.html       # Main web interface
├── run.py               # Application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Running in Development Mode
```bash
python run.py
```

The application will start in debug mode with:
- Host: 0.0.0.0 (accessible from any network interface)
- Port: 8080
- Debug logging enabled

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `run.py` or kill the process using port 8080

2. **Dependencies not found**
   - Ensure you're using Python 3.7+ and have installed requirements.txt

3. **Database errors**
   - The SQLite database will be created automatically on first run

4. **WebSocket connection issues**
   - Check if your browser supports WebSockets
   - Ensure no firewall is blocking the connection

### Logs
The application logs debug information to the console. Check the terminal output for any error messages.

## Future Enhancements

- [ ] Email/SMS OTP confirmation
- [ ] Bank integration for automatic transfers
- [ ] Government data protection integration (Kominfo)
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Advanced fraud detection
- [ ] Transaction history and analytics
- [ ] Escrow fee system

## License

This project is for educational and development purposes.

## Support

For issues or questions, please check the troubleshooting section or create an issue in the project repository.
"# escrow-app" 
