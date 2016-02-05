from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String(64), index=True, unique=True)
    about_me = db.Column(db.String(200), nullable=True)
    access_token = db.Column(db.String, nullable=False)

    @property
    def is_authenticated(self):
        return True

    def __repr__(self):
        return '<User %r>' % (self.nickname)