from app import db

# BookCopy Model (Represents individual copies of books)
class BookCopy(db.Model):
    __tablename__ = 'book_copy'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    barcode = db.Column(db.String(50), unique=True, nullable=False)  # Each copy has a unique barcode
    rack_location = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    book = db.relationship('Book', backref=db.backref('copies', lazy=True))