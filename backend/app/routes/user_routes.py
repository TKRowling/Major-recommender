from flask import Blueprint
from app.controllers.user_controller import create_user

user_bp = Blueprint("user", __name__)

user_bp.route("/users", methods=["POST"])(create_user)