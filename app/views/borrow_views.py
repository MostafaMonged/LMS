from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

borrow_view_bp = Blueprint("borrow_view", __name__)

@borrow_view_bp.route('/issue-book')
@jwt_required()
def issue_book_page():
    return render_template('issue_book.html')

@borrow_view_bp.route('/return-book')
@jwt_required()
def return_book_page():
    return render_template('return_book.html')