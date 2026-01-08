from models import PrivateMessage, User, db
from flask import request, jsonify, Blueprint
from helpers import _auth_user_id, _user_by_username

private_messages_blueprint = Blueprint("private_messages_blueprint", __name__)

# ---------- PRIVATE (DM) ----------
@private_messages_blueprint.route('/api/private/messages', methods=['GET'])
def private_get():
    uid = _auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    with_user = (request.args.get('with') or '').strip()
    if not with_user:
        return jsonify({'error': 'Podaj ?with=username'}), 400

    other = _user_by_username(with_user)
    if not other:
        return jsonify({'error': 'Nie ma takiego użytkownika'}), 404

    msgs = PrivateMessage.query.filter(
        db.or_(
            db.and_(PrivateMessage.sender_id == uid, PrivateMessage.receiver_id == other.id),
            db.and_(PrivateMessage.sender_id == other.id, PrivateMessage.receiver_id == uid)
        )
    ).order_by(PrivateMessage.timestamp.asc()).all()

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
    return jsonify(out), 200

@private_messages_blueprint.route('/api/private/messages', methods=['POST'])
def private_post():
    uid = _auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    to_user = (data.get('to') or '').strip()
    content = (data.get('content') or '').strip()
    if not to_user or not content:
        return jsonify({'error': 'Wymagane: to, content'}), 400

    other = _user_by_username(to_user)
    if not other:
        return jsonify({'error': 'Nie ma takiego użytkownika'}), 404

    msg = PrivateMessage(sender_id=uid, receiver_id=other.id, content=content)
    db.session.add(msg)
    db.session.commit()
    u =  User.query.get(msg.sender_id)
    return jsonify({
        'id': msg.id,
        'from': u.username if u else 'Nieznany',
        'to': to_user,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }), 201