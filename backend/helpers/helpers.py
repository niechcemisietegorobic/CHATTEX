import jwt
from flask import request, current_app
import os
from models import User
import random
import string

def auth_user_id():
    # Sprawdza token JWT i zwraca id użytkownika
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        return payload.get('user_id')
    except Exception:
        return None
    
def socket_auth_user_id(auth_header):
    # Sprawdza token JWT i zwraca id użytkownika
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        return payload.get('user_id')
    except Exception:
        return None

def user_by_username(username: str):
     # Szuka użytkownika po nazwie
    return User.query.filter_by(username=username).first()

def is_dev():
    return os.environ.get('IS_DEV', 'false').lower() == 'true'

def random_invite_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=8))

def check_environment():
    return (
        os.environ.get("IS_DEV") and
        os.environ.get("RDS_URL") and
        os.environ.get("CACHE_URL") and
        os.environ.get("RDS_SM") and
        os.environ.get("FRONTEND_URL") and
        os.environ.get("MEDIA_BUCKET") and
        os.environ.get("MEDIA_URL") and
        os.environ.get("REGION") 
    ) is not None

def media_bucket_url(filename):
    return f"https://{ os.environ.get("MEDIA_BUCKET") }.s3.{ os.environ.get("REGION") }.amazonaws.com/{filename}"

def default_background_url():
    return f"https://{ os.environ.get("MEDIA_BUCKET") }.s3.{ os.environ.get("REGION") }.amazonaws.com/backgrounds/default.png"
