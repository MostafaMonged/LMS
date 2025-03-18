import pytest
import logging


class TestAddBook:
    """
    Test cases for adding books.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestAddBook.
        Fixture to register and log in as a librarian, returning the authorization headers.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian One",
            "email": "librarian1@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian1@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}
        logging.info("Librarian registered and logged in successfully for TestAddBook.")
        return headers

    @pytest.mark.book_management
    def test_add_book(self, test_client,setup_headers):
        """
        Test adding a new book.
        """
        book_data = {
            "title": "Book Three",
            "author": "Author Three",
            "subject_category": "History",
            "publication_date": "2019-07-20"
        }
        response = test_client.post('/api/books', json=book_data, headers=setup_headers)
        logging.info(f"Test Add Book - Input: {book_data} - Output: {response.json}")
        assert response.status_code == 201
        assert response.json['message'] == "Book added successfully"

    @pytest.mark.book_management
    def test_add_book_missing_fields(self, test_client, setup_headers):
        """
        Test adding a book with missing required fields.
        """
        incomplete_book_data = {
            "title": "Incomplete Book"
        }
        response = test_client.post('/api/books', json=incomplete_book_data, headers=setup_headers)
        logging.info(f"Test Add Book Missing Fields - Input: {incomplete_book_data} - Output: {response.json}")
        assert response.status_code == 400
        assert "Missing required fields" in response.json['error']
    
    @pytest.mark.book_management
    def test_add_duplicate_book(self, test_client, setup_headers):
        """
        Test adding a duplicate book (same title and author).
        """
        book_data = {
            "title": "Book Three",
            "author": "Author Three",
            "subject_category": "History",
            "publication_date": "2019-07-20"
        }
        # Attempt to add the same book again
        duplicate_response = test_client.post('/api/books', json=book_data, headers=setup_headers)
        logging.info(f"Test Add Duplicate Book - Input: {book_data} - Output: {duplicate_response.json}")
        assert duplicate_response.status_code == 400
        assert "already exists" in duplicate_response.json['error']


class TestGetBooks:
    """
    Test cases for fetching all books.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestGetBooks.
        Fixture to register and log in as a librarian, returning the authorization headers.
        Also adds books for testing.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Four",
            "email": "librarian4@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian4@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add books for testing
        books = [
            {
                "title": "Book Five",
                "author": "Author Five",
                "subject_category": "Philosophy",
                "publication_date": "2017-03-15"
            },
            {
                "title": "Book Six",
                "author": "Author Six",
                "subject_category": "Mathematics",
                "publication_date": "2016-09-10"
            }
        ]
        for book in books:
            response = test_client.post('/api/books', json=book, headers=headers)
            assert response.status_code == 201, f"Failed to add book: {book['title']}"

        logging.info("Books added successfully for TestGetBooks.")
        return headers

    @pytest.mark.book_management
    def test_get_all_books(self, test_client, setup_headers):
        """
        Test fetching all books.
        """
        response = test_client.get('/api/books', headers=setup_headers)
        logging.info(f"Test Get All Books - Output: {response.json}")
        assert response.status_code == 200
        assert "books" in response.json
        assert len(response.json['books']) >= 2, "Expected at least 2 books in the catalog"

    @pytest.mark.book_management
    def test_get_book_by_barcode(self, test_client, setup_headers):
        """
        Test fetching a book by barcode.
        """
        # Fetch all books to get a valid barcode
        all_books_response = test_client.get('/api/books', headers=setup_headers)
        assert all_books_response.status_code == 200, "Failed to fetch all books"
        barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode
        response = test_client.get(f'/api/books/{barcode}', headers=setup_headers)
        logging.info(f"Test Get Book by Barcode - Output: {response.json}")
        assert response.status_code == 200, "Failed to fetch book by barcode"


class TestModifyBook:
    """
    Test cases for modifying books.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestModifyBook.
        Fixture to register and log in as a librarian, returning the authorization headers.
        Also adds books for testing modifications.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Two",
            "email": "librarian2@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian2@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add books for testing modifications
        books = [
            {
                "title": "Book One",
                "author": "Author One",
                "subject_category": "Fiction",
                "publication_date": "2020-01-01"
            },
            {
                "title": "Book Two",
                "author": "Author Two",
                "subject_category": "Science",
                "publication_date": "2021-05-15"
            }
        ]
        for book in books:
            response = test_client.post('/api/books', json=book, headers=headers)
            assert response.status_code == 201, f"Failed to add book: {book['title']}"

        logging.info("Books added successfully for TestModifyBook.")
        return headers

    @pytest.mark.book_management
    def test_modify_book(self, test_client, setup_headers):
        """
        Test modifying an existing book.
        """
        # Fetch all books to get a valid barcode
        all_books_response = test_client.get('/api/books', headers=setup_headers)
        assert all_books_response.status_code == 200, "Failed to fetch all books"
        barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode

        # Modify the book
        updated_data = {
            "title": "Updated Book Title",
            "author": "Updated Author"
        }
        response = test_client.put(f'/api/books/{barcode}', json=updated_data, headers=setup_headers)
        logging.info(f"Test Modify Book - Input: {updated_data} - Output: {response.json}")
        assert response.status_code == 200
        assert response.json['message'] == "Book updated successfully"

    @pytest.mark.book_management
    def test_modify_nonexistent_book(self, test_client, setup_headers):
        """
        Test modifying a book that does not exist.
        """
        nonexistent_barcode = "NONEXISTENT123"
        updated_data = {
            "title": "Nonexistent Book",
            "author": "Nonexistent Author"
        }
        response = test_client.put(f'/api/books/{nonexistent_barcode}', json=updated_data, headers=setup_headers)
        logging.info(f"Test Modify Nonexistent Book - Input: {updated_data} - Output: {response.json}")
        assert response.status_code == 404
        assert "Book not found" in response.json['error']


class TestDeleteBook:
    """
    Test cases for deleting books.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestDeleteBook.
        Fixture to register and log in as a librarian, returning the authorization headers.
        Also adds books for testing deletions.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Three",
            "email": "librarian3@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian3@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add books for testing deletions
        books = [
            {
                "title": "Book Three",
                "author": "Author Three",
                "subject_category": "History",
                "publication_date": "2019-07-20"
            },
            {
                "title": "Book Four",
                "author": "Author Four",
                "subject_category": "Technology",
                "publication_date": "2018-11-11"
            }
        ]
        for book in books:
            response = test_client.post('/api/books', json=book, headers=headers)
            assert response.status_code == 201, f"Failed to add book: {book['title']}"

        logging.info("Books added successfully for TestDeleteBook.")
        return headers

    @pytest.mark.book_management
    def test_delete_book(self, test_client, setup_headers):
        """
        Test deleting a book and all its copies.
        """
        # Fetch all books to get a valid barcode
        all_books_response = test_client.get('/api/books', headers=setup_headers)
        assert all_books_response.status_code == 200, "Failed to fetch all books"
        barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode

        # Delete the book
        response = test_client.delete(f'/api/books/{barcode}', headers=setup_headers)
        logging.info(f"Test Delete Book - Output: {response.json}")
        assert response.status_code == 200
        assert response.json['message'] == "Book and all its copies deleted successfully"

        # Verify the book is deleted
        verify_response = test_client.get(f'/api/books/{barcode}', headers=setup_headers)
        assert verify_response.status_code == 404, "Deleted book still exists"

    @pytest.mark.book_management
    def test_delete_nonexistent_book(self, test_client, setup_headers):
        """
        Test deleting a book that does not exist.
        """
        nonexistent_barcode = "NONEXISTENT123"
        response = test_client.delete(f'/api/books/{nonexistent_barcode}', headers=setup_headers)
        logging.info(f"Test Delete Nonexistent Book - Output: {response.json}")
        assert response.status_code == 404
        assert "Book not found" in response.json['error']


class TestCreateBookCopy:
    """
    Test cases for creating book copies.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestCreateBookCopy.
        Fixture to register and log in as a librarian, returning the authorization headers.
        Also adds a book for testing book copies.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Nine",
            "email": "librarian9@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian9@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add a book for testing
        book_data = {
            "title": "Book Eleven",
            "author": "Author Eleven",
            "subject_category": "Fantasy",
            "publication_date": "2011-04-12"
        }
        response = test_client.post('/api/books', json=book_data, headers=headers)
        assert response.status_code == 201, "Failed to add book for testing book copies"

        logging.info("Book added successfully for TestCreateBookCopy.")
        return headers

    @pytest.mark.book_management
    def test_create_book_copy(self, test_client, setup_headers):
        """
        Test creating a new book copy for an existing book.
        """
        # Fetch the book to get its barcode
        all_books_response = test_client.get('/api/books', headers=setup_headers)
        assert all_books_response.status_code == 200, "Failed to fetch all books"
        barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode

        # Add a book copy
        copy_data = {
            "rack_location": "A1"
        }
        response = test_client.post(f'/api/book_copies/{barcode}', json=copy_data, headers=setup_headers)
        logging.info(f"Test Create Book Copy - Input: {copy_data} - Output: {response.json}")
        assert response.status_code == 201
        assert response.json['message'] == "Book copy created successfully"

    @pytest.mark.book_management
    def test_create_book_copy_nonexistent_book(self, test_client, setup_headers):
        """
        Test creating a book copy for a nonexistent book.
        """
        nonexistent_barcode = "NONEXISTENT123"
        copy_data = {
            "rack_location": "B2"
        }
        response = test_client.post(f'/api/book_copies/{nonexistent_barcode}', json=copy_data, headers=setup_headers)
        logging.info(f"Test Create Book Copy Nonexistent Book - Input: {copy_data} - Output: {response.json}")
        assert response.status_code == 404
        assert "Book not found" in response.json['error']


class TestModifyBookCopy:
    """
    Test cases for modifying book copies.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestModifyBookCopy.
        Fixture to register and log in as a librarian, returning the authorization headers.
        Also adds a book and a book copy for testing modifications.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Ten",
            "email": "librarian10@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian10@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add a book for testing
        book_data = {
            "title": "Book Twelve",
            "author": "Author Twelve",
            "subject_category": "Mystery",
            "publication_date": "2010-02-18"
        }
        response = test_client.post('/api/books', json=book_data, headers=headers)
        assert response.status_code == 201, "Failed to add book for testing book copies"

        # Add a book copy
        barcode = response.json['barcode']
        copy_data = {
            "rack_location": "C3"
        }
        copy_response = test_client.post(f'/api/book_copies/{barcode}', json=copy_data, headers=headers)
        assert copy_response.status_code == 201, "Failed to add book copy for testing modifications"

        logging.info("Book and book copy added successfully for TestModifyBookCopy.")
        return headers

    @pytest.mark.book_management
    def test_modify_book_copy(self, test_client, setup_headers):
        """
        Test modifying an existing book copy.
        """
        # Fetch the book to get its barcode
        all_books_response = test_client.get('/api/books', headers=setup_headers)
        assert all_books_response.status_code == 200, "Failed to fetch all books"
        barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode

        # Fetch the book copies to get a valid copy ID
        copies_response = test_client.get(f'/api/book_copies/{barcode}', headers=setup_headers)
        assert copies_response.status_code == 200, "Failed to fetch book copies"
        copy_id = copies_response.json['book_copies'][0]['id']  # Use the first copy's ID

        # Modify the book copy
        updated_data = {
            "rack_location": "D4",
            "is_available": False
        }
        response = test_client.put(f'/api/book_copies/{barcode}/{copy_id}', json=updated_data, headers=setup_headers)
        logging.info(f"Test Modify Book Copy - Input: {updated_data} - Output: {response.json}")
        assert response.status_code == 200
        assert response.json['message'] == "Book copy modified successfully"

    @pytest.mark.book_management
    def test_modify_book_copy_nonexistent(self, test_client, setup_headers):
        """
        Test modifying a nonexistent book copy.
        """
        nonexistent_barcode = "NONEXISTENT123"
        nonexistent_copy_id = 9999
        updated_data = {
            "rack_location": "E5",
            "is_available": True
        }
        response = test_client.put(f'/api/book_copies/{nonexistent_barcode}/{nonexistent_copy_id}', json=updated_data, headers=setup_headers)
        logging.info(f"Test Modify Nonexistent Book Copy - Input: {updated_data} - Output: {response.json}")
        assert response.status_code == 404
        assert "Book not found" in response.json['error']

class TestDeleteBookCopy:
    """
    Test cases for deleting book copies.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_headers(self, test_client):
        """
        Class-level setup for TestDeleteBookCopy.
        Fixture to register and log in as a librarian, returning the authorization headers.
        Also adds a book and a book copy for testing deletions.
        """
        # Register the librarian
        librarian_data = {
            "name": "Librarian Eleven",
            "email": "librarian11@library.com",
            "password": "password123",
            "role": "Librarian"
        }
        register_response = test_client.post('/auth/register', json=librarian_data)
        assert register_response.status_code == 201, "Failed to register Librarian"

        # Log in as the librarian
        login_credentials = {
            "email": "librarian11@library.com",
            "password": "password123"
        }
        login_response = test_client.post('/auth/login', json=login_credentials)
        assert login_response.status_code == 200, "Failed to log in as Librarian"
        auth_token = login_response.json['access_token']
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Add a book for testing
        book_data = {
            "title": "Book Thirteen",
            "author": "Author Thirteen",
            "subject_category": "Biography",
            "publication_date": "2009-01-10"
        }
        response = test_client.post('/api/books', json=book_data, headers=headers)
        assert response.status_code == 201, "Failed to add book for testing book copies"

        # Add a book copy
        barcode = response.json['barcode']
        copy_data = {
            "rack_location": "B2",
        }
        copy_response = test_client.post(f'/api/book_copies/{barcode}', json=copy_data, headers=headers)
        assert copy_response.status_code == 201, "Failed to add book copy for testing deletions"

        logging.info("Book and book copy added successfully for TestDeleteBookCopy.")
        return headers

    @pytest.mark.book_management
    def test_delete_book_copy(self, test_client, setup_headers):
        """
        Test deleting an existing book copy.
        """
        # Fetch the book to get its barcode
        all_books_response = test_client.get('/api/books', headers=setup_headers)
        assert all_books_response.status_code == 200, "Failed to fetch all books"
        barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode

        # Fetch the book copies to get a valid copy ID
        copies_response = test_client.get(f'/api/book_copies/{barcode}', headers=setup_headers)
        assert copies_response.status_code == 200, "Failed to fetch book copies"
        copy_id = copies_response.json['book_copies'][0]['id']  # Use the first copy's ID

        # Delete the book copy
        response = test_client.delete(f'/api/book_copies/{barcode}/{copy_id}', headers=setup_headers)
        logging.info(f"Test Delete Book Copy - Output: {response.json}")
        assert response.status_code == 200
        assert response.json['message'] == "Book copy deleted successfully"

    @pytest.mark.book_management
    def test_delete_book_copy_nonexistent(self, test_client, setup_headers):
        """
        Test deleting a nonexistent book copy.
        """
        nonexistent_barcode = "NONEXISTENT123"
        nonexistent_copy_id = 9999
        response = test_client.delete(f'/api/book_copies/{nonexistent_barcode}/{nonexistent_copy_id}', headers=setup_headers)
        logging.info(f"Test Delete Nonexistent Book Copy - Output: {response.json}")
        assert response.status_code == 404
        assert "not found" in response.json['error']

    #needs more setup but it works
    # @pytest.mark.book_management
    # def test_delete_book_copy_unavailable(self, test_client, setup_headers):
    #     """
    #     Test deleting a book copy that is unavailable (checked out).
    #     """
    #     # Fetch the book to get its barcode
    #     all_books_response = test_client.get('/api/books', headers=setup_headers)
    #     assert all_books_response.status_code == 200, "Failed to fetch all books"
    #     barcode = all_books_response.json['books'][0]['barcode']  # Use the first book's barcode

    #     # Fetch the book copies to get a valid copy ID
    #     copies_response = test_client.get(f'/api/book_copies/{barcode}', headers=setup_headers)
    #     assert copies_response.status_code == 200, "Failed to fetch book copies"
    #     copy_id = copies_response.json['book_copies'][0]['id']  # Use the first copy's ID

    #     # Simulate the book copy being checked out
    #     modify_response = test_client.put(
    #         f'/api/book_copies/{barcode}/{copy_id}',
    #         json={"is_available": False},
    #         headers=setup_headers
    #     )
    #     assert modify_response.status_code == 200, "Failed to modify book copy to unavailable"

    #     # Attempt to delete the unavailable book copy
    #     delete_response = test_client.delete(f'/api/book_copies/{barcode}/{copy_id}', headers=setup_headers)
    #     logging.info(f"Test Delete Unavailable Book Copy - Output: {delete_response.json}")
    #     assert delete_response.status_code == 400
    #     assert "Cannot delete a book copy that is currently checked out" in delete_response.json['error']