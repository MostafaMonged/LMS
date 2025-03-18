import pytest
import logging

@pytest.mark.auth
def test_register_member(test_client):
    """
    Test registering a valid member.
    """
    payload = {
        "name": "Mostafa",
        "email": "mostafa@example.com",
        "password": "password123",
        "role": "Member"
    }
    response = test_client.post('/auth/register', json=payload)
    logging.info(f"Test Register Member - Input: {payload} - Output: {response.json}")
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully"


@pytest.mark.auth
def test_register_librarian(test_client):
    """
    Test registering a valid librarian.
    """
    payload = {
        "name": "Ahmed",
        "email": "ahmed@library.com",
        "password": "password123",
        "role": "Librarian"
    }
    response = test_client.post('/auth/register', json=payload)
    logging.info(f"Test Register Librarian - Input: {payload} - Output: {response.json}")
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully"


@pytest.mark.auth
def test_register_invalid_librarian_email(test_client):
    """
    Test registering a librarian with an invalid email.
    """
    payload = {
        "name": "InvalidLibrarian",
        "email": "invalid@example.com",  # Invalid email for librarian
        "password": "password123",
        "role": "Librarian"
    }
    response = test_client.post('/auth/register', json=payload)
    logging.info(f"Test Register Invalid Librarian Email - Input: {payload} - Output: {response.json}")
    assert response.status_code == 400
    assert "Invalid email" in response.json['error']


@pytest.mark.auth
def test_register_duplicate_email(test_client):
    """
    Test registering a user with a duplicate email.
    """
    payload = {
        "name": "DuplicateUser",
        "email": "duplicate@example.com",
        "password": "password123",
        "role": "Member"
    }
    # Register the first user
    test_client.post('/auth/register', json=payload)

    # Attempt to register the same email again
    response = test_client.post('/auth/register', json=payload)
    logging.info(f"Test Register Duplicate Email - Input: {payload} - Output: {response.json}")
    assert response.status_code == 400
    assert "A user with this email already exists" in response.json['error']


@pytest.mark.auth
def test_login_valid_credentials(test_client):
    """
    Test logging in with valid credentials.
    """
    # Register a user
    payload = {
        "name": "LoginUser",
        "email": "loginuser@example.com",
        "password": "password123",
        "role": "Member"
    }
    test_client.post('/auth/register', json=payload)

    # Login with the same credentials
    login_payload = {
        "email": "loginuser@example.com",
        "password": "password123"
    }
    response = test_client.post('/auth/login', json=login_payload)
    logging.info(f"Test Login Valid Credentials - Input: {login_payload} - Output: {response.json}")
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


@pytest.mark.auth
def test_login_invalid_credentials(test_client):
    """
    Test logging in with invalid credentials.
    """
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = test_client.post('/auth/login', json=login_payload)
    logging.info(f"Test Login Invalid Credentials - Input: {login_payload} - Output: {response.json}")
    assert response.status_code == 401
    assert "Invalid credentials" in response.json['error']


@pytest.mark.auth
def test_token_refresh_valid(test_client):
    """
    Test refreshing a valid token.
    """
    # Register and login a user
    payload = {
        "name": "RefreshUser",
        "email": "refreshuser@example.com",
        "password": "password123",
        "role": "Member"
    }
    test_client.post('/auth/register', json=payload)
    login_response = test_client.post('/auth/login', json={"email": payload["email"], "password": payload["password"]})
    refresh_token = login_response.json['refresh_token']

    # Refresh the token
    response = test_client.post('/auth/refresh', headers={"Authorization": f"Bearer {refresh_token}"})
    logging.info(f"Test Token Refresh - Output: {response.json}")
    assert response.status_code == 200
    assert "access_token" in response.json

