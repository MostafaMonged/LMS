# Library Management System (LMS)

A comprehensive Library Management System built with Flask that allows library members to search, check-out, and return books, while providing functionalities for librarians to manage books and users.

## Installation and Setup Guide

Follow these steps to set up the Library Management System on your local machine:

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository and open LMS directory (the project root)**

2. **Create and activate a virtual environment**

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin activate
```

3. **Install required dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize the database**

After installing the dependencies, you need to set up the database with these commands:

```bash
flask db init      # Initialize migrations directory if not present
flask db migrate   # Create migration script based on models
flask db upgrade   # Apply migrations to create the database
```

## Required Dependencies

All dependencies are listed in requirements.txt.

## Project Structure

```
LMS/
├── app/                    # Application package
│   ├── models/             # Database models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── views/              # Frontend views
│   ├── static/             # Static assets
│   ├── templates/          # HTML templates
│   ├── __init__.py         # Application initialization
│   └── config.py           # Configuration settings
│
├── Deliverables/           # Documentation
│   ├── API Documentation/  # API endpoints documentation
│   └── Database Documentation/ # Database schema documentation
│
├── instance/               # Instance-specific data
│   ├── library.db          # Main database will appear when you run db initialization flask migration commands
│   └── test.db             # Test database
│
├── migrations/             # Database migrations
│   └── versions/           # Migration scripts
│
├── tests/                  # Test suites
│   ├── conftest.py         # Test configuration
│   ├── test_auth.py        # Authentication tests
│   ├── test_book_management.py # Book management tests
│   ├── test_borrow.py      # Borrowing functionality tests
│   └── test_search.py      # Search functionality tests
│
├── pytest.ini              # Pytest configurations
├── requirements.txt        # All dependencies needed
└── run.py                  # Application entry point
```

## Run Commands

### Starting the Flask Server

To start the Flask development server:

```bash
python run.py
```

By default, the server will run on `http://127.0.0.1:5000`.

## Sample API Commands

### Linux/macOS Commands

#### Authentication

**Register a librarian user:**
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Ahmed Librarian", "email": "ahmed@library.com", "password": "password123", "role": "Librarian"}'
```

**Register a member user:**
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Mostafa Member", "email": "mostafa@example.com", "password": "password123", "role": "Member"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "ahmed@library.com", "password": "password123"}'
```

**Store the returned token:**
```bash
export TOKEN="use the returned access_token from login here"
```

#### API Endpoints

**Search for books by title:**
```bash
curl -X GET "http://127.0.0.1:5000/api/search/books?title=Gatsby" 
```

**Get all users:**
```bash
curl -X GET http://127.0.0.1:5000/api/users
```

**Add a new book (requires Librarian token):**
```bash
curl -X POST http://127.0.0.1:5000/api/books \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "subject_category": "Fiction", "publication_date": "1925-04-10"}'
```

### Windows PowerShell Commands

#### Authentication

**Register a librarian user:**
```powershell
curl -X POST http://127.0.0.1:5000/auth/register `
  -H "Content-Type: application/json" `
  -d '{"name": "Ahmed Librarian", "email": "ahmed@library.com", "password": "password123", "role": "Librarian"}'
```

**Register a member user:**
```powershell
curl -X POST http://127.0.0.1:5000/auth/register `
  -H "Content-Type: application/json" `
  -d '{"name": "Mostafa Member", "email": "mostafa@example.com", "password": "password123", "role": "Member"}'
```

**Login:**
```powershell
curl -X POST http://127.0.0.1:5000/auth/login `
  -H "Content-Type: application/json" `
  -d '{"email": "ahmed@library.com", "password": "password123"}'
```

**Store the returned token:**
```powershell
$env:TOKEN="use the returned access_token from login here"
```

#### API Endpoints

**Search for books by title:**
```powershell
curl -X GET "http://127.0.0.1:5000/api/search/books?title=Gatsby" 
```

**Get all users:**
```powershell
curl -X GET http://127.0.0.1:5000/api/users
```

**Add a new book (requires Librarian token):**
```powershell
curl -X POST http://127.0.0.1:5000/api/books `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer $env:TOKEN" `
  -d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "subject_category": "Fiction", "publication_date": "1925-04-10"}'
```

## Running Tests

The project includes comprehensive tests written with pytest. Here's how to run them:

**Run all tests:**
```bash
pytest
```

**Run specific test categories (with pytest markers):**
```bash
pytest -m auth # to run all authentication tests
pytest -m user_management # to run all user_management tests
pytest -m book_management # to run all book_management tests
pytest -m borrowing # to run all borrowing tests
pytest -m search # to run all search tests
```

**Tests logs:**

For information about tests logs you will find generated log files under **tests/logs/**

## Additional Resources in Deliverables Directory

- API Documentation - Details of all API endpoints
- Database Documentation - Database structure and relationships