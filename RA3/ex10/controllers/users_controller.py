from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user.users import User
from models.user.roles import Role

user_ = Blueprint("user_", __name__)

@user_.route('/register_user', methods=['GET'])
@login_required
def register_user():
    """Show user registration form"""
    roles = Role.get_role()
    return render_template("register_user.html", roles=roles)

@user_.route('/add_user', methods=['POST'])
@login_required
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success, result = User.save_user(role_name, username, email, password)
        
        if success:
            flash(f'User {username} created successfully!', 'success')
        else:
            flash(f'Error creating user: {result}', 'error')
        
        return redirect(url_for('user_.list_users'))

@user_.route('/list_users', methods=['GET'])
@login_required
def list_users():
    """List all users"""
    users = User.get_users()
    return render_template("list_users.html", users=users)

@user_.route('/edit_user/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id):
    """Show edit user form"""
    user_data = User.get_single_user(user_id)
    if not user_data:
        flash('User not found', 'error')
        return redirect(url_for('user_.list_users'))
    
    roles = Role.get_role()
    return render_template("edit_user.html", user=user_data[0], role=user_data[1], roles=roles)

@user_.route('/update_user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    """Update a user"""
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form.get('password', '').strip()

        # Enforce password required for update
        if not password:
            flash('Password is required to update the user.', 'error')
            return redirect(url_for('user_.edit_user', user_id=user_id))

        success, result = User.update_user(user_id, role_name, username, email, password)
        
        if success:
            flash(f'User {username} updated successfully!', 'success')
        else:
            flash(f'Error updating user: {result}', 'error')
        
        return redirect(url_for('user_.list_users'))

@user_.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    # Prevent deleting yourself
    if user_id == current_user.id:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('user_.list_users'))
    
    success, error = User.delete_user(user_id)
    
    if success:
        flash('User deleted successfully!', 'success')
    else:
        flash(f'Error deleting user: {error}', 'error')
    
    return redirect(url_for('user_.list_users'))
