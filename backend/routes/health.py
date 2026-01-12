from flask import jsonify, Blueprint

health_blueprint = Blueprint("health_blueprint", __name__)

@health_blueprint.route('/health', methods=['GET'])
def health():
    # Sprawdzenie czy backend działa
    return jsonify({"status": "ok"}), 200
