import os
import logging

from flask import Blueprint, jsonify, request

from app.services.chatbot_service import chatbot_service


logger = logging.getLogger(__name__)

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot", methods=["POST", "OPTIONS"])
def chatbot():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    history = data.get("history", [])
    session_id = str(data.get("session_id", "")).strip() or None

    if not question:
        return jsonify({"error": "Question is required."}), 400

    try:
        result = chatbot_service.answer_question(
            question=question,
            history=history,
            session_id=session_id,
        )
        return jsonify(result), 200

    except Exception as error:
        logger.exception("Chatbot route failed")

        response = {
            "error": "Failed to generate chatbot response."
        }

        if os.getenv("FLASK_DEBUG", "0") == "1":
            response["details"] = str(error)

        return jsonify(response), 500