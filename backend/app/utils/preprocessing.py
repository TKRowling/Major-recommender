from app.utils.helpers import safe_list


def normalize_payload(payload):
    return {
        "user_id": payload.get("user_id"),

        "favorite_subjects_sorted": safe_list(payload.get("favorite_subjects_sorted")),
        "good_at_subjects_sorted": safe_list(payload.get("good_at_subjects_sorted")),
        "interests_sorted": safe_list(payload.get("interests_sorted")),
        "hobbies_sorted": safe_list(payload.get("hobbies_sorted")),

        "work_style": safe_list(payload.get("work_style")),
        "future_workplace": safe_list(payload.get("future_workplace")),
    }