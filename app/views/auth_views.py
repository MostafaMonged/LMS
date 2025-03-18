from flask import Blueprint, render_template

auth_view_bp = Blueprint("auth_view", __name__)  # Frontend Blueprint

@auth_view_bp.route('/register')
def register_page():
    return render_template('register.html')

@auth_view_bp.route('/login')
def login_page():
    return render_template('login.html')

@auth_view_bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')
