from flask import request, jsonify
from app.services.recommendation_service import (
    get_recommendations_and_save,
    get_recommendation_history,
)


def recommend():
    try:
        payload = request.get_json() or {}
        result = get_recommendations_and_save(payload)

        return jsonify({
            "success": True,
            "data": {
                "recommendations": result["recommendations"],
                "history_id": result["history_id"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


def history():
    try:
        rows = get_recommendation_history(limit=20)

        return jsonify({
            "success": True,
            "data": rows
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500