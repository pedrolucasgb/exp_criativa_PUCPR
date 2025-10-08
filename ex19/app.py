from flask import Flask, render_template, redirect, url_for, request

# Import the login callable from the login blueprint (as requested)
from blueprints.login import login  # this imports the function that returns the login page

from blueprints.login import login_bp
from blueprints.sensors import sensors_bp
from blueprints.actuators import actuators_bp

app = Flask(__name__)
app.secret_key = 'dev-secret-ex18'

# register blueprints
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(sensors_bp, url_prefix='/sensors')
app.register_blueprint(actuators_bp, url_prefix='/actuators')


@app.route('/')
def index():
    # start at the login page (login is provided by the auth blueprint)
    return redirect(url_for('login_bp.login'))


@app.route('/home')
def home():
    # site home after login
    # include useful links that point to the registered blueprints
    user = request.args.get('user')
    links = {
        'Home': url_for('home'),
        'Login': url_for('login_bp.login'),
        'Listar Sensores': url_for('sensors_bp.list_sensors'),
        'Cadastrar Sensor': url_for('sensors_bp.register_sensor'),
        'Remover Sensor': url_for('sensors_bp.delete_sensor_form'),
        'Listar Atuadores': url_for('actuators_bp.list_actuators'),
        'Cadastrar Atuador': url_for('actuators_bp.register_actuator'),
        'Remover Atuador': url_for('actuators_bp.delete_actuator_form'),
        'Dashboard': url_for('login_bp.dashboard'),
    }
    return render_template('index.html', links=links, user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
