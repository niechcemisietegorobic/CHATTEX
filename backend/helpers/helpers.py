
import jwt
from flask import request
import os
from models import User

#  -------------------- FUNKCJE POMOCNICZE --------------------
def _auth_user_id():
    # Sprawdza token JWT i zwraca id użytkownika
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', 'dev_secret_key'), algorithms=['HS256'])
        return payload.get('user_id')
    except Exception:
        return None

def _user_by_username(username: str):
     # Szuka użytkownika po nazwie
    return User.query.filter_by(username=username).first()