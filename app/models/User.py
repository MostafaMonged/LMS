from app import db
from datetime import datetime

# User Model (Members and Librarians)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('Member', 'Librarian'), nullable=False)
    barcode = db.Column(db.String(50), unique=True, nullable=False)  # Unique barcode for member identification
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
