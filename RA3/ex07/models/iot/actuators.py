from models.db import db
from models.iot.devices import Device

class Actuator(db.Model):
    __tablename__ = 'actuators'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    command_topic = db.Column(db.String(50), nullable=False)
    state = db.Column(db.Boolean, default=False)
    
    def __init__(self, command_topic):
        self.command_topic = command_topic
        self.state = False
    
    @staticmethod
    def save_actuator(name, brand, model, command_topic, is_active):
        try:
            device = Device(name=name, brand=brand, model=model, is_active=is_active)
            actuator = Actuator(command_topic=command_topic)
            device.actuators.append(actuator)
            
            db.session.add(device)
            db.session.commit()
            return True, actuator
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_single_actuator(id):
        actuator = db.session.query(Actuator, Device)\
            .join(Device)\
            .filter(Device.id == id)\
            .first()
        return actuator if actuator else None

    @staticmethod
    def get_actuators():
        return db.session.query(Actuator, Device)\
            .join(Device)\
            .all()

    @staticmethod
    def update_actuator(id, name, brand, model, command_topic, is_active):
        try:
            device = Device.query.filter_by(id=id).first()
            if not device:
                return False, "Device not found"
            
            actuator = Actuator.query.filter_by(device_id=id).first()
            if not actuator:
                return False, "Actuator not found"
            
            device.name = name
            device.brand = brand
            device.model = model
            device.is_active = is_active
            actuator.command_topic = command_topic
            
            db.session.commit()
            return True, Actuator.get_actuators()
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_actuator(id):
        """Delete actuator and its device by device id (cascades to actuator)."""
        try:
            device = Device.query.filter_by(id=id).first()
            if not device:
                return False, "Device not found"

            db.session.delete(device)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def __repr__(self):
        return f'<Actuator {self.command_topic}>'