from datetime import datetime
from app import db

# Transaction Model (To track book checkouts and returns)
class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_copy_id = db.Column(db.Integer, db.ForeignKey('book_copy.id'), nullable=False)
    checkout_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    fine_amount = db.Column(db.Float, default=0.0)

    user = db.relationship('User', backref='transactions', lazy=True)
    book_copy = db.relationship('BookCopy', backref='transactions', lazy=True)