# app/routes/search_routes.py
from flask import Blueprint, request, jsonify
from app.services.search_service import search_books
#from flask_jwt_extended import jwt_required

search_bp = Blueprint('search', __name__)

@search_bp.route('/search/books', methods=['GET'])
# @jwt_required()
#any one can search so i removed jwt_required
def search_books_route():
    """
    Search for books based on query parameters.
    
    Query Parameters:
    - title: Title of the book
    - author: Author of the book
    - subject_category: Subject category of the book
    - publication_date: Publication date of the book (YYYY-MM-DD)
    
    Returns:
    - JSON response with search results.
    """
    # Get query parameters
    query_params = {
        'title': request.args.get('title'),
        'author': request.args.get('author'),
        'subject_category': request.args.get('subject_category'),
        'publication_date': request.args.get('publication_date')
    }
    
    response = search_books(query_params)
    return jsonify(response[0]), response[1]