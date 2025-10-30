from flask import Flask
from flask_login import LoginManager
from controllers.auth_controller import auth_bp
from models.database import init_db
from models.user import User

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure secret key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
