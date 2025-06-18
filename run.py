#!/usr/bin/env python3
import sys
from config import Config

def startFlask(host, port):
    from backend import app, socketio
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    # Set to false to hide debug log info
    app.config['DEBUG'] = Config.DEBUG
    log.debug("[+] Listening on port {}".format(port))
    socketio.run(app, host=host, port=port, debug=Config.DEBUG)

if __name__ == '__main__':
    try:
        port = Config.PORT
        host = Config.HOST
        print(f"[+] Starting Escrow System on {host}:{port}")
        print(f"[+] Access the web application at: http://localhost:{port}")
        startFlask(host, port)
    except Exception as E:
        print(str(E))
        exit(1)