from models import PublicMessage, User, db
from flask import request, jsonify, Blueprint
from helpers import auth_user_id, limiter
from websock import send_to_all_except

public_messages_blueprint = Blueprint("public_messages_blueprint", __name__)

@public_messages_blueprint.route('/api/public/messages', methods=['GET'])
@limiter.limit("12 per minute")
def public_get():
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    # Pobiera wiadomości z publicznego czatu
    msgs = PublicMessage.query.order_by(PublicMessage.timestamp.desc()).limit(100).all()
    out = []
    for m in msgs:
        u = User.query.get(m.user_id)
        out.append({
            'id': m.id,
            'username': u.username if u else 'Nieznany',
            'content': m.content,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    out.reverse()
    return jsonify(out), 200

@public_messages_blueprint.route('/api/public/messages', methods=['POST'])
@limiter.limit("10 per 10 seconds")
def public_post():
    # Dodaje wiadomość do publicznego czatu
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    data = request.get_json() or {}
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify({'error': 'Brak treści'}), 400
    elif len(content) > 1024:
        return jsonify({'error': 'Wiadomość jest zbyt długa'}), 400
    msg = PublicMessage(user_id=uid, content=content)
    db.session.add(msg)
    db.session.commit()
    u = User.query.get(msg.user_id)
    response = {
        'id': msg.id,
        'username': u.username if u else 'Nieznany',
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    send_to_all_except(msg.user_id, "public_message", response)
    return jsonify(response), 201
