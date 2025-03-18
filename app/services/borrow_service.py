from app import db
from app.models.Transaction import Transaction
from app.models.Reservation import Reservation
from app.models.Book import Book
from app.models.BookCopy import BookCopy
from app.models.User import User
from datetime import datetime, timedelta

def issue_book_service(user_barcode, book_barcode):
    """
    Issue a book to a user (checkout).
    
    Arguments:
    - user_barcode: The barcode of the user
    - book_barcode: The barcode of the book
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the user
        user = User.query.filter_by(barcode=user_barcode).first()
        if not user:
            return {"error": "User not found"}, 404
        
        # Check if user has reached the maximum number of books (5)
        active_transactions = Transaction.query.filter_by(user_id=user.id, return_date=None).count()
        if active_transactions >= 5:
            return {"error": "User has reached the maximum number of books allowed (5)"}, 400
        
        # Find the book
        book = Book.query.filter_by(barcode=book_barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Find an available copy of the book
        book_copy = BookCopy.query.filter_by(book_id=book.id, is_available=True).first()
        if not book_copy:
            return {"error": "No available copies of this book"}, 400
        
        # Calculate due date (10 days from now)
        due_date = datetime.utcnow() + timedelta(days=10)
        
        # Create a new transaction
        new_transaction = Transaction(
            user_id=user.id,
            book_copy_id=book_copy.id,
            checkout_date=datetime.utcnow(),
            due_date=due_date,
            return_date=None,
            fine_amount=0.0
        )
        
        # Update the book copy to unavailable
        book_copy.is_available = False
        
        # Check if there's a pending reservation for this book and update it
        reservation = Reservation.query.filter_by(user_id=user.id, book_id=book.id, status='Pending').first()
        if reservation:
            reservation.status = 'Fulfilled'
        
        db.session.add(new_transaction)
        db.session.commit()
        
        return {
            "message": "Book issued successfully",
            "transaction_id": new_transaction.id,
            "due_date": due_date.strftime("%Y-%m-%d")
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def return_book_service(transaction_id):
    """
    Return a book to the library.
    
    Arguments:
    - transaction_id: ID of the transaction
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the transaction
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return {"error": "Transaction not found"}, 404
        
        # Check if the book has already been returned
        if transaction.return_date:
            return {"error": "This book has already been returned"}, 400
        
        # Calculate fine if the book is overdue
        current_date = datetime.utcnow()
        if current_date > transaction.due_date:
            # Calculate days overdue
            # the return of subtraction is timedelta object, so we can use days method to get the number of days
            days_overdue = (current_date - transaction.due_date).days
            # Calculate fine amount (assuming $0.50 per day)
            fine_amount = days_overdue * 0.50
            transaction.fine_amount = fine_amount
        
        # Update the transaction with return date
        transaction.return_date = current_date
        
        # Update the book copy to available
        book_copy = BookCopy.query.get(transaction.book_copy_id)
        if book_copy:
            book_copy.is_available = True
        
            # Notify users with pending reservations for this book
            # I think this is the simplest way to send notification, open for discussion in the presentation
            reservations = Reservation.query.filter_by(book_id=book_copy.book_id, status='Pending').all()
            for reservation in reservations:
                user = User.query.get(reservation.user_id)
                book = Book.query.get(book_copy.book_id)
                if user and book:
                    subject = "Book Reservation Available"
                    body = f"Dear {user.name},\n\nThe book '{book.title}' you reserved is now available. Please check it out soon.\n\nThank you!"
                    user.add_notification(subject, body)
        

        db.session.commit()
        
        response = {
            "message": "Book returned successfully",
            "transaction_id": transaction.id,
        }
        
        if transaction.fine_amount > 0:
            response["fine_amount"] = transaction.fine_amount
            response["message"] += f", with a fine of ${transaction.fine_amount:.2f}"
        
        return response, 200
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def reserve_book_service(user_barcode, book_barcode):
    """
    Reserve a book that is currently unavailable.
    
    Arguments:
    - user_barcode: The barcode of the user
    - book_barcode: The barcode of the book
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the user
        user = User.query.filter_by(barcode=user_barcode).first()
        if not user:
            return {"error": "User not found"}, 404
        
        # Find the book
        book = Book.query.filter_by(barcode=book_barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Check if any copies are available
        available_copies = BookCopy.query.filter_by(book_id=book.id, is_available=True).count()
        if available_copies > 0:
            return {"error": "This book is currently available, no need to reserve"}, 400
        
        # Check if user already has a pending reservation for this book
        existing_reservation = Reservation.query.filter_by(
            user_id=user.id, 
            book_id=book.id, 
            status='Pending'
        ).first()
        
        if existing_reservation:
            return {"error": "You already have a pending reservation for this book"}, 400
        
        # Create a new reservation
        new_reservation = Reservation(
            user_id=user.id,
            book_id=book.id,
            reservation_date=datetime.utcnow(),
            status='Pending'
        )
        
        db.session.add(new_reservation)
        db.session.commit()
        
        return {
            "message": "Book reserved successfully",
            "reservation_id": new_reservation.id
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def cancel_reservation_service(reservation_id):
    """
    Cancel a book reservation.
    
    Arguments:
    - reservation_id: ID of the reservation
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the reservation
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return {"error": "Reservation not found"}, 404
        
        # Check if the reservation is already fulfilled or cancelled
        if reservation.status != 'Pending':
            return {"error": f"This reservation is already {reservation.status.lower()}"}, 400
        
        # Update the reservation status to Cancelled
        reservation.status = 'Cancelled'
        
        db.session.commit()
        
        return {
            "message": "Reservation cancelled successfully"
        }, 200
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def renew_book_service(transaction_id):
    """
    Renew a book (extend the due date).
    
    Arguments:
    - transaction_id: ID of the transaction
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the transaction
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return {"error": "Transaction not found"}, 404
        
        # Check if the book has been returned
        if transaction.return_date:
            return {"error": "This book has already been returned"}, 400
        
        # Check if the book is overdue
        if datetime.utcnow() > transaction.due_date:
            return {"error": "Overdue books cannot be renewed"}, 400
        
        # Extend the due date by 10 more days from the current due date
        transaction.due_date = transaction.due_date + timedelta(days=10)
        
        db.session.commit()
        
        return {
            "message": "Book renewed successfully",
            "new_due_date": transaction.due_date.strftime("%Y-%m-%d")
        }, 200
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500

def check_overdue_books_service():
    """
    Check for overdue books and calculate fines.
    
    Returns:
        - A tuple containing the list of overdue books and HTTP status code.
    """
    try:
        current_date = datetime.utcnow()
        
        # Find all transactions where the book is overdue and not returned
        overdue_transactions = Transaction.query.filter(
            Transaction.due_date < current_date,
            Transaction.return_date.is_(None) 
        ).all()
        
        result = []
        for transaction in overdue_transactions:
            days_overdue = (current_date - transaction.due_date).days
            fine_amount = days_overdue * 0.50  # $0.50 per day
            
            user = User.query.get(transaction.user_id)
            book_copy = BookCopy.query.get(transaction.book_copy_id)
            book = Book.query.get(book_copy.book_id) if book_copy else None

            if user and book:
                # Add a notification to the user's notifications list here and open for discussion in the presentation
                subject = "Overdue Book Notification"
                body = f"Dear {user.name},\n\nThe book '{book.title}' is overdue by {days_overdue} days. Please return it as soon as possible to avoid further fines.\n\nThank you!"
                user.add_notification(subject, body)

            result.append({
                "transaction_id": transaction.id,
                "user_name": user.name if user else "Unknown",
                "user_email": user.email if user else "Unknown",
                "book_title": book.title if book else "Unknown",
                "days_overdue": days_overdue,
                "fine_amount": fine_amount,
                "due_date": transaction.due_date.strftime("%Y-%m-%d")
            })
        
        return {"overdue_books": result}, 200
        
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    

#it is the same as issue but the role is different
def checkout_book_service(user_barcode, book_barcode):
    """
    Issue a book to a user (checkout).
    
    Arguments:
    - user_barcode: The barcode of the user
    - book_barcode: The barcode of the book
    
    Returns:
        - A tuple containing the response message and HTTP status code.
    """
    try:
        # Find the user
        user = User.query.filter_by(barcode=user_barcode).first()
        if not user:
            return {"error": "User not found"}, 404
        
        # Check if user has reached the maximum number of books (5)
        active_transactions = Transaction.query.filter_by(user_id=user.id, return_date=None).count()
        if active_transactions >= 5:
            return {"error": "User has reached the maximum number of books allowed (5)"}, 400
        
        # Find the book
        book = Book.query.filter_by(barcode=book_barcode).first()
        if not book:
            return {"error": "Book not found"}, 404
        
        # Find an available copy of the book
        book_copy = BookCopy.query.filter_by(book_id=book.id, is_available=True).first()
        if not book_copy:
            return {"error": "No available copies of this book"}, 400
        
        # Calculate due date (10 days from now)
        due_date = datetime.utcnow() + timedelta(days=10)
        
        # Create a new transaction
        new_transaction = Transaction(
            user_id=user.id,
            book_copy_id=book_copy.id,
            checkout_date=datetime.utcnow(),
            due_date=due_date,
            return_date=None,
            fine_amount=0.0
        )
        
        # Update the book copy to unavailable
        book_copy.is_available = False
        
        # Check if there's a pending reservation for this book and update it
        reservation = Reservation.query.filter_by(user_id=user.id, book_id=book.id, status='Pending').first()
        if reservation:
            reservation.status = 'Fulfilled'
        
        db.session.add(new_transaction)
        db.session.commit()
        
        return {
            "message": "Book issued successfully",
            "transaction_id": new_transaction.id,
            "due_date": due_date.strftime("%Y-%m-%d")
        }, 201
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"An error occurred: {str(e)}"}, 500


#####################two routes I was missing in the requirements############################################
#o The system should retrieve information about checked-out books and borrowing history.

def get_borrowing_history_service(user_id):
    """
    Retrieve borrowing history for a specific user.
    
    Arguments:
    - user_id: The ID of the user.
    
    Returns:
    - A tuple containing the borrowing history and HTTP status code.
    """
    try:
        # Find the user
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        # Retrieve all transactions for the user
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        
        # Format the results
        history = []
        for transaction in transactions:
            book_copy = BookCopy.query.get(transaction.book_copy_id)
            book = Book.query.get(book_copy.book_id) if book_copy else None
            history.append({
                "transaction_id": transaction.id,
                "book_title": book.title,
                "checkout_date": transaction.checkout_date.strftime("%Y-%m-%d"),
                "due_date": transaction.due_date.strftime("%Y-%m-%d"),
                "return_date": transaction.return_date.strftime("%Y-%m-%d") if transaction.return_date else None,
                "fine_amount": transaction.fine_amount
            })
        
        return {"borrowing_history": history}, 200
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500


def get_checked_out_books_service(user_id):
    """
    Retrieve currently checked-out books for a specific user.
    
    Arguments:
    - user_id: The ID of the user.
    
    Returns:
    - A tuple containing the list of checked-out books and HTTP status code.
    """
    try:
        # Find the user
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        # Retrieve all active transactions (not returned)
        transactions = Transaction.query.filter_by(user_id=user_id, return_date=None).all()
        
        # Format the results
        checked_out_books = []
        for transaction in transactions:
            book_copy = BookCopy.query.get(transaction.book_copy_id)
            book = Book.query.get(book_copy.book_id) if book_copy else None
            checked_out_books.append({
                "transaction_id": transaction.id,
                "book_title": book.title if book else "Unknown",
                "checkout_date": transaction.checkout_date.strftime("%Y-%m-%d"),
                "due_date": transaction.due_date.strftime("%Y-%m-%d")
            })
        
        return {"checked_out_books": checked_out_books}, 200
    
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
    