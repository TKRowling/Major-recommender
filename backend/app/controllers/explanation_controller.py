from flask import request
from app.services.explanation_service import generate_explanation
from app.utils.response_builder import success_response, error_response


def explain_macro_major_controller():
    try:
        payload = request.get_json() or {}

        macro_major = payload.get("macro_major", "").strip()
        if not macro_major:
            return error_response("macro_major is required", 400)

        explanation = generate_explanation(payload, macro_major)

        return success_response({
            "macro_major": macro_major,
            "explanation": explanation
        })

    except Exception as e:
        return error_response(f"Explanation failed: {str(e)}", 500)