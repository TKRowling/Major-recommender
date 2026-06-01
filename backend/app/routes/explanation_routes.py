from flask import Blueprint
from app.controllers.explanation_controller import explain_macro_major_controller

explanation_bp = Blueprint("explanation_bp", __name__)


@explanation_bp.route("/explanation", methods=["POST"])
def explanation():
    return explain_macro_major_controller()