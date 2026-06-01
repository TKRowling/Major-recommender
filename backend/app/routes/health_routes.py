from flask import Blueprint, jsonify

health_bp = Blueprint("health_bp", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "Backend is running"
    }), 200