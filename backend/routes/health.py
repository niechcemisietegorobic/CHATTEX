from flask import jsonify, Blueprint
from models import User
from helpers import limiter
from websock import get_online_number

health_blueprint = Blueprint("health_blueprint", __name__)

@health_blueprint.route('/health', methods=['GET'])
@limiter.limit("120 per minute")
def fetch_health():
    return jsonify({"status": "ok"}), 200


@health_blueprint.route("/api/stats", methods=["GET"])
@limiter.limit("5 per minute")
def fetch_stats():
    online = get_online_number()
    registered = User.query.count()
    return jsonify({
        "online": online,
        "registered": registered
    }), 200
