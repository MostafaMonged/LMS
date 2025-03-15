from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///library.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = "placeholder for now"  # TODO
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

