from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    recommendations = db.relationship("RecommendationHistory", backref="user", lazy=True)
    feedbacks = db.relationship("Feedback", backref="user", lazy=True)
    saved_majors = db.relationship("SavedMajor", backref="user", lazy=True)
    chatbot_histories = db.relationship("ChatbotHistory", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }