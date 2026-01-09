from flask_socketio import SocketIO
from flask import request
from helpers import _socket_auth_user_id

socket = SocketIO(cors_allowed_origins="*")

socket_sessions = {}

@socket.on("connect")
def handle_connect(data):
    if (data is not None and data["token"] is not None):
        user_id = _socket_auth_user_id(data["token"])
        if (user_id is not None):
            socket_sessions[request.sid] = user_id

@socket.on("disconnect")
def handle_disconnect():
    del socket_sessions[request.sid]