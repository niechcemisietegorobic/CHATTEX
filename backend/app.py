import os
import datetime
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

db = SQLAlchemy(app)
CORS(app)

# ---------- MODELE ----------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class PublicMessage(db.Model):
    __tablename__ = 'public_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class PrivateMessage(db.Model):
    __tablename__ = 'private_messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ForumPost(db.Model):
    __tablename__ = 'forum_posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class ForumComment(db.Model):
    __tablename__ = 'forum_comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class PostReaction(db.Model):
    __tablename__ = 'post_reactions'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    emoji = db.Column(db.String(16), nullable=False)

# ---------- HELPERS ----------
def _auth_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('user_id')
    except Exception:
        return None

def _user_by_username(username: str):
    return User.query.filter_by(username=username).first()

# ---------- BASIC ----------
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Brak danych rejestracyjnych'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Użytkownik już istnieje'}), 400

    u = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(u)
    db.session.commit()
    return jsonify({'message': 'Rejestracja udana'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = (data.get('username') or '').strip()
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Brak danych logowania'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Nieprawidłowa nazwa użytkownika lub hasło'}), 401

    token_payload = {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)}
    token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username}}), 200

@app.route('/api/users', methods=['GET'])
def list_users():
    users = User.query.order_by(User.username.asc()).all()
    return jsonify([u.username for u in users]), 200

# ---------- PUBLIC CHAT ----------
@app.route('/api/public/messages', methods=['GET'])
def public_get():
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

@app.route('/api/public/messages', methods=['POST'])
def public_post():
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
    return jsonify({'message': 'OK', 'id': msg.id}), 201

# ---------- PRIVATE (DM) ----------
@app.route('/api/private/messages', methods=['GET'])
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

@app.route('/api/private/messages', methods=['POST'])
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
    return jsonify({'message': 'OK', 'id': msg.id}), 201

# ---------- FORUM (posts + comments + reactions) ----------
def _reaction_counts_for_post(post_id: int):
    rows = PostReaction.query.filter_by(post_id=post_id).all()
    counts = {}
    for r in rows:
        counts[r.emoji] = counts.get(r.emoji, 0) + 1
    return counts

def _comments_for_post(post_id: int):
    rows = ForumComment.query.filter_by(post_id=post_id).order_by(ForumComment.timestamp.asc()).all()
    out = []
    for c in rows:
        author = User.query.get(c.author_id)
        out.append({
            'id': c.id,
            'author': author.username if author else 'Nieznany',
            'body': c.body,
            'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return out

@app.route('/api/forum/posts', methods=['GET'])
def forum_get_posts():
    posts = ForumPost.query.order_by(ForumPost.timestamp.desc()).all()
    out = []
    for p in posts:
        author = User.query.get(p.author_id)
        out.append({
            'id': p.id,
            'author': author.username if author else 'Nieznany',
            'title': p.title,
            'body': p.body,
            'timestamp': p.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'reactions': _reaction_counts_for_post(p.id),
            'comments': _comments_for_post(p.id),
        })
    return jsonify(out), 200

@app.route('/api/forum/posts', methods=['POST'])
def forum_add_post():
    uid = _auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    body = (data.get('body') or '').strip()
    if not title or not body:
        return jsonify({'error': 'Wymagane: title, body'}), 400

    p = ForumPost(author_id=uid, title=title, body=body)
    db.session.add(p)
    db.session.commit()
    return jsonify({'message': 'OK', 'id': p.id}), 201

@app.route('/api/forum/comments', methods=['POST'])
def forum_add_comment():
    uid = _auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    post_id = data.get('post_id')
    body = (data.get('body') or '').strip()
    if not post_id or not body:
        return jsonify({'error': 'Wymagane: post_id, body'}), 400

    p = ForumPost.query.get(post_id)
    if not p:
        return jsonify({'error': 'Post nie istnieje'}), 404

    c = ForumComment(post_id=p.id, author_id=uid, body=body)
    db.session.add(c)
    db.session.commit()
    return jsonify({'message': 'OK', 'id': c.id}), 201

@app.route('/api/forum/reactions', methods=['POST'])
def forum_toggle_reaction():
    uid = _auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    post_id = data.get('post_id')
    emoji = (data.get('emoji') or '').strip()
    if not post_id or not emoji:
        return jsonify({'error': 'Wymagane: post_id, emoji'}), 400

    p = ForumPost.query.get(post_id)
    if not p:
        return jsonify({'error': 'Post nie istnieje'}), 404

    existing = PostReaction.query.filter_by(post_id=p.id, user_id=uid, emoji=emoji).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(PostReaction(post_id=p.id, user_id=uid, emoji=emoji))
    db.session.commit()

    return jsonify({'message': 'OK', 'reactions': _reaction_counts_for_post(p.id)}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
