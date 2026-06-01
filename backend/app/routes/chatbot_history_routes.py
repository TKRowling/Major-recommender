from flask import Blueprint
from app.controllers.chatbot_history_controller import save_chatbot_history

chatbot_history_bp = Blueprint("chatbot_history", __name__)

chatbot_history_bp.route("/chatbot-history", methods=["POST"])(save_chatbot_history)