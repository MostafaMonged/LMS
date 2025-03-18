from datetime import datetime
from app import db

# Reservation Model (Tracks reserved books)
class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('Pending', 'Fulfilled', 'Cancelled'), default='Pending')

    user = db.relationship('User', backref='reservations', lazy=True)
    book = db.relationship('Book', backref='reservations', lazy=True)
