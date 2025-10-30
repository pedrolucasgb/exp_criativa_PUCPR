from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.iot.sensors import Sensor

sensor_ = Blueprint("sensor_", __name__, template_folder="views")

@sensor_.route('/register_sensor')
@login_required
def register_sensor():
    return render_template("register_sensor.html")

@sensor_.route('/add', methods=['POST'])
def add_sensor():
    try:
        name = request.form.get("name") 
        brand = request.form.get("brand")
        model = request.form.get("model")
        topic = request.form.get("topic")
        unit = request.form.get("unit")
        is_active = True if request.form.get("is_active") == "on" else False
        
        success, result = Sensor.save_sensor(name, brand, model, topic, unit, is_active)
        
        if success:
            flash('Sensor registered successfully!', 'success')
        else:
            flash(f'Error registering sensor: {result}', 'error')
            
    except Exception as e:
        flash(f'Error registering sensor: {str(e)}', 'error')
        
    return redirect(url_for('auth.dashboard'))