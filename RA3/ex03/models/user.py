from flask_login import UserMixin
from .db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()