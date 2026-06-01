from flask import request, jsonify
from app.extensions import db
from database.models.user import User


def create_user():
    try:
        data = request.get_json()

        user = User(
            full_name=data.get("full_name"),
            email=data.get("email"),
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500