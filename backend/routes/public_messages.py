from models import PublicMessage, User, db
from flask import request, jsonify, Blueprint
from helpers import _auth_user_id

public_messages_blueprint = Blueprint("public_messages_blueprint", __name__)

# ---------- PUBLIC CHAT ----------
@public_messages_blueprint.route('/api/public/messages', methods=['GET'])
def public_get():
    # Pobiera wiadomości z publicznego czatu
    msgs = PublicMessage.query.order_by(PublicMessage.timestamp.asc()).all()
    out = []
    for m in msgs:
        u = User.query.get(m.user_id)
        out.append({
            'id': m.id,
            'username': u.username if u else 'Nieznany',
            'content': m.content,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(out), 200

@public_messages_blueprint.route('/api/public/messages', methods=['POST'])
def public_post():
    # Dodaje wiadomość do publicznego czatu
    uid = _auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    data = request.get_json() or {}
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'error': 'Brak treści'}), 400
    msg = PublicMessage(user_id=uid, content=content)
    db.session.add(msg)
    db.session.commit()
    u = User.query.get(msg.user_id)
    return jsonify({
        'id': msg.id,
        'username': u.username if u else 'Nieznany',
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }), 201