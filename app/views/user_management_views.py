from flask import render_template, redirect, url_for, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt

# Blueprint setup
user_management_view_bp = Blueprint('user_management_views', __name__)

@user_management_view_bp.route('/librarian-dashboard')
@jwt_required()  # Protect this route with JWT authentication
def librarian_dashboard_page():
    """
    Renders the librarian dashboard where users can manage user data.
    This view is accessible only by a librarian.
    """
    # Get the role from the JWT token
    current_user = get_jwt()
    print(f"Current user: {current_user}")  

    # # The role will be in the 'role' claim in the JWT payload
    # user_role = current_user.get('role')  # Extract the role from the JWT token

    # if user_role != 'Librarian':
    #     return redirect(url_for('user_management_views.unauthorized_page'))
        
    # Return the rendered template
    return render_template('librarian_dashboard.html')

@user_management_view_bp.route('/unauthorized')
def unauthorized_page():
    """
    Renders a page to indicate that the user doesn't have the right permissions.
    """
    return render_template('unauthorized.html')

# Route to display the member dashboard
@user_management_view_bp.route('/member-dashboard')
@jwt_required()  # Protect this route with JWT authentication
def member_dashboard_page():
    """
    Renders the member dashboard where users can manage user data.
    """
    # Get the role from the JWT token
    current_user = get_jwt()
    return render_template('member_dashboard.html')