from flask import jsonify, Blueprint, request
from app.services.user_management_service import get_all_users,delete_user_by_barcode,get_user_by_barcode,get_user_notifications_service
from flask_jwt_extended import jwt_required

user_management_bp = Blueprint('user_management', __name__)

# Route to fetch all users
@user_management_bp.route("/users", methods=["GET"])
def get_users():
    """
    Fetch all users.

    Returns:
        A JSON response with a list of users.
    """
    response = get_all_users()
    return jsonify(response[0]), response[1]


# Route to fetch user details by barcode
@user_management_bp.route('/users/barcode/<string:barcode>', methods=['GET'])
def get_user_details(barcode):
    """
    Fetch user details by user ID.

    Returns:
        A JSON response with user details or an error message.
    """
    response = get_user_by_barcode(barcode)
    return jsonify(response[0]), response[1]


@user_management_bp.route("/users", methods=["DELETE"])
def delete_user_route():
    """
    Delete a user by barcode.

    Returns:
        A JSON response with a message indicating success or failure.
    """
    barcode = request.json.get('barcode')
    if not barcode:
        return jsonify({"error": "Barcode is required"}), 400
    
    response = delete_user_by_barcode(barcode)
    return jsonify(response[0]), response[1]



@user_management_bp.route('/users/<string:barcode>/notifications', methods=['GET'])
@jwt_required()
def get_user_notifications(barcode):
    """
    Get notifications for a specific user.
    
    Arguments:
    - barcode: The ID of the user.
    
    Returns:
    - JSON response with the user's notifications.
    """
    response = get_user_notifications_service(barcode)
    return jsonify(response[0]), response[1]