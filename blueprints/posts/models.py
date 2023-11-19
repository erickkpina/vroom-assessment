from database.database import db
from datetime import datetime


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_image = db.Column(db.Text, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'date_posted': self.date_posted.strftime("%Y-%m-%d %H:%M") if self.date_posted else None,
            'post_image': self.post_image
        }