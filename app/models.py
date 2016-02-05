from datetime import datetime

from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, nullable=False,
                        onupdate=datetime.utcnow)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(64), nullable=True, index=True, unique=True)
    about_me = db.Column(db.String(200), nullable=True)
    profile_url = db.Column(db.String, nullable=False)
    access_token = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % (self.name)