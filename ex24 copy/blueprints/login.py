from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required

login_bp = Blueprint('login_bp', __name__, template_folder='../templates')


@login_bp.route('/login', methods=['GET'])
def login():
    # expose as a callable that returns the login page (so app.py can import it)
    return render_template('login.html')


@login_bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash('Usuário e senha são obrigatórios')
        return redirect(url_for('login_bp.login'))

    # validate against central USER_STORE in app
    expected = current_app.config.get('USER_STORE') if current_app and current_app.config.get('USER_STORE') else None
    # fallback to module-level simple check if config missing
    if expected is None:
        expected = {'admin': 'admin', 'teste': 'teste'}

    pwd = expected.get(username)
    if pwd and pwd == password:
        # create a lightweight user object and login
        from flask_login import UserMixin

        class SimpleUser(UserMixin):
            def __init__(self, id):
                self.id = id

        user = SimpleUser(username)
        login_user(user)
        return redirect(url_for('home', user=username))
    else:
        flash('Usuário ou senha inválidos')
        return redirect(url_for('login_bp.login'))


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado')
    return redirect(url_for('login_bp.login'))


@login_bp.route('/dashboard')
@login_required
def dashboard():
    user = request.args.get('user', 'desconhecido')
    return render_template('dashboard.html', user=user)
