from flask import request
from app.services.micro_major_service import recommend_micro_majors
from app.utils.response_builder import success_response, error_response


def recommend_micro_majors_controller():
    try:
        payload = request.get_json() or {}

        macro_major = payload.get("macro_major", "").strip()
        if not macro_major:
            return error_response("macro_major is required", 400)

        micro_majors = recommend_micro_majors(macro_major, payload)

        return success_response({
            "macro_major": macro_major,
            "micro_majors": micro_majors
        })

    except Exception as e:
        return error_response(f"Micro-major recommendation failed: {str(e)}", 500)