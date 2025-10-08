from flask import Blueprint, render_template, request, redirect, url_for, flash

login_bp = Blueprint('login_bp', __name__, template_folder='../templates')

# simple in-memory user store for the example
users = {'admin': 'admin', 'pedro': 'senha123'}

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
    expected = users.get(username)
    if expected and expected == password:
        # on success redirect to the main app home (outside the blueprint)
        return redirect(url_for('home', user=username))
    else:
        flash('Usuário ou senha inválidos')
        return redirect(url_for('login_bp.login'))


@login_bp.route('/dashboard')
def dashboard():
    user = request.args.get('user', 'desconhecido')
    return render_template('dashboard.html', user=user)
