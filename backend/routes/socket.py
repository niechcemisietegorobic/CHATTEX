from flask_socketio import SocketIO, send, emit, join_room, leave_room

socket = SocketIO()

@socket.on("join")
def handle_join(data):
    print("joined", data)

