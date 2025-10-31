from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models.db import db
from models.user.users import User
from models.iot.sensors import Sensor
from models.iot.actuators import Actuator

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
        
    username = request.form['username']
    password = request.form['password']
    
    user = User.get_by_username(username)
    
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('auth.dashboard'))
    
    flash('Invalid username or password')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        try:
            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'error')
            else:
                # Register as regular User by default
                success, result = User.save_user('User', username, email, password)
                if success:
                    flash('Registration successful! Please login.', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash(f'Error during registration: {result}', 'error')
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
    
    return render_template('register.html')

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get all sensors and actuators with their devices
        sensors = Sensor.get_sensors()
        actuators = Actuator.get_actuators()
        return render_template('dashboard.html', sensors=sensors, actuators=actuators)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))