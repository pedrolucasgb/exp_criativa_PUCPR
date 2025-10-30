from flask_login import UserMixin
from .database import get_db

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        db.close()
        
        if not user:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            password=user['password']
        )

    @staticmethod
    def get_by_username(username):
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        db.close()
        
        if not user:
            return None
            
        return User(
            id=user['id'],
            username=user['username'],
            password=user['password']
        )