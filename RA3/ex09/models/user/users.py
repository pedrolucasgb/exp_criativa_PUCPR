from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    
    # Relationship
    role = db.relationship('Role', backref='users', lazy=True)
    
    def __init__(self, role_id, username, email, password):
        self.role_id = role_id
        self.username = username
        self.email = email
        self.password = password
    
    @staticmethod
    def save_user(role_type_, username, email, password):
        """Save a new user"""
        try:
            role = Role.get_single_role(role_type_)
            if not role:
                return False, "Role not found"
            
            user = User(
                role_id=role.id,
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
        """Get user by ID"""
        return User.query.get(int(user_id))
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_users():
        """Get all users with their roles"""
        return db.session.query(User, Role)\
            .join(Role, User.role_id == Role.id)\
            .all()
    
    @staticmethod
    def get_single_user(user_id):
        """Get a single user with role"""
        return db.session.query(User, Role)\
            .join(Role, User.role_id == Role.id)\
            .filter(User.id == user_id)\
            .first()
    
    @staticmethod
    def update_user(user_id, role_type_, username, email, password=None):
        """Update an existing user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            role = Role.get_single_role(role_type_)
            if not role:
                return False, "Role not found"
            
            user.role_id = role.id
            user.username = username
            user.email = email
            
            # Only update password if provided
            if password:
                user.password = generate_password_hash(password)
            
            db.session.commit()
            return True, user
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            db.session.delete(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
