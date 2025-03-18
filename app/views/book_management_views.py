from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

book_management_view_bp = Blueprint("book_management_view", __name__)

@book_management_view_bp.route('/books')
@jwt_required()
def books_management_page():
    return render_template('book_management.html')
