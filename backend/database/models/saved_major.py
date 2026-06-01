from datetime import datetime
from app.extensions import db


class SavedMajor(db.Model):
    __tablename__ = "saved_major"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    macro_major = db.Column(db.String(255), nullable=False)
    micro_major = db.Column(db.String(255), nullable=True)
    note = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "macro_major": self.macro_major,
            "micro_major": self.micro_major,
            "note": self.note,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }