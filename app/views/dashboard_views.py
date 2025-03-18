from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.User import User

dashboard_view_bp = Blueprint('dashboard_views', __name__)

@dashboard_view_bp.route('/')
@jwt_required()
def dashboard_redirect():
    # Get current user identity from JWT
    current_user = get_jwt_identity()
    
    # Get user from database
    user = User.query.filter_by(email=current_user).first()
    
    if not user:
        return redirect(url_for('auth_views.login_page'))
    
    if user.role == 'Librarian':
        return redirect(url_for('dashboard_views.librarian_dashboard'))
    else:  # Member
        return redirect(url_for('dashboard_views.member_dashboard'))

@dashboard_view_bp.route('/librarian')
@jwt_required()
def librarian_dashboard():
    # Get current user identity from JWT
    current_user = get_jwt_identity()
    
    # Get user from database
    user = User.query.filter_by(email=current_user).first()
    
    if not user or user.role != 'Librarian':
        return redirect(url_for('auth_views.login_page'))
    
    return render_template('dashboard/librarian_dashboard.html')

@dashboard_view_bp.route('/member')
@jwt_required()
def member_dashboard():
    # Get current user identity from JWT
    current_user = get_jwt_identity()
    
    # Get user from database
    user = User.query.filter_by(email=current_user).first()
    
    if not user or user.role != 'Member':
        return redirect(url_for('auth_views.login_page'))
    
    return render_template('dashboard/member_dashboard.html')

@dashboard_view_bp.route('/get-current-user')
@jwt_required()
def get_current_user():
    # Get current user identity from JWT
    current_user = get_jwt_identity()
    
    # Get user from database
    user = User.query.filter_by(email=current_user).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'barcode': user.barcode
    })