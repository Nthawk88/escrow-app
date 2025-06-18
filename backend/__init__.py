# Create a basic Flask app
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import pkgutil

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import any local modules that contain routes for use later
__all__ = []
__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__,
                                                      prefix=__name__+'.'):
    __import__(modname)  # noqa: E402