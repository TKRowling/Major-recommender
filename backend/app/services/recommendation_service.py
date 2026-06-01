from app.extensions import db
from app.services.model_service import predict_top3_recommendations
from database.models.recommendation_history import RecommendationHistory


def get_recommendations_and_save(payload):
    recommendations = predict_top3_recommendations(payload)

    history = RecommendationHistory(
        user_id=payload.get("user_id"),

        micro_major=None,

        favorite_subjects=payload.get("favorite_subjects_sorted", []),
        good_at_subjects=payload.get("good_at_subjects_sorted", []),
        interests=payload.get("interests_sorted", []),
        hobbies=payload.get("hobbies_sorted", []),

        work_style=payload.get("work_style", []),
        future_workplace=payload.get("future_workplace", []),

        top1_major=recommendations[0]["macro_major"] if len(recommendations) > 0 else None,
        top1_score=recommendations[0]["score"] if len(recommendations) > 0 else None,
        top2_major=recommendations[1]["macro_major"] if len(recommendations) > 1 else None,
        top2_score=recommendations[1]["score"] if len(recommendations) > 1 else None,
        top3_major=recommendations[2]["macro_major"] if len(recommendations) > 2 else None,
        top3_score=recommendations[2]["score"] if len(recommendations) > 2 else None,
    )

    db.session.add(history)
    db.session.commit()

    return {
        "recommendations": recommendations,
        "history_id": history.id
    }


def get_recommendation_history(limit=20):
    rows = (
        RecommendationHistory.query
        .order_by(RecommendationHistory.id.desc())
        .limit(limit)
        .all()
    )

    result = []
    for row in rows:
        result.append({
            "id": row.id,
            "favorite_subjects": row.favorite_subjects,
            "good_at_subjects": row.good_at_subjects,
            "interests": row.interests,
            "hobbies": row.hobbies,
            "work_style": row.work_style,
            "future_workplace": row.future_workplace,
            "top1_major": row.top1_major,
            "top1_score": row.top1_score,
            "top2_major": row.top2_major,
            "top2_score": row.top2_score,
            "top3_major": row.top3_major,
            "top3_score": row.top3_score,
        })

    return result