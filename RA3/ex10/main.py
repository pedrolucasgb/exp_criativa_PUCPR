from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_mqtt import Mqtt
import json

from controllers.auth_controller import auth_bp
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read_
from controllers.writes_controller import write_
from controllers.users_controller import user_

from models.db import db
from models.user.users import User
from models.user.roles import Role
from models.iot.read import Read
from models.iot.write import Write

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5000  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your broker supports TLS, set it True

# Initialize Flask-SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# Initialize MQTT
mqtt_client = Mqtt()
mqtt_client.init_app(app)

# MQTT Topics
topic_subscribe = "/aula_flask/"

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# MQTT Handlers
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe)  # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    """Handle incoming MQTT messages"""
    if message.topic == topic_subscribe:
        try:
            js = json.loads(message.payload.decode())
            
            with app.app_context():
                # Check if it's a sensor reading
                if 'sensor' in js and 'valor' in js:
                    Read.save_read(js["sensor"], js["valor"])
                    print(f"Saved sensor reading: {js['sensor']} = {js['valor']}")
                
                # Check if it's an actuator command
                elif 'actuator' in js and 'command' in js:
                    Write.save_write(js["actuator"], js["command"])
                    print(f"Saved actuator command: {js['actuator']} = {js['command']}")
                    
        except json.JSONDecodeError:
            print(f"Invalid JSON: {message.payload}")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

@mqtt_client.on_log()
def handle_logging(client, userdata, level, buf):
    print(f"MQTT Log: {buf}")

# Add root route to the main app
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_, url_prefix='/sensors')
app.register_blueprint(actuator_, url_prefix='/actuators')
app.register_blueprint(read_, url_prefix='/reads')
app.register_blueprint(write_, url_prefix='/writes')
app.register_blueprint(user_, url_prefix='/users')

# Create database tables
def init_db():
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        # Create all tables
        db.create_all()
        
        # Create roles
        Role.save_role("Admin", "Usuário full")
        Role.save_role("User", "Usuário com limitações")
        
        # Create admin user
        User.save_user("Admin", "admin", "admin@admin.com", "admin")
        
        print("Database initialized successfully!")
        print("Default admin user created: username='admin', password='admin'")

if __name__ == '__main__':
    # Initialize the database
    init_db()
    app.run(debug=True)
