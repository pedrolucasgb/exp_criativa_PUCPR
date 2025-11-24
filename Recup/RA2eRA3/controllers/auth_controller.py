from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.usuarios import Usuario
from models.comanda import Comanda

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Usuario.get_by_email(email)
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de novos clientes"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Verificar se email já existe
        if Usuario.get_by_email(email):
            flash('Email já cadastrado.', 'error')
            return redirect(url_for('auth.register'))
        
        # Criar novo cliente
        success, result = Usuario.save_usuario(nome, email, password, 'cliente')
        
        if success:
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Erro ao criar conta: {result}', 'error')
    
    return render_template('register.html')

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    # Buscar comandas do usuário logado
    if current_user.is_cliente():
        # Cliente vê apenas suas comandas
        comandas = Comanda.get_comandas_by_cliente(current_user.id)
    else:
        # Atendente e Caixa veem todas as comandas
        comandas = Comanda.get_comandas()
    
    # Se for caixa, buscar comandas fechadas para pagamento
    comandas_fechadas = []
    if current_user.is_caixa():
        comandas_fechadas = Comanda.get_comandas_fechadas()
    
    # Se for atendente ou caixa, buscar lista de clientes para seleção
    usuarios_clientes = []
    if current_user.is_atendente() or current_user.is_caixa():
        usuarios_clientes = Usuario.get_usuarios_by_tipo('cliente')
    
    return render_template('dashboard.html', 
                         comandas=comandas, 
                         comandas_fechadas=comandas_fechadas,
                         usuarios_clientes=usuarios_clientes)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('auth.login'))
