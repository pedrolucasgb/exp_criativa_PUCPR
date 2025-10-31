from models.db import db

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationships
    sensors = db.relationship('Sensor', backref='device', lazy=True, cascade="all, delete-orphan")
    actuators = db.relationship('Actuator', backref='device', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, brand, model, is_active=False):
        self.name = name
        self.brand = brand
        self.model = model
        self.is_active = is_active
    
    def __repr__(self):
        return f'<Device {self.name}>'