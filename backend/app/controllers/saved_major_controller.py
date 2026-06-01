from flask import request, jsonify
from app.extensions import db
from database.models.saved_major import SavedMajor


def save_major():
    try:
        data = request.get_json()

        saved = SavedMajor(
            user_id=data.get("user_id"),
            macro_major=data.get("macro_major"),
            micro_major=data.get("micro_major"),
            note=data.get("note"),
        )

        db.session.add(saved)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": saved.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500