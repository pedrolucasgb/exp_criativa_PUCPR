from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.sensor import Sensor

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Redirecionar para login se não autenticado, senão para dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de novos usuários"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Verificar se usuário já existe
        if User.get_by_username(username):
            flash('Usuário já existe.', 'error')
            return redirect(url_for('auth.register'))
        
        # Criar novo usuário
        success, result = User.save_user(username, email, password)
        
        if success:
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Erro ao criar conta: {result}', 'error')
    
    return render_template('register.html')

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal com listagem de sensores"""
    sensors = Sensor.get_sensors()
    return render_template('dashboard.html', sensors=sensors)

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('auth.login'))
