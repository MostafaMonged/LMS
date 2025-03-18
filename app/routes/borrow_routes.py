from flask import Blueprint, request, jsonify
from app.services.borrow_service import (
    issue_book_service,
    return_book_service,
    reserve_book_service,
    cancel_reservation_service,
    renew_book_service,
    check_overdue_books_service,
    checkout_book_service,
    get_borrowing_history_service,
    get_checked_out_books_service
)
from flask_jwt_extended import jwt_required, get_jwt

# Create a Blueprint for borrow
borrow_bp = Blueprint("borrow", __name__)

@borrow_bp.route('/issue', methods=['POST'])
@jwt_required()
def issue_book():
    """
    Issue a book to a user.
    
    Expected JSON data:
    - user_barcode: The barcode of the user
    - book_barcode: The barcode of the book
    
    Returns:
        - JSON response with success or error message.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    
    data = request.json
    if not data or not all(key in data for key in ('user_barcode', 'book_barcode')):
        return jsonify({"error": "Missing required fields"}), 400
    
    response = issue_book_service(data['user_barcode'], data['book_barcode'])
    return jsonify(response[0]), response[1]

@borrow_bp.route('/return/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def return_book(transaction_id):
    """
    Return a book to the library.
    
    Parameters:
    - transaction_id: ID of the transaction
    
    Returns:
        - JSON response with success or error message.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    
    response = return_book_service(transaction_id)
    return jsonify(response[0]), response[1]

@borrow_bp.route('/reserve', methods=['POST'])
@jwt_required()
def reserve_book():
    """
    Reserve a book that is currently unavailable.
    
    Expected JSON data:
    - user_barcode: The barcode of the user
    - book_barcode: The barcode of the book
    
    Returns:
        - JSON response with success or error message.
    """
    data = request.json
    if not data or not all(key in data for key in ('user_barcode', 'book_barcode')):
        return jsonify({"error": "Missing required fields"}), 400
    
    response = reserve_book_service(data['user_barcode'], data['book_barcode'])
    return jsonify(response[0]), response[1]

@borrow_bp.route('/cancel-reservation/<int:reservation_id>', methods=['PUT'])
@jwt_required()
def cancel_reservation(reservation_id):
    """
    Cancel a book reservation.
    
    Parameters:
    - reservation_id: ID of the reservation
    
    Returns:
        - JSON response with success or error message.
    """
    response = cancel_reservation_service(reservation_id)
    return jsonify(response[0]), response[1]

@borrow_bp.route('/renew/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def renew_book(transaction_id):
    """
    Renew a book (extend the due date).
    
    Parameters:
    - transaction_id: ID of the transaction
    
    Returns:
        - JSON response with success or error message.
    """
    response = renew_book_service(transaction_id)
    return jsonify(response[0]), response[1]

@borrow_bp.route('/overdue-books', methods=['GET'])
@jwt_required()
def check_overdue_books():
    """
    Check for overdue books and calculate fines.
    
    Returns:
        - JSON response with list of overdue books or error message.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    
    response = check_overdue_books_service()
    return jsonify(response[0]), response[1]

@borrow_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout_book_route():
    """
    Check out a book for the member.
    
    Members can only check out books for themselves.
    """
    # Check if the user has member role
    claims = get_jwt()
    if claims.get("role") != "Member":
        return jsonify({"error": "Unauthorized: Member role required"}), 403
    
    data = request.json
    if not data or not all(key in data for key in ('user_barcode', 'book_barcode')):
        return jsonify({"error": "Missing required fields"}), 400
    
    response = checkout_book_service(data['user_barcode'], data['book_barcode'])
    return jsonify(response[0]), response[1]

#####################two routes I was missing in the requirements############################################
#o The system should retrieve information about checked-out books and borrowing history.

@borrow_bp.route('/users/<int:user_id>/borrowing-history', methods=['GET'])
@jwt_required()
def get_borrowing_history(user_id):
    """
    Retrieve borrowing history for a specific user.
    
    Arguments:
    - user_id: The ID of the user.
    
    Returns:
    - JSON response with the user's borrowing history.
    """
    response = get_borrowing_history_service(user_id)
    return jsonify(response[0]), response[1]

@borrow_bp.route('/users/<int:user_id>/checked-out-books', methods=['GET'])
@jwt_required()
def get_checked_out_books(user_id):
    """
    Retrieve currently checked-out books for a specific user.
    
    Arguments:
    - user_id: The ID of the user.
    
    Returns:
    - JSON response with the user's currently checked-out books.
    """
    response = get_checked_out_books_service(user_id)
    return jsonify(response[0]), response[1]