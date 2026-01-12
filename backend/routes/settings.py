from models import User, db
from flask import request, jsonify, Blueprint
from helpers import auth_user_id
import datetime
import jwt

settings_blueprint = Blueprint("settings_blueprint", __name__)

@settings_blueprint.route('/api/user/username', methods=['POST'])
def login():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    # Logowanie i generowanie tokenu JWT
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    if not username:
        return jsonify({'error': 'Brak danych logowania'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Ta nazwa użytkownika jest już zajęta'}), 401
    
    user = User.query.filter_by(id=uid).first()
    if not user:
        return jsonify({'error': 'Błędny token'}), 401
    user.username = username
    db.session.commit()

    return jsonify({"message", "placeholder success"}), 200
