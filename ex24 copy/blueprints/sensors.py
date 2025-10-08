from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

sensors_bp = Blueprint('sensors_bp', __name__, template_folder='../templates')

# small in-memory sensors dict
sensores = {'Umidade': 22, 'Temperatura': 23}


@sensors_bp.route('/')
@login_required
def list_sensors():
    return render_template('list_sensors.html', sensores=sensores)


@sensors_bp.route('/register', methods=['GET'])
@login_required
def register_sensor():
    return render_template('register_sensor.html')


@sensors_bp.route('/add', methods=['POST'])
def add_sensor():
    name = request.form.get('name')
    value = request.form.get('value')
    if not name:
        flash('Nome do sensor é obrigatório')
        return redirect(url_for('sensors_bp.register_sensor'))
    try:
        val = float(value) if value else 0
    except ValueError:
        flash('Valor inválido')
        return redirect(url_for('sensors_bp.register_sensor'))
    sensores[name] = val
    flash('Sensor cadastrado')
    return redirect(url_for('sensors_bp.list_sensors'))


@sensors_bp.route('/delete', methods=['GET'])
@login_required
def delete_sensor_form():
    return render_template('delete_sensor.html', sensores=sensores)


@sensors_bp.route('/delete', methods=['POST'])
def delete_sensor_action():
    name = request.form.get('name')
    if name and name in sensores:
        sensores.pop(name)
        flash(f'Sensor {name} removido com sucesso')
    else:
        flash('Sensor não encontrado')
    return redirect(url_for('sensors_bp.list_sensors'))
