from flask_socketio import SocketIO
from flask import request
from helpers import socket_auth_user_id
from .cache import cache, get_all_key_values

socket = SocketIO(cors_allowed_origins="*")


def send_to_all_except(user_id: int, event: str, data):
    keyvals = get_all_key_values()
    [socket.emit(event, data, to=k) for k, v in keyvals.items() if v != str(user_id)]
    
def send_only_to(user_id: int, event: str, data):
    keyvals = get_all_key_values()
    [socket.emit(event, data, to=k) for k, v in keyvals.items() if v == str(user_id)]

@socket.on("connect")
def handle_connect(data):
    if (data is not None and data["token"] is not None):
        user_id = socket_auth_user_id(data["token"])
        if (user_id is not None):
            cache.set(request.sid, str(user_id))

@socket.on("disconnect")
def handle_disconnect():
    cache.delete([request.sid])
