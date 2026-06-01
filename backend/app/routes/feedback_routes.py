from flask import Blueprint
from app.controllers.feedback_controller import create_feedback

feedback_bp = Blueprint("feedback", __name__)

feedback_bp.route("/feedback", methods=["POST"])(create_feedback)