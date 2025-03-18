from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import register_user, login_user, refresh_token#, logout_user

# Create a Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Handle user registration.

    Expected Form Data:
    - name: str
    - email: str
    - password: str
    - role: str
    - barcode: str

    Returns:
        A JSON response with a message indicating success or failure.
    """
    data = request.json

    response = register_user(data)
    return jsonify(response[0]), response[1]

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handle user login and JWT generation.

    Expected Form Data:
    - email: str
    - password: str

    Returns:
        A JSON response with access and refresh tokens or an error message.
    """
    # data = {
    #     "email": request.form.get("email"),
    #     "password": request.form.get("password"),
    # }
    data = request.json
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
    response = refresh_token(identity)
    return jsonify({"access_token": response}), 200

# @auth_bp.route('/logout', methods=['POST'])
# @jwt_required()
# def logout():
#     """
#     Logout the user. This is typically handled client-side by removing the JWT token.
    
#     Returns:
#         A JSON response indicating success.
#     """
#     response = logout_user()
#     return jsonify({"message": response}), 200