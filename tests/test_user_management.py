import pytest
import logging


@pytest.fixture(scope="module", autouse=True)
def setup_user_management_suite(test_client):
    """
    Module-scoped fixture for user management test suite.
    Populates the database with mock data.
    """
    logging.info("Setting up user management test suite...")

    # Register mock users
    users = [
        {
            "name": "Member One",
            "email": "member1@example.com",
            "password": "password123",
            "role": "Member"
        },
        {
            "name": "Member Two",
            "email": "member2@example.com",
            "password": "password123",
            "role": "Member"
        },
        {
            "name": "Librarian One",
            "email": "librarian1@library.com",
            "password": "password123",
            "role": "Librarian"
        }
    ]

    for user in users:
        response = test_client.post('/auth/register', json=user)
        assert response.status_code == 201, f"Failed to register user: {user['email']}"

    logging.info("User management test suite setup complete.")


class TestGetUsers:
    """
    Test cases for fetching users.
    """

    @pytest.mark.user_management
    def test_get_all_users(self, test_client):
        """
        Test fetching all users.
        """
        response = test_client.get('/api/users')
        logging.info(f"Test Get All Users - Output: {response.json}")
        assert response.status_code == 200
        assert len(response.json) >= 3, f"Expected at least 3 users, got {len(response.json)}"
        assert any(user['role'] == 'Member' for user in response.json), "No Member found in users"
        assert any(user['role'] == 'Librarian' for user in response.json), "No Librarian found in users"

    @pytest.mark.user_management
    def test_get_user_by_barcode(self, test_client):
        """
        Test fetching a user by their barcode.
        """
        # Fetch all users to get a valid barcode
        all_users_response = test_client.get('/api/users')
        assert all_users_response.status_code == 200, "Failed to fetch all users"
        barcode = all_users_response.json[0]['barcode']  # Use the first user's barcode

        # Fetch the user by barcode
        response = test_client.get(f'/api/users/barcode/{barcode}')
        logging.info(f"Test Get User By Barcode - Output: {response.json}")
        assert response.status_code == 200
        assert response.json['barcode'] == barcode, "Fetched user barcode does not match"

    @pytest.mark.user_management
    def test_get_user_by_invalid_barcode(self, test_client):
        """
        Test fetching a user with an invalid barcode.
        """
        invalid_barcode = "INVALID123"
        response = test_client.get(f'/api/users/barcode/{invalid_barcode}')
        logging.info(f"Test Get User By Invalid Barcode - Output: {response.json}")
        assert response.status_code == 404
        assert "User not found" in response.json['error']


class TestDeleteUsers:
    """
    Test cases for deleting users.
    """

    @pytest.mark.user_management
    def test_delete_member_by_barcode(self, test_client):
        """
        Test deleting a member by their barcode.
        """
        # Fetch all users to get a valid member barcode
        all_users_response = test_client.get('/api/users')
        assert all_users_response.status_code == 200, "Failed to fetch all users"
        member = next(user for user in all_users_response.json if user['role'] == 'Member')
        barcode = member['barcode']

        # Delete the member by barcode
        response = test_client.delete('/api/users', json={"barcode": barcode})
        logging.info(f"Test Delete Member By Barcode - Output: {response.json}")
        assert response.status_code == 200
        assert response.json['message'] == "User deleted successfully"

        # Verify the user is deleted
        verify_response = test_client.get(f'/api/users/barcode/{barcode}')
        assert verify_response.status_code == 404, "Deleted user still exists"

    @pytest.mark.user_management
    def test_prevent_deleting_librarian(self, test_client):
        """
        Test preventing deletion of a librarian.
        """
        # Fetch all users to get a valid librarian barcode
        all_users_response = test_client.get('/api/users')
        assert all_users_response.status_code == 200, "Failed to fetch all users"
        librarian = next(user for user in all_users_response.json if user['role'] == 'Librarian')
        barcode = librarian['barcode']

        # Attempt to delete the librarian
        response = test_client.delete('/api/users', json={"barcode": barcode})
        logging.info(f"Test Prevent Deleting Librarian - Output: {response.json}")
        assert response.status_code == 400
        assert "Cannot delete a Librarian" in response.json['error']

    @pytest.mark.user_management
    def test_delete_user_with_invalid_barcode(self, test_client):
        """
        Test deleting a user with an invalid barcode.
        """
        invalid_barcode = "INVALID123"
        response = test_client.delete('/api/users', json={"barcode": invalid_barcode})
        logging.info(f"Test Delete User With Invalid Barcode - Output: {response.json}")
        assert response.status_code == 404
        assert "User not found" in response.json['error']


# Skipped for now as it needs a user with notifications
# class TestUserNotifications:
#     """
#     Test cases for user notifications.
#     """
# 
#     @pytest.mark.user_management
#     def test_get_user_notifications(self, test_client):
#         """
#         Test fetching notifications for a specific user using their barcode.
#         """
#         # Fetch all users to get a valid barcode
#         all_users_response = test_client.get('/api/users')
#         assert all_users_response.status_code == 200, "Failed to fetch all users"
#         user = all_users_response.json[0]
#         barcode = user['barcode']  # Use the user's barcode
# 
#         # Fetch notifications for the user using their barcode
#         response = test_client.get(f'/api/users/barcode/{barcode}/notifications')
#         logging.info(f"Test Get User Notifications - Output: {response.json}")
#         assert response.status_code == 200
#         assert isinstance(response.json, list), "Notifications should be a list"