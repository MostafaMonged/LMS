import pytest
import logging
import os
from app import create_app, db



# Global variable to track the current log file
current_log_file = None

@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config):
    """
    Configure logging based on the marker of the test suite.
    This ensures all tests with the same marker log to the same file.
    """
    global current_log_file

    # Get the marker from the command-line arguments (e.g., pytest -m auth)
    marker = config.getoption("-m")
    if not marker:
        marker = "all"  # Default marker if none is provided

    # Determine the log file name based on the marker
    log_file = f"tests/logs/{marker}_tests.log"

    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Remove existing handlers to reconfigure logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Overwrite the log file for the suite
    current_log_file = log_file
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="w"  # Overwrite the log file for each test suite run
    )

    # Log the start of the test suite
    logging.info(f"Starting test suite for marker: {marker}")

@pytest.fixture(scope="module")
def test_client():
    """
    Set up the Flask test client and initialize the database.
    """
    app = create_app('app.config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
            yield client
            db.session.remove()
            db.drop_all()  # Drop tables after tests