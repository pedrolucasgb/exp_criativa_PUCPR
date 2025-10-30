from models.db import db
from models.iot.devices import Device

class Sensor(db.Model):
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    
    def __init__(self, unit, topic):
        self.unit = unit
        self.topic = topic
    
    @staticmethod
    def save_sensor(name, brand, model, topic, unit, is_active):
        try:
            device = Device(name=name, brand=brand, model=model, is_active=is_active)
            sensor = Sensor(unit=unit, topic=topic)
            device.sensors.append(sensor)
            
            db.session.add(device)
            db.session.commit()
            return True, sensor
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def __repr__(self):
        return f'<Sensor {self.topic}>'