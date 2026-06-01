def validate_recommendation_payload(payload):
    required_numeric = [
        "logical_thinking",
        "communication_skill",
        "creativity",
        "leadership",
        "problem_solving",
        "teamwork",
        "computer_skill",
        "analytical_skill"
    ]

    for field in required_numeric:
        value = payload.get(field, None)
        if value is None:
            return False, f"{field} is required"

        try:
            number = int(value)
            if number < 1 or number > 5:
                return False, f"{field} must be between 1 and 5"
        except Exception:
            return False, f"{field} must be an integer"

    return True, "Valid"