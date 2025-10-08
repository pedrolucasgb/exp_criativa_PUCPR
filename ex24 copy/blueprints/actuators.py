from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

actuators_bp = Blueprint('actuators_bp', __name__, template_folder='../templates')

# small in-memory actuators dict
atuadores = {'Interruptor': 1, 'Lampada': 0}


@actuators_bp.route('/')
@login_required
def list_actuators():
    return render_template('list_actuators.html', actuators=atuadores)


@actuators_bp.route('/register', methods=['GET'])
@login_required
def register_actuator():
    return render_template('register_actuator.html')


@actuators_bp.route('/add', methods=['POST'])
def add_actuator():
    name = request.form.get('name')
    state = request.form.get('state')
    if not name:
        flash('Nome do atuador é obrigatório')
        return redirect(url_for('actuators_bp.register_actuator'))
    try:
        st = int(state)
        if st not in (0, 1):
            raise ValueError()
    except Exception:
        flash('Estado inválido: informe 0 ou 1')
        return redirect(url_for('actuators_bp.register_actuator'))
    atuadores[name] = st
    flash('Atuador cadastrado')
    return redirect(url_for('actuators_bp.list_actuators'))


@actuators_bp.route('/delete', methods=['GET'])
@login_required
def delete_actuator_form():
    return render_template('delete_actuator.html', atuadores=atuadores)


@actuators_bp.route('/delete', methods=['POST'])
def delete_actuator_action():
    name = request.form.get('name')
    if name and name in atuadores:
        atuadores.pop(name)
        flash(f'Atuador {name} removido com sucesso')
    else:
        flash('Atuador não encontrado')
    return redirect(url_for('actuators_bp.list_actuators'))
