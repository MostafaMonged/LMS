from app import db
import uuid

# Book Model (Represents a general book with a unique barcode)
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(10), unique=True, nullable=False)  # Each book has a unique barcode
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    subject_category = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    copies = db.relationship('BookCopy', backref='book', cascade='all, delete-orphan', lazy=True)

    def generate_barcode(self):
        # Generate a unique barcode for each book using UUID
        return str(uuid.uuid4())
