from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.iot.write import Write

write_ = Blueprint("write_", __name__, template_folder="views")

@write_.route('/writes', methods=['GET'])
@login_required
def list_writes():
    """List all actuator writes"""
    try:
        writes = Write.get_all_writes(limit=100)
        return render_template("writes.html", writes=writes)
    except Exception as e:
        flash(f'Error loading writes: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))

@write_.route('/writes/actuator/<int:actuator_id>', methods=['GET'])
@login_required
def writes_by_actuator(actuator_id):
    """Get writes for specific actuator"""
    try:
        writes = Write.get_writes_by_actuator(actuator_id, limit=50)
        return jsonify([{
            'id': w.id,
            'datetime': w.write_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'value': w.value
        } for w in writes])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@write_.route('/writes/api', methods=['POST'])
def save_write_api():
    """API endpoint to save actuator command (for MQTT or external calls)"""
    try:
        data = request.get_json()
        command_topic = data.get('command_topic')
        value = data.get('value')
        
        if not command_topic or value is None:
            return jsonify({'error': 'Command topic and value are required'}), 400
        
        success, result = Write.save_write(command_topic, value)
        
        if success:
            return jsonify({'message': 'Write saved successfully', 'id': result.id}), 201
        else:
            return jsonify({'error': result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
