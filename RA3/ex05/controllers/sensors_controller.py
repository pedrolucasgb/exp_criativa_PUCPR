# sensors_blueprint.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from models.iot.sensors import Sensor

# Nome do blueprint mantém "sensor_" para não quebrar url_for existentes
sensor_ = Blueprint("sensor_", __name__, template_folder="views")


# --------- Helpers ---------
def _checkbox_to_bool(field_name: str) -> bool:
    # Considera marcado se veio no form (ex.: <input type="checkbox" name="is_active">)
    return field_name in request.form and request.form.get(field_name) in ("on", "true", "1")


# --------- Rotas ---------
@sensor_.route("/register_sensor", methods=["GET"])
@login_required
def register_sensor():
    # Apenas renderiza o formulário de cadastro
    return render_template("register_sensor.html")


@sensor_.route("/add", methods=["POST"])
@login_required
def add_sensor():
    try:
        name = request.form.get("name", "").strip()
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()
        topic = request.form.get("topic", "").strip()
        unit = request.form.get("unit", "").strip()
        is_active = _checkbox_to_bool("is_active")

        # (Opcional) validações simples
        if not name or not brand or not model or not topic or not unit:
            flash("Preencha todos os campos obrigatórios.", "error")
            return redirect(url_for("sensor_.register_sensor"))

        success, result = Sensor.save_sensor(name, brand, model, topic, unit, is_active)

        if success:
            flash("Sensor registrado com sucesso!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash(f"Erro ao registrar sensor: {result}", "error")
            return redirect(url_for("sensor_.register_sensor"))

    except Exception as e:
        flash(f"Erro ao registrar sensor: {str(e)}", "error")
        return redirect(url_for("sensor_.register_sensor"))


@sensor_.route("/edit_sensor", methods=["GET"])
@login_required
def edit_sensor():
    sensor_id = request.args.get("id")
    if not sensor_id:
        flash("Sensor ID é obrigatório.", "error")
        return redirect(url_for("auth.dashboard"))

    sensor = Sensor.get_single_sensor(sensor_id)
    if not sensor:
        flash("Sensor não encontrado.", "error")
        return redirect(url_for("auth.dashboard"))

    return render_template("update_sensor.html", sensor=sensor)


@sensor_.route("/update_sensor", methods=["POST"])
@login_required
def update_sensor():
    try:
        sensor_id = request.form.get("id")
        if not sensor_id:
            flash("Sensor ID é obrigatório.", "error")
            return redirect(url_for("auth.dashboard"))

        name = request.form.get("name", "").strip()
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()
        topic = request.form.get("topic", "").strip()
        unit = request.form.get("unit", "").strip()
        is_active = _checkbox_to_bool("is_active")

        if not name or not brand or not model or not topic or not unit:
            flash("Preencha todos os campos obrigatórios.", "error")
            return redirect(url_for("sensor_.edit_sensor", id=sensor_id))

        success, result = Sensor.update_sensor(sensor_id, name, brand, model, topic, unit, is_active)

        if success:
            flash("Sensor atualizado com sucesso!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash(f"Erro ao atualizar sensor: {result}", "error")
            return redirect(url_for("sensor_.edit_sensor", id=sensor_id))

    except Exception as e:
        flash(f"Erro ao atualizar sensor: {str(e)}", "error")
        # Tenta voltar para a edição do mesmo id, se existir
        return redirect(url_for("sensor_.edit_sensor", id=request.form.get("id")))
