from models import User, Invite, db
from flask import request, jsonify, Blueprint
from helpers import auth_user_id, random_invite_code

settings_blueprint = Blueprint("settings_blueprint", __name__)

@settings_blueprint.route('/api/user/username', methods=['POST'])
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
    })

@settings_blueprint.route("/api/user/invite", methods=["POST"])
def get_invite():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}),
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
    })