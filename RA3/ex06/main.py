from flask import Flask, redirect, url_for
from flask_login import LoginManager
from controllers.auth_controller import auth_bp
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from models.db import db
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Add root route to the main app
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_, url_prefix='/sensors')
app.register_blueprint(actuator_, url_prefix='/actuators')

# Create database tables
def init_db():
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    # Initialize the database
    init_db()
    app.run(debug=True)
