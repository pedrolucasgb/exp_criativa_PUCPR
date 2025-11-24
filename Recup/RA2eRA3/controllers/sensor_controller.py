from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.sensor import Sensor

sensor_bp = Blueprint("sensor", __name__)

def _checkbox_to_bool(field_name: str) -> bool:
    """Converter checkbox para booleano"""
    return field_name in request.form and request.form.get(field_name) in ("on", "true", "1")

@sensor_bp.route("/register_sensor", methods=["GET"])
@login_required
def register_sensor():
    """Renderizar formulário de cadastro de sensor"""
    return render_template("register_sensor.html")

@sensor_bp.route("/add", methods=["POST"])
@login_required
def add_sensor():
    """Adicionar novo sensor"""
    try:
        name = request.form.get("name", "").strip()
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()
        topic = request.form.get("topic", "").strip()
        unit = request.form.get("unit", "").strip()
        is_active = _checkbox_to_bool("is_active")

        # Validações
        if not name or not brand or not model or not topic or not unit:
            flash("Preencha todos os campos obrigatórios.", "error")
            return redirect(url_for("sensor.register_sensor"))

        success, result = Sensor.save_sensor(name, brand, model, unit, topic, is_active)

        if success:
            flash("Sensor cadastrado com sucesso!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash(f"Erro ao cadastrar sensor: {result}", "error")
            return redirect(url_for("sensor.register_sensor"))

    except Exception as e:
        flash(f"Erro ao cadastrar sensor: {str(e)}", "error")
        return redirect(url_for("sensor.register_sensor"))

@sensor_bp.route("/edit_sensor", methods=["GET"])
@login_required
def edit_sensor():
    """Renderizar formulário de edição de sensor"""
    sensor_id = request.args.get("id")
    if not sensor_id:
        flash("ID do sensor é obrigatório.", "error")
        return redirect(url_for("auth.dashboard"))

    sensor = Sensor.get_single_sensor(sensor_id)
    if not sensor:
        flash("Sensor não encontrado.", "error")
        return redirect(url_for("auth.dashboard"))

    return render_template("edit_sensor.html", sensor=sensor)

@sensor_bp.route("/update_sensor", methods=["POST"])
@login_required
def update_sensor():
    """Atualizar sensor existente"""
    try:
        sensor_id = request.form.get("id")
        if not sensor_id:
            flash("ID do sensor é obrigatório.", "error")
            return redirect(url_for("auth.dashboard"))

        name = request.form.get("name", "").strip()
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()
        topic = request.form.get("topic", "").strip()
        unit = request.form.get("unit", "").strip()
        is_active = _checkbox_to_bool("is_active")

        if not name or not brand or not model or not topic or not unit:
            flash("Preencha todos os campos obrigatórios.", "error")
            return redirect(url_for("sensor.edit_sensor", id=sensor_id))

        success, result = Sensor.update_sensor(sensor_id, name, brand, model, unit, topic, is_active)

        if success:
            flash("Sensor atualizado com sucesso!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash(f"Erro ao atualizar sensor: {result}", "error")
            return redirect(url_for("sensor.edit_sensor", id=sensor_id))

    except Exception as e:
        flash(f"Erro ao atualizar sensor: {str(e)}", "error")
        return redirect(url_for("sensor.edit_sensor", id=request.form.get("id")))

@sensor_bp.route('/delete_sensor', methods=['POST'])
@login_required
def delete_sensor():
    """Deletar sensor"""
    try:
        sensor_id = request.form.get('id')
        if not sensor_id:
            flash('ID do sensor é obrigatório.', 'error')
            return redirect(url_for('auth.dashboard'))

        success, result = Sensor.delete_sensor(sensor_id)
        if success:
            flash('Sensor deletado com sucesso!', 'success')
        else:
            flash(f'Erro ao deletar sensor: {result}', 'error')
    except Exception as e:
        flash(f'Erro ao deletar sensor: {str(e)}', 'error')

    return redirect(url_for('auth.dashboard'))
