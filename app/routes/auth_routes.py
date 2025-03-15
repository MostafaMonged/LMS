# app/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import register_user, login_user, refresh_token, logout_user

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Handle user registration.

    Expected JSON input:
    {
        "name": <str>, 
        "email": <str>, 
        "password": <str>, 
        "role": <str>, 
        "barcode": <str>
    }

    Returns:
        A JSON response with a message indicating success or failure.
    """
    data = request.get_json()
    # Call the service to register the user
    response = register_user(data)
    return jsonify(response[0]), response[1]

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login and JWT generation.

    Expected JSON input:
    {
        "email": <str>,
        "password": <str>
    }

    Returns:
        A JSON response with access and refresh tokens or an error message.
    """
    data = request.get_json()
    # Call the service to log in and generate tokens
    response = login_user(data)
    return jsonify(response[0]), response[1]

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh the access token using a valid refresh token.
    
    Returns:
        A new access token in the JSON response.
    """
    identity = get_jwt_identity()
    # Call the service to refresh the token
    response = refresh_token(identity)
    return jsonify({"access_token": response}), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout the user. This is typically handled client-side by removing the JWT token.
    
    Returns:
        A JSON response indicating success.
    """
    # Call the service to handle logout
    response = logout_user()
    return jsonify({"message": response}), 200
