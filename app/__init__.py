# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


# Initialize the database and JWT manager
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.models import User,Book,BookCopy,Transaction,Reservation

    #registering blueprints for backend routes
    from app.routes.auth_routes import auth_bp
    from app.routes.user_management_routes import user_management_bp
    from app.routes.book_management_routes import book_management_bp
    from app.routes.borrow_routes import borrow_bp
    from app.routes.search_routes import search_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_management_bp, url_prefix='/api')
    app.register_blueprint(book_management_bp, url_prefix='/api')
    app.register_blueprint(borrow_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    #register blueprints for frontend views
    from app.views.auth_views import auth_view_bp
    from app.views.user_management_views import user_management_view_bp
    app.register_blueprint(user_management_view_bp)
    app.register_blueprint(auth_view_bp)



    return app
