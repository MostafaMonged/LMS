# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes.auth_routes import auth_bp

# Initialize the database and JWT manager
db = SQLAlchemy()
jwt = JWTManager()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Register auth blueprint
    
    return app
