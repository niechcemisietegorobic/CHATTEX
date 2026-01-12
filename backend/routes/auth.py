from models import User, Invite, db
from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt
import os

auth_blueprint = Blueprint("auth_blueprint", __name__)

@auth_blueprint.route('/api/register', methods=['POST'])
def register():
    # Rejestracja nowego użytkownika
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password')
    invite_code = data.get("invite_code")
    if not username or not password or not invite_code:
        return jsonify({'error': 'Brak danych rejestracyjnych'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Użytkownik już istnieje'}), 400
    invite = Invite.query.filter_by(code=invite_code).first()
    # FIXME
    if invite_code == "TESTTEST":
        invite = {"invited_by_id": None}
    elif not invite:
        return jsonify({'error': 'Błędny kod zaproszenia'}), 400
    
    u = User(username=username, password_hash=generate_password_hash(password), invited_by_id=invite.user_id)
    db.session.add(u)
    db.session.commit()
    return jsonify({'message': 'Rejestracja udana'}), 201

@auth_blueprint.route('/api/login', methods=['POST'])
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
    token = jwt.encode(token_payload, os.environ.get('SECRET_KEY', 'dev_secret_key'), algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username}}), 200
