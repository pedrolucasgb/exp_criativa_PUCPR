from models.db import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(512))
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    @staticmethod
    def save_role(name, description):
        """Save a new role"""
        try:
            role = Role(name=name, description=description)
            db.session.add(role)
            db.session.commit()
            return True, role
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_single_role(name):
        """Get a single role by name"""
        role = Role.query.filter(Role.name == name).first()
        return role
    
    @staticmethod
    def get_role():
        """Get all roles"""
        roles = Role.query.all()
        return roles
    
    def __repr__(self):
        return f'<Role {self.name}>'
