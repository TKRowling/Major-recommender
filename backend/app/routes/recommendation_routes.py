from flask import Blueprint
from app.controllers.recommendation_controller import recommend, history

recommendation_bp = Blueprint("recommendation_bp", __name__)

recommendation_bp.route("/recommend", methods=["POST"])(recommend)
recommendation_bp.route("/history", methods=["GET"])(history)