from flask import Blueprint,request, jsonify
from app.services.book_management_service import add_book_service,delete_book_service, modify_book_service,create_book_copy_service, delete_book_copy_service, modify_book_copy_service,get_all_books_service,get_book_by_barcode_service,get_book_copies_service
from flask_jwt_extended import jwt_required, get_jwt

# Create a Blueprint for book-related routes
book_management_bp = Blueprint("book_management", __name__)  


#Route for getting all books
@book_management_bp.route('/books', methods=['GET'])
@jwt_required()
def get_all_books():
    """
    Fetch all books from the catalog.

    Returns:
        - JSON response with the list of books or an error message.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    response = get_all_books_service()
    return jsonify(response[0]), response[1]

#Route for getting book by barcode
@book_management_bp.route('/books/<string:barcode>', methods=['GET'])
@jwt_required()
def get_book_by_barcode(barcode):
    """
    Fetch a book by its barcode.

    Returns:
        - JSON response with the book details if exist.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    response = get_book_by_barcode_service(barcode)
    return jsonify(response[0]), response[1]

# Route for adding a new book
@book_management_bp.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    """
    Add a new book to the catalog.

    Expected JSON Data:
    - title: str (Title of the book)
    - author: str (Author of the book)
    - subject_category: str (Subject category of the book)
    - publication_date: str (Publication date of the book in YYYY-MM-DD format)

    Returns:
        A JSON response with success or error message.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    data = request.json  # Use request.json to handle the JSON body data
    response = add_book_service(data)
    return jsonify(response[0]), response[1]

# Route for modifying an existing book
@book_management_bp.route('/books/<barcode>', methods=['PUT'])
@jwt_required()
def modify_book(barcode):
    """
    Modify a book's details (e.g., title, author, etc.) using barcode.
    
    Parameters:
    - barcode: The unique barcode of the book
    
    Returns:
        - Success message or error message if book not found.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    data = request.json
    response = modify_book_service(barcode, data)
    return jsonify(response[0]), response[1]


@book_management_bp.route('/books/<barcode>', methods=['DELETE'])
@jwt_required()
def delete_book(barcode):
    """
    Delete a book by its barcode and remove all its copies.
    
    Parameters:
    - barcode: The unique barcode of the book
    
    Returns:
        - Success message or error message if book not found.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    response = delete_book_service(barcode)
    return jsonify(response[0]), response[1]




##########################################BOOK COPY MANAGEMENT ROUTES######################################################


# Route for adding a book copy
@book_management_bp.route('/book_copies/<barcode>', methods=['POST'])
@jwt_required()
def create_book_copy(barcode):
    """
    Create a new book copy using the barcode of the book.
    
    Parameters:
    - barcode: The unique barcode of the book
    
    Returns:
        - Success message or error message if book not found.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    data = request.json
    response = create_book_copy_service(barcode, data)
    return jsonify(response[0]), response[1]



# Route for removing a book copy
@book_management_bp.route('/book_copies/<barcode>/<int:copy_id>', methods=['DELETE'])
@jwt_required()
def delete_book_copy(barcode, copy_id):
    """
    Delete a book copy by its book barcode and copy ID.
    
    Parameters:
    - barcode: The unique barcode of the book
    - copy_id: The ID of the book copy to be deleted
    
    Returns:
        - Success message or error message if book or copy not found.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    response = delete_book_copy_service(barcode, copy_id)
    return jsonify(response[0]), response[1]

# Route for modifying a book copy
@book_management_bp.route('/book_copies/<barcode>/<int:copy_id>', methods=['PUT'])
@jwt_required()
def modify_book_copy(barcode, copy_id):
    """
    Modify a book copy by its barcode and copy ID.
    
    Parameters:
    - barcode: The unique barcode of the book
    - copy_id: The ID of the book copy to be modified
    
    Returns:
        - Success message or error message if book or copy not found.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    data = request.json
    response = modify_book_copy_service(barcode, copy_id, data)
    return jsonify(response[0]), response[1]

# Route for fetching all book copies for a given book barcode
@book_management_bp.route('/book_copies/<barcode>', methods=['GET'])
@jwt_required()
def get_book_copies(barcode):
    """
    Fetch all book copies for a given book barcode.

    Parameters:
    - barcode: The unique barcode of the book

    Returns:
        - JSON response with the list of book copies or an error message.
    """
    # Check if the user has librarian role
    claims = get_jwt()
    if claims.get("role") != "Librarian":
        return jsonify({"error": "Unauthorized: Librarian role required"}), 403
    response = get_book_copies_service(barcode)
    return jsonify(response[0]), response[1]