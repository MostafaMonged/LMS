from app import db
from app.models.Book import Book
from app.models.BookCopy import BookCopy
from datetime import datetime
from app.models.Reservation import Reservation
from app.models.User import User

def get_all_books_service():
    """
    Fetch all books from the catalog.

    Returns:
        - A tuple containing the list of books and HTTP status code.
    """
    try:
        books = Book.query.all()
        results = []
        for book in books:
            # Count available and total copies
            available_copies = BookCopy.query.filter_by(book_id=book.id, is_available=True).count()
            total_copies = BookCopy.query.filter_by(book_id=book.id).count()

            results.append({
                "id": book.id,
                "barcode": book.barcode,
                "title": book.title,
                "author": book.author,
                "subject_category": book.subject_category,
                "publication_date": book.publication_date.strftime('%Y-%m-%d'),
                "available_copies": available_copies,
                "total_copies": total_copies
            })

        return {"books": results}, 200

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_book_by_barcode_service(barcode):
    """
    Fetch all books from the catalog.

    Returns:
        - A tuple containing the list of books and HTTP status code.
    """
    try:
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Count available and total copies
        available_copies = BookCopy.query.filter_by(book_id=book.id, is_available=True).count()
        total_copies = BookCopy.query.filter_by(book_id=book.id).count()
        return{
            "id": book.id,
            "barcode": book.barcode,
            "title": book.title,
            "author": book.author,
            "subject_category": book.subject_category,
            "publication_date": book.publication_date.strftime('%Y-%m-%d'),
            "available_copies": available_copies,
            "total_copies": total_copies
            }, 200

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500

def add_book_service(data):
    """
    Add a new book to the catalog.
    """
    try:
        # Validate the input data
        if not data or not all(key in data for key in ('title', 'author', 'subject_category', 'publication_date')):
            return {"error": "Missing required fields"}, 400
        
        # Convert publication_date from string to date object
        try:
            publication_date = datetime.strptime(data['publication_date'], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}, 400
        
        # Check if a book with the same title and author already exists
        existing_book = Book.query.filter_by(title=data['title'], author=data['author'],publication_date = data['publication_date']).first()
        if existing_book:
            return {"error": "A book with the same title and author already exists"}, 400
        
        # Create a new book instance
        new_book = Book(
            title=data['title'],
            author=data['author'],
            subject_category=data['subject_category'],
            publication_date=publication_date,  # Now correctly formatted
            barcode=Book.generate_barcode(Book)
        )

        db.session.add(new_book)
        db.session.commit()

        return {"message": "Book added successfully", "book_id": new_book.id, "barcode": new_book.barcode}, 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return {"error": "Database error occurred", "details": str(e)}, 500


def modify_book_service(barcode, data):
    """
    Modify a book based on its barcode.
    
    Arguments:
    - barcode: The unique barcode of the book
    - data: Updated data for the book (e.g., title, author, etc.)
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the book by barcode
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Update the book details
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.subject_category = data.get('subject_category', book.subject_category)
        book.publication_date = data.get('publication_date', book.publication_date)
        
        db.session.commit()
        return {"message": "Book updated successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500



def delete_book_service(barcode):
    try:
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        db.session.delete(book)  # This will also delete its copies if cascade is set
        db.session.commit()
        return {"message": "Book and all its copies deleted successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500



#######################################Book Copy Management Service############################################

def create_book_copy_service(barcode, data):
    """
    Create a new book copy based on the book's barcode.
    
    Arguments:
    - barcode: The unique barcode of the book
    - data: Data for creating the book copy (e.g., rack_location)
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the book by barcode
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Create a new book copy
        book_copy = BookCopy(
            book_id=book.id,
            rack_location=data.get('rack_location'),
            is_available=True
        )
        
        db.session.add(book_copy)
        db.session.commit()
        
        # Notify users with pending reservations for this book
        reservations = Reservation.query.filter_by(book_id=book.id, status='Pending').all()
        for reservation in reservations:
            user = User.query.get(reservation.user_id)
            if user:
                subject = "Book Reservation Available"
                body = f"Dear {user.name},\n\nThe book '{book.title}' you reserved is now available. Please check it out soon.\n\nThank you!"
                user.add_notification(subject, body)

        return {"message": "Book copy created successfully"}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500


def delete_book_copy_service(barcode, copy_id):
    """
    Delete a book copy using the book barcode and copy ID.
    
    Arguments:
    - barcode: The unique barcode of the book
    - copy_id: The ID of the book copy
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the book by barcode
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Find the book copy by ID
        book_copy = BookCopy.query.filter_by(id=copy_id, book_id=book.id).first()
        if not book_copy:
            return {"error": "Book copy not found"}, 404
        
        # Check if the book copy is available
        if book_copy.is_available:
            return {"error": "Cannot delete a book copy that is currently checked out"}, 400
        
        # Delete the book copy
        db.session.delete(book_copy)
        db.session.commit()
        return {"message": "Book copy deleted successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def modify_book_copy_service(barcode, copy_id, data):
    """
    Modify a book copy using the book's barcode and copy ID.
    
    Arguments:
    - barcode: The unique barcode of the book
    - copy_id: The ID of the book copy
    - data: Data to modify the book copy (e.g., rack_location, availability)
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the book by barcode
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Find the book copy by ID
        book_copy = BookCopy.query.filter_by(id=copy_id, book_id=book.id).first()
        if not book_copy:
            return {"error": "Book copy not found"}, 404
        
        # Modify the book copy
        book_copy.rack_location = data.get('rack_location', book_copy.rack_location)
        book_copy.is_available = data.get('is_available', book_copy.is_available)
        
        db.session.commit()
        
        if book_copy.is_available:
            # Notify users with pending reservations for this book
            reservations = Reservation.query.filter_by(book_id=book.id, status='Pending').all()
            for reservation in reservations:
                user = User.query.get(reservation.user_id)
                if user:
                    subject = "Book Reservation Available"
                    body = f"Dear {user.name},\n\nThe book '{book.title}' you reserved is now available. Please check it out soon.\n\nThank you!"
                    user.add_notification(subject, body)

        return {"message": "Book copy modified successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def get_book_copies_service(barcode):
    """
    Fetch all book copies for a given book barcode.

    Arguments:
    - barcode: The unique barcode of the book

    Returns:
        - A tuple containing the list of book copies and HTTP status code.
    """
    try:
        # Find the book by barcode
        book = Book.query.filter_by(barcode=barcode).first()
        if not book:
            return {"error": "Book not found"}, 404

        # Fetch all book copies for the book
        book_copies = BookCopy.query.filter_by(book_id=book.id).all()
        results = []
        for copy in book_copies:
            results.append({
                "id": copy.id,
                "rack_location": copy.rack_location,
                "is_available": copy.is_available
            })

        return {"book_copies": results}, 200

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500