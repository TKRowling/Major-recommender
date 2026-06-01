from flask import Blueprint, jsonify, request

from app.services.chatbot_service import chatbot_service


chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot", methods=["POST", "OPTIONS"])
def chatbot():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json() or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question is required."}), 400

    try:
        result = chatbot_service.answer_question(question)
        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "error": "Failed to generate chatbot response.",
            "details": str(error),
        }), 500