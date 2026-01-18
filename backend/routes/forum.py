from models import PostReaction, ForumComment, ForumPost, User, db
from flask import request, jsonify, Blueprint
from helpers import auth_user_id, limiter
from websock import send_to_all_except

forum_blueprint = Blueprint("forum_blueprint", __name__)

def reaction_counts_for_post(post_id: int):
    rows = PostReaction.query.filter_by(post_id=post_id).all()
    counts = {}
    for r in rows:
        counts[r.emoji] = counts.get(r.emoji, 0) + 1
    return counts

def comments_for_post(post_id: int):
    rows = ForumComment.query.filter_by(post_id=post_id).order_by(ForumComment.timestamp.desc()).limit(10).all()
    out = []
    for c in rows:
        author = User.query.get(c.author_id)
        out.append({
            'id': c.id,
            'author': author.username if author else 'Nieznany',
            'body': c.body,
            'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    out.reverse()
    return out

@forum_blueprint.route('/api/forum/posts', methods=['GET'])
@limiter.limit("12 per minute")
def forum_get_posts():
    posts = ForumPost.query.order_by(ForumPost.timestamp.desc()).limit(10).all()
    out = []
    for p in posts:
        author = User.query.get(p.author_id)
        out.append({
            'id': p.id,
            'author': author.username if author else 'Nieznany',
            'title': p.title,
            'body': p.body,
            'timestamp': p.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'reactions': reaction_counts_for_post(p.id),
            'comments': comments_for_post(p.id),
        })
    return jsonify(out), 200


@forum_blueprint.route('/api/forum/posts/<int:pid>', methods=['DELETE'])
@limiter.limit("3 per minute")
def forum_delete_post(pid: int):
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401
    post = ForumPost.query.filter_by(id=pid).first()
    if (post.author_id != uid):
        return jsonify({'error': 'Brak uprawnień'}), 400
    db.session.delete(post)
    db.session.commit()
    send_to_all_except(post.author_id, "forum_post_delete", {'id': pid})
    return jsonify({'id': pid}), 200


@forum_blueprint.route('/api/forum/posts', methods=['POST'])
@limiter.limit("2 per minute")
def forum_add_post():
    #dodawanie wlasnego posta
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    body = (data.get('body') or '').strip()
    if not title or not body:
        return jsonify({'error': 'Wymagane: title, body'}), 400
    elif len(title) > 120 or len(body) > 2048:
        return jsonify({'error': 'Tytuł lub treść posta jest zbyt długa'}), 400

    p = ForumPost(author_id=uid, title=title, body=body)
    db.session.add(p)
    db.session.commit()
    author =  User.query.get(p.author_id)
    response = {
        'id': p.id,
        'author': author.username if author else 'Nieznany',
        'title': p.title,
        'body': p.body,
        'timestamp': p.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'reactions': reaction_counts_for_post(p.id),
        'comments': comments_for_post(p.id),
    }
    send_to_all_except(p.author_id, "forum_post", response)
    return jsonify(response), 201

@forum_blueprint.route('/api/forum/comments', methods=['POST'])
@limiter.limit("10 per minute")
def forum_add_comment():
    # komentarze
    uid = auth_user_id()
    if not uid:
        return jsonify({'error': 'Brak/nieprawidłowy token'}), 401

    data = request.get_json() or {}
    post_id = data.get('post_id')
    body = (data.get('body') or '').strip()
    if not post_id or not body:
        return jsonify({'error': 'Wymagane: post_id, body'}), 400
    elif len(body) > 512:
        return jsonify({'error': 'Komentarz jest zbyt długi'}), 400

    p = ForumPost.query.get(post_id)
    if not p:
        return jsonify({'error': 'Post nie istnieje'}), 404

    c = ForumComment(post_id=p.id, author_id=uid, body=body)
    db.session.add(c)
    db.session.commit()
    u =  User.query.get(c.author_id)
    response = {
        'id': c.id,
        'author': u.username if u else 'Nieznany',
        'body': c.body,
        'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    send_to_all_except(c.author_id, "forum_comment", {'post_id': p.id, 'comment': response})
    return jsonify(response), 201

@forum_blueprint.route('/api/forum/reactions', methods=['POST'])
@limiter.limit("10 per 10 seconds")
def forum_toggle_reaction():
    # emoji
    uid = auth_user_id()
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

    response = reaction_counts_for_post(p.id)
    send_to_all_except(uid, "forum_reactions", {'post_id': p.id, 'reactions': response})
    return jsonify(response), 200
