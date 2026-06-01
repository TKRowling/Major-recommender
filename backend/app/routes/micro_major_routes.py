from flask import Blueprint
from app.controllers.micro_major_controller import recommend_micro_majors_controller

micro_major_bp = Blueprint("micro_major_bp", __name__)


@micro_major_bp.route("/micro-majors", methods=["POST"])
def micro_majors():
    return recommend_micro_majors_controller()