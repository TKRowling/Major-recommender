from flask import request, jsonify
from app.extensions import db
from database.models.feedback import Feedback


def create_feedback():
    try:
        data = request.get_json()

        feedback = Feedback(
            user_id=data.get("user_id"),
            recommendation_id=data.get("recommendation_id"),
            rating=data.get("rating"),
            comment=data.get("comment"),
        )

        db.session.add(feedback)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": feedback.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500