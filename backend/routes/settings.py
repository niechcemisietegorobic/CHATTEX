from models import User, Invite, Background, db
from flask import request, jsonify, Blueprint
from helpers import auth_user_id, random_invite_code, limiter, default_background_url, media_bucket_url
import boto3
from botocore.exceptions import ClientError
import hashlib
from PIL import Image, UnidentifiedImageError
import os

settings_blueprint = Blueprint("settings_blueprint", __name__)

@settings_blueprint.route('/api/user/background', methods=['POST'])
@limiter.limit("6 per hour")
def change_background():
    # uid = auth_user_id()
    # if not uid:
    #     return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    if 'file' not in request.files:
        return jsonify({"error": "Zmiana tła nieudana (brak file in request.files)"}), 400
    file = request.files['file']
    if (file.filename.find('.') == -1):
        return jsonify({"error": "Zmiana tła nieudana (brak extension: filename )" + file.filename}), 400

    try:
        img = Image.open(file.stream)
        img.verify()
    except (UnidentifiedImageError, OSError) as e:
        return jsonify({"error": "Zmiana tła nieudana (niepoprawny obraz)" + str(e)}), 400
    file.stream.seek(0)
    
    sha256 = hashlib.sha256()
    while chunk := file.stream.read(4092):
        sha256.update(chunk)
    file_hash = sha256.hexdigest()
    file.stream.seek(0)

    _, ext = os.path.splitext(file.filename)
    s3_filename = f"backgrounds/{file_hash}{ext}"
    session = boto3.session.Session()
    client = session.client(
        service_name='s3',
        region_name=os.environ.get("REGION")
    )
    try:
        client.upload_fileobj(file, os.environ.get("MEDIA_BUCKET"), s3_filename)
    except ClientError as e:
        return jsonify({"error": str(e)}), 400#"Zmiana tła nieudana"}), 400
    # bg = Background(user_id=uid, url=media_bucket_url(s3_filename))
    # db.session.add(bg)
    # db.session.commit()
    return jsonify({"url": media_bucket_url(s3_filename)}), 200


@settings_blueprint.route('/api/background', methods=['GET'])
@limiter.limit("10 per 10 seconds")
def get_default_background():
    return jsonify({'url': default_background_url()}), 200


@settings_blueprint.route('/api/user/background', methods=['GET'])
@limiter.limit("10 per 10 seconds")
def get_background():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    bg = Background.query.filter_by(user_id=uid).first()
    if not bg:
        return jsonify({'url': default_background_url()}), 200
    return jsonify({'url': bg.url}), 200


@settings_blueprint.route('/api/user/username', methods=['POST'])
@limiter.limit("3 per hour")
def change_username():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

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

    return jsonify({"message": "placeholder success"}), 200


@settings_blueprint.route("/api/user/invite", methods=["GET"])
@limiter.limit("10 per 10 seconds")
def get_invite():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}),
    invite = Invite.query.filter_by(user_id=uid).first()
    if not invite:
        return jsonify({'error': 'Brak zaproszenia'}), 401
    
    return jsonify({
        'user_id': invite.user_id,
        'code': invite.code
    }), 200


@settings_blueprint.route("/api/user/invite", methods=["POST"])
@limiter.limit("6 per hour")
def refresh_invite():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    invite = Invite.query.filter_by(user_id=uid).first()
    if not invite:
        invite = Invite(user_id=uid, code=random_invite_code())
        db.session.add(invite)
    else:
        invite.code = random_invite_code()
    db.session.commit()
    
    return jsonify({
        'user_id': invite.user_id,
        'code': invite.code
    }), 200