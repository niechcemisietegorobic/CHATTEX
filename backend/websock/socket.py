from flask_socketio import SocketIO
from flask import request
from helpers import socket_auth_user_id
import asyncio
# from .cache import cache

socket = SocketIO(cors_allowed_origins="*")

socket_sessions = {}

def send_to_all_except(user_id: int, event: str, data):
    pass
    
def send_only_to(user_id: int, event: str, data):
    pass

@socket.on("connect")
def handle_connect(data):
    if (data is not None and data["token"] is not None):
        user_id = socket_auth_user_id(data["token"])
        if (user_id is not None):
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(cache.set(request.sid, user_id))
            socket_sessions[request.sid] = user_id

@socket.on("disconnect")
def handle_disconnect():
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(cache.delete(request.sid))
    del socket_sessions[request.sid]
