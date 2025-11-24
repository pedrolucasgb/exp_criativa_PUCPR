from models.db import db

class Sensor(db.Model):
    __tablename__ = 'sensors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    topic = db.Column(db.String(100), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __init__(self, name, brand, model, unit, topic, is_active=True):
        self.name = name
        self.brand = brand
        self.model = model
        self.unit = unit
        self.topic = topic
        self.is_active = is_active
    
    @staticmethod
    def save_sensor(name, brand, model, unit, topic, is_active=True):
        """Salvar um novo sensor"""
        try:
            sensor = Sensor(
                name=name,
                brand=brand,
                model=model,
                unit=unit,
                topic=topic,
                is_active=is_active
            )
            db.session.add(sensor)
            db.session.commit()
            return True, sensor
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_sensors():
        """Listar todos os sensores"""
        return Sensor.query.all()
    
    @staticmethod
    def get_single_sensor(sensor_id):
        """Buscar um sensor específico"""
        return Sensor.query.get(sensor_id)
    
    @staticmethod
    def update_sensor(sensor_id, name, brand, model, unit, topic, is_active):
        """Atualizar um sensor existente"""
        try:
            sensor = Sensor.query.get(sensor_id)
            if not sensor:
                return False, "Sensor não encontrado"
            
            sensor.name = name
            sensor.brand = brand
            sensor.model = model
            sensor.unit = unit
            sensor.topic = topic
            sensor.is_active = is_active
            
            db.session.commit()
            return True, sensor
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def delete_sensor(sensor_id):
        """Deletar um sensor"""
        try:
            sensor = Sensor.query.get(sensor_id)
            if not sensor:
                return False, "Sensor não encontrado"
            
            db.session.delete(sensor)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def __repr__(self):
        return f'<Sensor {self.name}>'
