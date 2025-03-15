from app import db

# Book Model (Represents a general book title, not individual copies)
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    subject_category = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
