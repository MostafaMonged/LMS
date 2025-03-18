# app/services/auth_service.py

from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.User import User

# Helper function to check if the email is valid for a Librarian role
def is_valid_librarian_email(email):
    valid_domains = ["@library.com"]
    return any(email.endswith(domain) for domain in valid_domains)


def register_user(data):
    """
    Handles user registration by creating a new user record in the database.

    Arguments:
    - data (dict): User data including name, email, password, role.

    Returns:
    - A tuple containing the response message and HTTP status code.
    """
    if not data or not all(key in data for key in ("name", "email", "password", "role")):
        return {"error": "Missing required fields"}, 400

    if data['role'] == 'Librarian' and not is_valid_librarian_email(data['email']):
        return {"error": "Invalid email for Librarian role"}, 400
    try:
        # Check if the email already exists
        if User.query.filter_by(email=data['email']).first():
            return {"error": "A user with this email already exists"}, 400

        hashed_password = generate_password_hash(data['password'])
        user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=data['role'],
            barcode= User.generate_barcode(User)  # Generate a unique barcode for the user
        )
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201

    except Exception as e:
        db.session.rollback()  # Rollback transaction on failure
        return {"error": "Database error occurred", "details": str(e)}, 500


def login_user(data):
    """
    Handles user login by checking credentials and returning JWT tokens.

    Arguments:
    - data (dict): User data including email and password.

    Returns:
    - A tuple containing the response message with tokens and HTTP status code.
    """
    if not data or not all(key in data for key in ("email", "password")):
        return {"error": "Missing email or password"}, 400

    try:
        user = User.query.filter_by(email=data.get('email')).first()
        
        if not user or not check_password_hash(user.password, data.get('password')):
            return {"error": "Invalid credentials"}, 401

        # Create access and refresh tokens with the user's role included in the additional claims
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=user.email, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=user.email)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role
        }, 200

    except Exception as e:
        return {"error": "Database error occurred", "details": str(e)}, 500



def refresh_token(identity):
    """
    Handles the refresh token process by creating a new access token.

    Arguments:
    - identity (int): The user ID.

    Returns:
    - A new access token string.
    """
    return create_access_token(identity=identity)


# def logout_user():
#     """
#     Handles the user logout process. For now, this is a placeholder.

#     Returns:
#     - A message indicating logout was successful.
#     """
#     # For JWT, logging out is generally handled client-side.
#     # No action is needed on the server as JWT tokens are stateless.
#     return {"message": "Logout successful"}, 200
