from models.db import db
from models.sensor import Sensor
from datetime import datetime

class SensorReading(db.Model):
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    read_datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationship
    sensor = db.relationship('Sensor', backref='readings', lazy=True)
    
    def __init__(self, sensor_id, value, read_datetime=None):
        self.sensor_id = sensor_id
        self.value = value
        self.read_datetime = read_datetime if read_datetime else datetime.now()
    
    @staticmethod
    def save_reading(topic, value):
        """Salvar leitura do sensor recebida via MQTT"""
        try:
            # Buscar sensor pelo tópico
            sensor = Sensor.query.filter_by(topic=topic, is_active=True).first()
            
            if not sensor:
                return False, f"Sensor não encontrado ou inativo para tópico: {topic}"
            
            # Criar nova leitura
            reading = SensorReading(
                sensor_id=sensor.id,
                value=float(value),
                read_datetime=datetime.now()
            )
            
            db.session.add(reading)
            db.session.commit()
            return True, reading
            
        except ValueError:
            db.session.rollback()
            return False, f"Valor inválido: {value}"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_readings_by_sensor(sensor_id, limit=50):
        """Buscar leituras de um sensor específico"""
        return SensorReading.query.filter_by(sensor_id=sensor_id)\
            .order_by(SensorReading.read_datetime.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_all_readings(limit=100):
        """Buscar todas as leituras com informações do sensor"""
        return db.session.query(SensorReading, Sensor)\
            .join(Sensor, SensorReading.sensor_id == Sensor.id)\
            .order_by(SensorReading.read_datetime.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_latest_by_sensor(sensor_id):
        """Buscar última leitura de um sensor"""
        return SensorReading.query.filter_by(sensor_id=sensor_id)\
            .order_by(SensorReading.read_datetime.desc())\
            .first()
    
    @staticmethod
    def get_readings_by_date_range(sensor_id, start_date, end_date):
        """Buscar leituras de um sensor em um intervalo de datas"""
        from sqlalchemy import and_
        return SensorReading.query.filter(
            and_(
                SensorReading.sensor_id == sensor_id,
                SensorReading.read_datetime >= start_date,
                SensorReading.read_datetime <= end_date
            )
        ).order_by(SensorReading.read_datetime.asc()).all()
    
    def __repr__(self):
        return f'<SensorReading {self.id} - Sensor {self.sensor_id} - Value {self.value}>'
