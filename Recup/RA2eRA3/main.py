from flask import Flask, redirect, url_for
from flask_login import LoginManager
import os

from controllers.auth_controller import auth_bp
from controllers.sensor_controller import sensor_bp

from models.db import db
from models.user import User
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Configuração do MySQL
# Formato: mysql+pymysql://usuario:senha@host:porta/nome_do_banco
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'restaurante')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db.init_app(app)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Rota raiz
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_bp, url_prefix='/sensors')

# Criar tabelas do banco de dados
def init_db():
    """Inicializar o banco de dados"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Verificar se já existe usuário admin
        admin = User.get_by_username('admin')
        if not admin:
            # Criar usuário admin padrão
            User.save_user('admin', 'admin@admin.com', 'admin')
            print("Usuário admin criado com sucesso!")
            print("Username: admin")
            print("Password: admin")
        else:
            print("Usuário admin já existe.")
        
        print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    # Inicializar o banco de dados
    init_db()
    
    # Executar aplicação
    app.run(debug=True, host='0.0.0.0', port=5000)
