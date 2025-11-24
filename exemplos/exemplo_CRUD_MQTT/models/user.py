from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    @staticmethod
    def save_user(username, email, password):
        """Salvar um novo usuário"""
        try:
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return True, user
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get(user_id):
        """Buscar usuário por ID"""
        return User.query.get(int(user_id))
    
    @staticmethod
    def get_by_username(username):
        """Buscar usuário por username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_users():
        """Listar todos os usuários"""
        return User.query.all()
    
    def check_password(self, password):
        """Verificar se a senha está correta"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
