from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime

db = SQLAlchemy()


class Act(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    recording = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'recording': self.recording,
            'content': self.content,
            'created_at': self.created_at
        }
