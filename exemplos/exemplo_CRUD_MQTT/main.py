from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_mqtt import Mqtt
import os
import json

from controllers.auth_controller import auth_bp
from controllers.sensor_controller import sensor_bp
from controllers.readings_controller import readings_bp

from models.db import db
from models.user import User
from models.sensor_reading import SensorReading
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Configuração do MySQL
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'sensor_system')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração MQTT
app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL', 'mqtt-dashboard.com')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT', '1883'))
app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME', '')
app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD', '')
app.config['MQTT_KEEPALIVE'] = int(os.getenv('MQTT_KEEPALIVE', '5000'))
app.config['MQTT_TLS_ENABLED'] = os.getenv('MQTT_TLS_ENABLED', 'False').lower() == 'true'

# Inicializar SQLAlchemy
db.init_app(app)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

# Inicializar MQTT
mqtt_client = Mqtt()
mqtt_client.init_app(app)

# Tópico MQTT para subscrever (# = wildcard para todos os subtópicos)
MQTT_TOPIC = os.getenv('MQTT_TOPIC', '/sensores/#')

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Handlers MQTT
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    """Conectar ao broker MQTT"""
    if rc == 0:
        print('✓ Conectado ao broker MQTT com sucesso!')
        mqtt_client.subscribe(MQTT_TOPIC)
        print(f'✓ Inscrito no tópico: {MQTT_TOPIC}')
    else:
        print(f'✗ Falha na conexão MQTT. Código: {rc}')

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    """Processar mensagens MQTT recebidas"""
    try:
        topic = message.topic
        payload = message.payload.decode()
        
        print(f'📨 Mensagem recebida - Tópico: {topic}')
        print(f'   Payload: {payload}')
        
        # Tentar parsear como JSON
        try:
            data = json.loads(payload)
            # Formato esperado: {"value": 25.5} ou {"valor": 25.5}
            value = data.get('value') or data.get('valor')
        except json.JSONDecodeError:
            # Se não for JSON, assumir que é um valor direto
            value = payload
        
        # Salvar leitura no banco de dados
        with app.app_context():
            success, result = SensorReading.save_reading(topic, value)
            
            if success:
                print(f'✓ Leitura salva: {topic} = {value}')
            else:
                print(f'✗ Erro ao salvar: {result}')
                
    except Exception as e:
        print(f'✗ Erro ao processar mensagem MQTT: {str(e)}')

@mqtt_client.on_log()
def handle_logging(client, userdata, level, buf):
    """Log de eventos MQTT (opcional - descomente se quiser ver logs detalhados)"""
    # print(f'[MQTT Log] {buf}')
    pass

# Rota raiz
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_bp, url_prefix='/sensors')
app.register_blueprint(readings_bp, url_prefix='/readings')

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
    print("="*50)
    print("🚀 Iniciando servidor Flask com MQTT")
    print(f"📊 Dashboard: http://localhost:5000")
    print(f"📡 MQTT Broker: {app.config['MQTT_BROKER_URL']}:{app.config['MQTT_BROKER_PORT']}")
    print(f"📮 Tópico MQTT: {MQTT_TOPIC}")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
