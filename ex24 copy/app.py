
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_required, current_user

# Import the login callable from the login blueprint (as requested)
from blueprints.login import login  # this imports the function that returns the login page

from blueprints.login import login_bp
from blueprints.sensors import sensors_bp
from blueprints.actuators import actuators_bp

app = Flask(__name__)
app.secret_key = 'dev-secret-ex19'

# simple user model for flask-login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# create login manager
login_manager = LoginManager()
login_manager.login_view = 'login_bp.login'
login_manager.init_app(app)

# In-memory users for authentication (username -> password)
# Per your request: admin/admin and teste/teste
USER_STORE = {'admin': 'admin', 'teste': 'teste'}


@login_manager.user_loader
def load_user(user_id):
    # user_id maps to username
    if user_id in USER_STORE:
        return User(user_id)
    return None

# register blueprints
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(sensors_bp, url_prefix='/sensors')
app.register_blueprint(actuators_bp, url_prefix='/actuators')

# expose user store to blueprints via config
app.config['USER_STORE'] = USER_STORE


@app.route('/')
def index():
    # start at the login page (login is provided by the auth blueprint)
    return redirect(url_for('login_bp.login'))


@app.route('/home')
@login_required
def home():
    # site home after login
    # include useful links that point to the registered blueprints
    user = current_user.id if current_user and hasattr(current_user, 'id') else None
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
        'Logout': url_for('login_bp.logout')
    }
    return render_template('index.html', links=links, user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
