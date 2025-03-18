from app.models.User import User, db


def get_all_users():
    """
    Handles fetching all users from the database.

    Returns:
        A tuple containing a list of users and HTTP status code.
    """
    try:
        users = User.query.all()
        user_list = [{
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "barcode": user.barcode
        } for user in users]

        return user_list, 200
    except Exception as e:
        return {"error": str(e)}, 500


def get_user_by_barcode(barcode):
    """
    Handles fetching a specific user from the database by barcode.

    Arguments:
    - barcode (str): The barcode of the user to fetch.

    Returns:
        A tuple containing user details or an error message with HTTP status code.
    """
    try:
        user = User.query.filter_by(barcode=barcode).first()
        if not user:
            return {"error": "User not found"}, 404
        
        return {
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "barcode": user.barcode
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500


def delete_user_by_barcode(barcode):
    """
    Handles deleting a user from the database by barcode.

    Arguments:
    - barcode (str): The barcode of the user to delete.

    Returns:
        A tuple containing a success message or an error message with HTTP status code.
    """
    try:
        user_to_delete = User.query.filter_by(barcode=barcode).first()
        if not user_to_delete:
            return {"error": "User not found"}, 404
        
        # Prevent deleting a librarian
        if user_to_delete.role == "Librarian":
            return {"error": "Cannot delete a Librarian"}, 400

        db.session.delete(user_to_delete)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return {"error": str(e)}, 500
    


def get_user_notifications_service(barcode):
    """
    Retrieve notifications for a specific user.
    
    Arguments:
    - barcode: The barcode of the user.
    
    Returns:
    - A tuple containing the notifications list and HTTP status code.
    """
    user = User.query.get(barcode)
    if not user:
        return {"error": "User not found"}, 404
    
    # Deserialize the notifications JSON string into a Python list
    notifications = user.get_notifications()
    return notifications, 200