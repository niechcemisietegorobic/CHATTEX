from flask import jsonify, Blueprint
from helpers import limiter

health_blueprint = Blueprint("health_blueprint", __name__)

@health_blueprint.route('/health', methods=['GET'])
@limiter.limit("120 per minute")
def health():
    # Sprawdzenie czy backend działa
    return jsonify({"status": "ok"}), 200

