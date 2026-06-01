from flask import Blueprint
from app.controllers.saved_major_controller import save_major

saved_major_bp = Blueprint("saved_major", __name__)

saved_major_bp.route("/saved-majors", methods=["POST"])(save_major)