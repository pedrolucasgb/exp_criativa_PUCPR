from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.iot.actuators import Actuator

actuator_ = Blueprint("actuator_", __name__, template_folder="views")

@actuator_.route('/register_actuator')
@login_required
def register_actuator():
    return render_template("register_actuator.html")

@actuator_.route('/add', methods=['POST'])
def add_actuator():
    try:
        name = request.form.get("name")
        brand = request.form.get("brand")
        model = request.form.get("model")
        command_topic = request.form.get("command_topic")
        is_active = True if request.form.get("is_active") == "on" else False
        
        success, result = Actuator.save_actuator(name, brand, model, command_topic, is_active)
        
        if success:
            flash('Actuator registered successfully!', 'success')
        else:
            flash(f'Error registering actuator: {result}', 'error')
            
    except Exception as e:
        flash(f'Error registering actuator: {str(e)}', 'error')
        
    return redirect(url_for('auth.dashboard'))