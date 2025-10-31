from models.db import db
from models.iot.sensors import Sensor
from models.iot.devices import Device
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'read'
    
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    sensors_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    value = db.Column(db.Float, nullable=True)
    
    # Relationship
    sensor = db.relationship('Sensor', backref='reads', lazy=True)
    
    def __init__(self, read_datetime, sensors_id, value):
        self.read_datetime = read_datetime
        self.sensors_id = sensors_id
        self.value = value
    
    @staticmethod
    def save_read(topic, value):
        """Save sensor reading to database"""
        try:
            sensor = Sensor.query.filter(Sensor.topic == topic).first()
            
            if sensor is not None:
                device = Device.query.filter(Device.id == sensor.device_id).first()
                
                if device is not None and device.is_active == True:
                    read = Read(
                        read_datetime=datetime.now(),
                        sensors_id=sensor.id,
                        value=float(value)
                    )
                    db.session.add(read)
                    db.session.commit()
                    return True, read
                else:
                    return False, "Device not active or not found"
            else:
                return False, "Sensor not found"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_reads_by_sensor(sensor_id, limit=10):
        """Get latest reads for a specific sensor"""
        return Read.query.filter_by(sensors_id=sensor_id)\
            .order_by(Read.read_datetime.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_read(sensor_id, start, end):
        """Get historical reads for a sensor between start and end datetime"""
        from sqlalchemy import and_
        return Read.query.filter(
            and_(
                Read.sensors_id == sensor_id,
                Read.read_datetime > start,
                Read.read_datetime < end
            )
        ).order_by(Read.read_datetime.asc()).all()
    
    @staticmethod
    def get_all_reads(limit=50):
        """Get latest reads with explicit joins to avoid ambiguity"""
        return db.session.query(Read, Sensor, Device)\
            .select_from(Read)\
            .join(Sensor, Read.sensors_id == Sensor.id)\
            .join(Device, Sensor.device_id == Device.id)\
            .order_by(Read.read_datetime.desc())\
            .limit(limit)\
            .all()
    
    def __repr__(self):
        return f'<Read {self.id} - Sensor {self.sensors_id} - {self.value}>'
