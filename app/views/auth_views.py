from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_view_bp = Blueprint('auth_views', __name__)

@auth_view_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('auth/register.html')

@auth_view_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('auth/login.html')

@auth_view_bp.route('/logout')
def logout():
    # We'll handle actual logout via JavaScript by removing the token
    return redirect(url_for('auth_views.login_page'))

@auth_view_bp.route('/dashboard')
@jwt_required()
def dashboard_redirect():
    # Get current user identity from JWT
    current_user = get_jwt_identity()
    
    # Get user role from database
    from app.models.User import User
    from app import db
    
    user = User.query.filter_by(email=current_user).first()
    
    if user.role == 'Librarian':
        return redirect(url_for('dashboard_views.librarian_dashboard'))
    else:  # Member
        return redirect(url_for('dashboard_views.member_dashboard'))