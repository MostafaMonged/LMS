# app/services/search_service.py
from app.models.Book import Book
from app.models.BookCopy import BookCopy

def search_books(query_params):
    """
    Search for books based on query parameters.
    
    Arguments:
    - query_params: Dictionary containing search parameters (title, author, subject_category, publication_date)
    
    Returns:
    - A tuple containing the search results and HTTP status code.
    """
    try:
        # Start with a base query
        query = Book.query
        
        # Apply filters based on provided parameters
        if 'title' in query_params and query_params['title']:
            query = query.filter(Book.title.ilike(f"%{query_params['title']}%"))
            
        if 'author' in query_params and query_params['author']:
            query = query.filter(Book.author.ilike(f"%{query_params['author']}%"))
            
        if 'subject_category' in query_params and query_params['subject_category']:
            query = query.filter(Book.subject_category.ilike(f"%{query_params['subject_category']}%"))
            
        if 'publication_date' in query_params and query_params['publication_date']:
            query = query.filter(Book.publication_date == query_params['publication_date'])
        
        # Execute the query and get results
        books = query.all()
        
        # Format the results
        results = []
        for book in books:
            # Count available copies
            available_copies = BookCopy.query.filter_by(book_id=book.id, is_available=True).count()
            total_copies = BookCopy.query.filter_by(book_id=book.id).count()
            
            results.append({
                'id': book.id,
                'barcode': book.barcode,
                'title': book.title,
                'author': book.author,
                'subject_category': book.subject_category,
                'publication_date': book.publication_date.strftime('%Y-%m-%d'),
                'available_copies': available_copies,
                'total_copies': total_copies
            })
        
        return {'books': results}, 200
        
    except Exception as e:
        return {'error': f'An error occurred: {str(e)}'}, 500