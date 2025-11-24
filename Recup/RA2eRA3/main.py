from flask import Flask, redirect, url_for
from flask_login import LoginManager
import os
from dotenv import load_dotenv

from controllers.auth_controller import auth_bp
from controllers.sensor_controller import sensor_bp

from models.db import db
from models.usuarios import Usuario
from models.itens_cardapio import ItemCardapio
from models.comanda import Comanda
from models.item_comanda import ItemComanda
from models.pagamento import Pagamento

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
    return Usuario.get(int(user_id))

# Rota raiz
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_bp, url_prefix='/cardapio')

# Criar tabelas do banco de dados
def init_db():
    """Inicializar o banco de dados"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Criar usuários padrão
        print("\n=== Inicializando Banco de Dados ===\n")
        
        # Caixa
        caixa = Usuario.get_by_email('caixa@restaurante.com')
        if not caixa:
            Usuario.save_usuario('Caixa Principal', 'caixa@restaurante.com', 'caixa123', 'caixa')
            print("✓ Usuário CAIXA criado - Email: caixa@restaurante.com | Senha: caixa123")
        
        # Atendente
        atendente = Usuario.get_by_email('atendente@restaurante.com')
        if not atendente:
            Usuario.save_usuario('Atendente 1', 'atendente@restaurante.com', 'atendente123', 'atendente')
            print("✓ Usuário ATENDENTE criado - Email: atendente@restaurante.com | Senha: atendente123")
        
        # Cliente
        cliente = Usuario.get_by_email('cliente@email.com')
        if not cliente:
            Usuario.save_usuario('Cliente Teste', 'cliente@email.com', 'cliente123', 'cliente')
            print("✓ Usuário CLIENTE criado - Email: cliente@email.com | Senha: cliente123")
        
        # Criar itens do cardápio
        if ItemCardapio.query.count() == 0:
            print("\n=== Populando Cardápio ===\n")
            
            # Bebidas
            ItemCardapio.save_item('Refrigerante', 'Coca-Cola, Guaraná ou Fanta', 'bebida', 5.00)
            ItemCardapio.save_item('Suco Natural', 'Laranja, Limão ou Maracujá', 'bebida', 8.00)
            ItemCardapio.save_item('Cerveja', 'Cerveja pilsen 350ml', 'bebida', 7.00)
            ItemCardapio.save_item('Água Mineral', 'Água sem gás 500ml', 'bebida', 3.00)
            
            # Comidas
            ItemCardapio.save_item('X-Burger', 'Hambúrguer, queijo, alface e tomate', 'comida', 25.00)
            ItemCardapio.save_item('X-Salada', 'Hambúrguer, queijo, alface, tomate e milho', 'comida', 28.00)
            ItemCardapio.save_item('X-Bacon', 'Hambúrguer, queijo, bacon e molho especial', 'comida', 30.00)
            ItemCardapio.save_item('Batata Frita', 'Porção de batata frita crocante', 'comida', 18.00)
            ItemCardapio.save_item('Pastel', 'Pastel de carne, queijo ou frango', 'comida', 12.00)
            
            # Sobremesas
            ItemCardapio.save_item('Pudim', 'Pudim de leite condensado', 'sobremesa', 10.00)
            ItemCardapio.save_item('Sorvete', 'Sorvete 2 bolas (vários sabores)', 'sobremesa', 12.00)
            ItemCardapio.save_item('Brownie', 'Brownie de chocolate com sorvete', 'sobremesa', 15.00)
            
            print("✓ Cardápio populado com 12 itens")
        
        print("\n=== Banco de dados inicializado com sucesso! ===\n")

if __name__ == '__main__':
    # Inicializar o banco de dados
    init_db()
    
    # Executar aplicação
    app.run(debug=True, host='0.0.0.0', port=5000)
