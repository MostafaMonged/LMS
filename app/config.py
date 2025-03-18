from datetime import timedelta

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = "placeholder for now"  # TODO
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'  # Production database

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # separate test DB
    TESTING = True
