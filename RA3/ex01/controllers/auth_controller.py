from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3
from models.database import get_db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    username = request.form['username']
    password = request.form['password']
    
    user = User.get_by_username(username)
    
    if user and user.password == password:  # In production, use proper password hashing!
        login_user(user)
        return redirect(url_for('auth.dashboard'))
    
    flash('Invalid username or password')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            db.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
        finally:
            db.close()
    
    return render_template('register.html')

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))