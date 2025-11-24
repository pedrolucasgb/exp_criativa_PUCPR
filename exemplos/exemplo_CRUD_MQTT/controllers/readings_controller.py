from flask import Blueprint, render_template, request
from flask_login import login_required
from models.sensor_reading import SensorReading
from models.sensor import Sensor

readings_bp = Blueprint("readings", __name__)

@readings_bp.route("/history", methods=["GET"])
@login_required
def history():
    """Visualizar histórico de todas as leituras"""
    readings_with_sensors = SensorReading.get_all_readings(limit=100)
    return render_template("readings_history.html", readings=readings_with_sensors)

@readings_bp.route("/sensor/<int:sensor_id>", methods=["GET"])
@login_required
def sensor_history(sensor_id):
    """Visualizar histórico de leituras de um sensor específico"""
    sensor = Sensor.get_single_sensor(sensor_id)
    if not sensor:
        return "Sensor não encontrado", 404
    
    readings = SensorReading.get_readings_by_sensor(sensor_id, limit=100)
    return render_template("sensor_readings.html", sensor=sensor, readings=readings)

@readings_bp.route("/latest", methods=["GET"])
@login_required
def latest():
    """Visualizar últimas leituras de todos os sensores"""
    sensors = Sensor.get_sensors()
    latest_readings = []
    
    for sensor in sensors:
        latest = SensorReading.get_latest_by_sensor(sensor.id)
        latest_readings.append({
            'sensor': sensor,
            'reading': latest
        })
    
    return render_template("latest_readings.html", latest_readings=latest_readings)
