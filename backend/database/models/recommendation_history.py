from datetime import datetime
from app.extensions import db


class RecommendationHistory(db.Model):
    __tablename__ = "recommendation_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    micro_major = db.Column(db.String(255), nullable=True)

    favorite_subjects = db.Column(db.JSON, nullable=True)
    good_at_subjects = db.Column(db.JSON, nullable=True)
    interests = db.Column(db.JSON, nullable=True)
    hobbies = db.Column(db.JSON, nullable=True)
    work_style = db.Column(db.JSON, nullable=True)
    future_workplace = db.Column(db.JSON, nullable=True)

    top1_major = db.Column(db.String(255), nullable=True)
    top1_score = db.Column(db.Float, nullable=True)
    top2_major = db.Column(db.String(255), nullable=True)
    top2_score = db.Column(db.Float, nullable=True)
    top3_major = db.Column(db.String(255), nullable=True)
    top3_score = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "micro_major": self.micro_major,
            "favorite_subjects": self.favorite_subjects,
            "good_at_subjects": self.good_at_subjects,
            "interests": self.interests,
            "hobbies": self.hobbies,
            "work_style": self.work_style,
            "future_workplace": self.future_workplace,
            "logical_thinking": self.logical_thinking,
            "communication_skill": self.communication_skill,
            "creativity": self.creativity,
            "leadership": self.leadership,
            "problem_solving": self.problem_solving,
            "teamwork": self.teamwork,
            "computer_skill": self.computer_skill,
            "analytical_skill": self.analytical_skill,
            "top1_major": self.top1_major,
            "top1_score": self.top1_score,
            "top2_major": self.top2_major,
            "top2_score": self.top2_score,
            "top3_major": self.top3_major,
            "top3_score": self.top3_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }