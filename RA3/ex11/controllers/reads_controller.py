from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.iot.read import Read
from models.iot.sensors import Sensor

read_ = Blueprint("read_", __name__)

@read_.route('/reads', methods=['GET'])
@login_required
def list_reads():
    """List all sensor reads"""
    try:
        reads = Read.get_all_reads(limit=100)
        return render_template("reads.html", reads=reads)
    except Exception as e:
        flash(f'Error loading reads: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))

@read_.route('/reads/sensor/<int:sensor_id>', methods=['GET'])
@login_required
def reads_by_sensor(sensor_id):
    """Get reads for specific sensor"""
    try:
        reads = Read.get_reads_by_sensor(sensor_id, limit=50)
        return jsonify([{
            'id': r.id,
            'datetime': r.read_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'value': r.value
        } for r in reads])
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@read_.route('/history_read', methods=['GET'])
@login_required
def history_read():
    sensors = Sensor.get_sensors()
    read = {}
    return render_template('history_read.html', sensors=sensors, read=read)

@read_.route('/get_read', methods=['POST'])
@login_required
def get_read():
    if request.method == 'POST':
        sensor_id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(sensor_id, start, end)
        sensors = Sensor.get_sensors()
        return render_template('history_read.html', sensors=sensors, read=read)

@read_.route('/reads/api', methods=['POST'])
@login_required
def save_read_api():
    """API endpoint to save sensor reading (for MQTT or external calls)"""
    try:
        data = request.get_json()
        topic = data.get('topic')
        value = data.get('value')
        
        if not topic or value is None:
            return jsonify({'error': 'Topic and value are required'}), 400
        
        success, result = Read.save_read(topic, value)
        
        if success:
            return jsonify({'message': 'Read saved successfully', 'id': result.id}), 201
        else:
            return jsonify({'error': result}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
