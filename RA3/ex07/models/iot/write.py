from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuators_id = db.Column(db.Integer, db.ForeignKey('actuators.id'), nullable=False)
    value = db.Column(db.String(50), nullable=True)
    
    # Relationship
    actuator = db.relationship('Actuator', backref='writes', lazy=True)
    
    def __init__(self, write_datetime, actuators_id, value):
        self.write_datetime = write_datetime
        self.actuators_id = actuators_id
        self.value = value
    
    @staticmethod
    def save_write(command_topic, value):
        """Save actuator command to database"""
        try:
            actuator = Actuator.query.filter(Actuator.command_topic == command_topic).first()
            
            if actuator is not None:
                device = Device.query.filter(Device.id == actuator.device_id).first()
                
                if device is not None and device.is_active == True:
                    write = Write(
                        write_datetime=datetime.now(),
                        actuators_id=actuator.id,
                        value=str(value)
                    )
                    db.session.add(write)
                    db.session.commit()
                    return True, write
                else:
                    return False, "Device not active or not found"
            else:
                return False, "Actuator not found"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_writes_by_actuator(actuator_id, limit=10):
        """Get latest writes for a specific actuator"""
        return Write.query.filter_by(actuators_id=actuator_id)\
            .order_by(Write.write_datetime.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_all_writes(limit=50):
        """Get latest writes with explicit joins to avoid ambiguity"""
        return db.session.query(Write, Actuator, Device)\
            .select_from(Write)\
            .join(Actuator, Write.actuators_id == Actuator.id)\
            .join(Device, Actuator.device_id == Device.id)\
            .order_by(Write.write_datetime.desc())\
            .limit(limit)\
            .all()
    
    def __repr__(self):
        return f'<Write {self.id} - Actuator {self.actuators_id} - {self.value}>'
