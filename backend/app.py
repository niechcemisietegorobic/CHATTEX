import os
import datetime
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from routes import public_messages_blueprint, private_messages_blueprint, forum_blueprint

# Backend aplikacji CHATTEX
# Flask + SQLite (lokalnie), gotowe pod AWS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

db.init_app(app)
CORS(app)

app.register_blueprint(public_messages_blueprint)
app.register_blueprint(private_messages_blueprint)
app.register_blueprint(forum_blueprint)

# ---------- PODSTAWOWE RZECZY------------------------
@app.route('/health', methods=['GET'])
def health():
    # Sprawdzenie czy backend działa
    return jsonify({"status": "ok"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    # Rejestracja nowego użytkownika
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Brak danych rejestracyjnych'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Użytkownik już istnieje'}), 400

    u = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(u)
    db.session.commit()
    return jsonify({'message': 'Rejestracja udana'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    # Logowanie i generowanie tokenu JWT
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Brak danych logowania'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Nieprawidłowa nazwa użytkownika lub hasło'}), 401

    token_payload = {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)}
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username}}), 200

@app.route('/api/users', methods=['GET'])
def list_users():
    # Lista użytkowników (do DM)
    users = User.query.order_by(User.username.asc()).all()
    return jsonify([u.username for u in users]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
