from flask import request, jsonify
from app.extensions import db
from database.models.chatbot_history import ChatbotHistory


def save_chatbot_history():
    try:
        data = request.get_json()

        history = ChatbotHistory(
            user_id=data.get("user_id"),
            user_message=data.get("user_message"),
            bot_response=data.get("bot_response"),
        )

        db.session.add(history)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": history.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500