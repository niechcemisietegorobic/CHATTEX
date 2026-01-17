from flask import jsonify, Blueprint
from helpers import limiter

health_blueprint = Blueprint("health_blueprint", __name__)

@health_blueprint.route('/health', methods=['GET'])
@limiter.limit("120 per minute")
def health():
    # Sprawdzenie czy backend działa
    return jsonify({"status": "ok"}), 200

@health_blueprint.errorhandler(429)
def ratelimit_handler():
    return jsonify({"error": "ratelimit exceeded"}), 429

@health_blueprint.errorhandler(404)
def notfound_handler():
    return jsonify({"error": "file not found"}), 404
