# app/services/auth_service.py

from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.User import User

def register_user(data):
    """
    Handles user registration by creating a new user record in the database.

    Arguments:
    - data (dict): User data including name, email, password, role, and barcode.

    Returns:
    - A tuple containing the response message and HTTP status code.
    """
    if not data or not all(key in data for key in ("name", "email", "password", "role", "barcode")):
        return {"error": "Missing required fields"}, 400

    hashed_password = generate_password_hash(data['password'])
    user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data['role'],
        barcode=data['barcode']
    )
    
    db.session.add(user)
    db.session.commit()
    
    return {"message": "User registered successfully"}, 201


def login_user(data):
    """
    Handles user login by checking credentials and returning JWT tokens.

    Arguments:
    - data (dict): User data including email and password.

    Returns:
    - A tuple containing the response message with tokens and HTTP status code.
    """
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not check_password_hash(user.password, data.get('password')):
        return {"error": "Invalid credentials"}, 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, 200


def refresh_token(identity):
    """
    Handles the refresh token process by creating a new access token.

    Arguments:
    - identity (int): The user ID.

    Returns:
    - A new access token string.
    """
    return create_access_token(identity=identity)


def logout_user():
    """
    Handles the user logout process. For now, this is a placeholder.

    Returns:
    - A message indicating logout was successful.
    """
    # For JWT, logging out is generally handled client-side.
    # No action is needed on the server as JWT tokens are stateless.
    return "Logout successful"
