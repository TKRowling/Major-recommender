from datetime import datetime
from app.extensions import db


class ChatbotHistory(db.Model):
    __tablename__ = "chatbot_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }