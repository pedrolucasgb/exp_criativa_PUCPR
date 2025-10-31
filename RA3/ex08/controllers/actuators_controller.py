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

@actuator_.route('/edit_actuator')
@login_required
def edit_actuator():
    id = request.args.get('id')
    if not id:
        flash('Actuator ID is required', 'error')
        return redirect(url_for('auth.dashboard'))
    
    actuator = Actuator.get_single_actuator(id)
    if not actuator:
        flash('Actuator not found', 'error')
        return redirect(url_for('auth.dashboard'))
    
    return render_template("update_actuator.html", actuator=actuator)

@actuator_.route('/update_actuator', methods=['POST'])
@login_required
def update_actuator():
    try:
        id = request.form.get("id")
        name = request.form.get("name")
        brand = request.form.get("brand")
        model = request.form.get("model")
        command_topic = request.form.get("command_topic")
        is_active = True if request.form.get("is_active") == "on" else False
        
        success, result = Actuator.update_actuator(id, name, brand, model, command_topic, is_active)
        
        if success:
            flash('Actuator updated successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash(f'Error updating actuator: {result}', 'error')
            return redirect(url_for('actuator_.edit_actuator', id=id))
            
    except Exception as e:
        flash(f'Error updating actuator: {str(e)}', 'error')
        return redirect(url_for('actuator_.edit_actuator', id=id))

@actuator_.route('/delete_actuator', methods=['POST'])
@login_required
def delete_actuator():
    try:
        device_id = request.form.get('id')
        if not device_id:
            flash('Actuator ID is required', 'error')
            return redirect(url_for('auth.dashboard'))

        success, result = Actuator.delete_actuator(device_id)
        if success:
            flash('Actuator deleted successfully!', 'success')
        else:
            flash(f'Error deleting actuator: {result}', 'error')
    except Exception as e:
        flash(f'Error deleting actuator: {str(e)}', 'error')

    return redirect(url_for('auth.dashboard'))