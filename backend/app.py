import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes import public_messages_blueprint, private_messages_blueprint, forum_blueprint, auth_blueprint
from websock import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

db.init_app(app)
socket.init_app(app)
CORS(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(public_messages_blueprint)
app.register_blueprint(private_messages_blueprint)
app.register_blueprint(forum_blueprint)

@app.route('/health', methods=['GET'])
def health():
    # Sprawdzenie czy backend działa
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socket.run(app, host='0.0.0.0', port=5000)
