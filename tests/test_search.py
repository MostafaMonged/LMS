import pytest
import logging

class TestSearchBooks:
    """
    Test cases for searching books.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_books(self, test_client):
        """
        Class-level setup for TestSearchBooks.
        Registers a librarian, logs in, and adds books to the database for testing search functionality.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Search",
            "email": "librarian_search@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian_search@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add books for testing
        books = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "subject_category": "Fiction",
                "publication_date": "1925-04-10"
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "subject_category": "Fiction",
                "publication_date": "1960-07-11"
            },
            {
                "title": "A Brief History of Time",
                "author": "Stephen Hawking",
                "subject_category": "Science",
                "publication_date": "1988-03-01"
            },

        ]
        for book in books:
            response = test_client.post('/api/books', json=book, headers=headers)
            assert response.status_code == 201, f"Failed to add book: {book['title']}"

        logging.info("Books added successfully for TestSearchBooks.")

    @pytest.mark.search
    def test_search_by_title(self, test_client):
        """
        Test searching books by title.
        """
        response = test_client.get('/api/search/books?title=The Great Gatsby')
        logging.info(f"Search by Title - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 1
        assert response.json['books'][0]['title'] == "The Great Gatsby"

    @pytest.mark.search
    def test_search_by_author(self, test_client):
        """
        Test searching books by author.
        """
        response = test_client.get('/api/search/books?author=Harper Lee')
        logging.info(f"Search by Author - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 1
        assert response.json['books'][0]['author'] == "Harper Lee"

    @pytest.mark.search
    def test_search_by_subject_category(self, test_client):
        """
        Test searching books by subject category.
        """
        response = test_client.get('/api/search/books?subject_category=Science')
        logging.info(f"Search by Subject Category - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 1
        assert response.json['books'][0]['subject_category'] == "Science"

    @pytest.mark.search
    def test_search_by_publication_date(self, test_client):
        """
        Test searching books by publication date.
        """
        response = test_client.get('/api/search/books?publication_date=1925-04-10')
        logging.info(f"Search by Publication Date - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 1
        assert response.json['books'][0]['publication_date'] == "1925-04-10"

    @pytest.mark.search
    def test_search_with_multiple_filters(self, test_client):
        """
        Test searching books with multiple filters (title and author).
        """
        response = test_client.get('/api/search/books?title=The Great Gatsby&author=F. Scott Fitzgerald')
        logging.info(f"Search with Multiple Filters - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 1
        assert response.json['books'][0]['title'] == "The Great Gatsby"
        assert response.json['books'][0]['author'] == "F. Scott Fitzgerald"

    @pytest.mark.search
    def test_search_with_no_filters(self, test_client):
        """
        Test searching books with no filters (should return all books).
        """
        response = test_client.get('/api/search/books')
        logging.info(f"Search with No Filters - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 3  # All books added in setup

    @pytest.mark.search
    def test_search_with_no_results(self, test_client):
        """
        Test searching books with filters that yield no results.
        """
        response = test_client.get('/api/search/books?title=Nonexistent Book')
        logging.info(f"Search with No Results - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json['books']) == 0