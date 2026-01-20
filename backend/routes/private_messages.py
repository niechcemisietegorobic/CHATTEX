from models import PrivateMessage, User, db
from flask import request, jsonify, Blueprint
from helpers import auth_user_id, user_by_username, limiter
from websock import send_only_to

private_messages_blueprint = Blueprint("private_messages_blueprint", __name__)

@private_messages_blueprint.route('/api/private/messages', methods=['GET'])
@limiter.limit("24 per minute")
def private_get():
    skip = request.args.get("skip", default=0, type=int)
    limit = min(request.args.get("limit", default=30, type=int), 100)
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    with_user = (request.args.get('with', default="")).strip()
    if not with_user:
        return jsonify({'error': 'Podaj ?with=username'}), 400

    other = user_by_username(with_user)
    if not other:
        return jsonify({'error': 'Nie ma takiego użytkownika'}), 404

    msgs = PrivateMessage.query.filter(
        db.or_(
            db.and_(PrivateMessage.sender_id == uid, PrivateMessage.receiver_id == other.id),
            db.and_(PrivateMessage.sender_id == other.id, PrivateMessage.receiver_id == uid)
        )
    ).order_by(PrivateMessage.timestamp.desc()).offset(skip).limit(limit).all()

    out = []
    for m in msgs:
        sender = User.query.get(m.sender_id)
        out.append({
            'id': m.id,
            'from': sender.username if sender else 'Nieznany',
            'to': with_user,
            'content': m.content,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    out.reverse()
    return jsonify(out), 200


@private_messages_blueprint.route('/api/private/messages/<int:mid>', methods=['DELETE'])
@limiter.limit("6 per minute")
def private_delete(mid: int):
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    msg = PrivateMessage.query.filter_by(id=mid).first()
    if (msg.sender_id != uid):
        return jsonify({'error': 'Brak uprawnień'}), 400
    db.session.delete(msg)
    db.session.commit()
    send_only_to(msg.receiver_id, "private_message_delete", {'id': mid})
    return jsonify({'id': mid}), 200


@private_messages_blueprint.route('/api/private/messages', methods=['POST'])
@limiter.limit("10 per 10 seconds")
def private_post():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    to_user = (data.get('to') or '').strip()
    content = (data.get('content') or '').strip()
    if not to_user or not content:
        return jsonify({'error': 'Wymagane: to, content'}), 400
    elif len(content) > 1024:
        return jsonify({'error': 'Wiadomość jest zbyt długa'}), 400

    other = user_by_username(to_user)
    if not other:
        return jsonify({'error': 'Nie ma takiego użytkownika'}), 404

    msg = PrivateMessage(sender_id=uid, receiver_id=other.id, content=content)
    db.session.add(msg)
    db.session.commit()
    u =  User.query.get(msg.sender_id)
    response = {
        'id': msg.id,
        'from': u.username if u else 'Nieznany',
        'to': to_user,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    send_only_to(other.id, "private_message", response)
    return jsonify(response), 201


@private_messages_blueprint.route('/api/users', methods=['GET'])
@limiter.limit("12 per minute")
def list_users():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    skip = request.args.get("skip", default=0, type=int)
    limit = min(request.args.get("limit", default=20, type=int), 50)
    users = User.query.order_by(User.username.asc()).filter_by(id!=uid).offset(skip).limit(limit).all()
    return jsonify([u.username for u in users]), 200
