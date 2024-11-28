from api.routes.login import login_route

from flask import request, jsonify

from api.lib.login.login_funcs import login_verification, google_sign_in

@login_route.route('/', methods=["POST"])
def login():
    """
    This function will check if the username and password sent in the JSON is the same as one in the database.
    Returns a True or False, and a JWT token if successful.
    {
        "USERNAME_OR_EMAIL": <username_or_email>,
        "PASSWORD": <password>
    }
    """
    user = request.get_json()

    # Call the verification function to check credentials and generate token
    result = login_verification(user)

    if result['LOGIN']:
        return jsonify(result), 200  # Includes the token
    else:
        return jsonify(result), 401  # Unauthorized status for failed login
    
@login_route.route('/google', methods = ["POST"])
def google():
    """
    This method creates a new user/logs in an existing user with their google credentials.
    {
        "EMAIL": <email>,
        "FIRST_NAME": <first_name>,
        "LAST_NAME": <last_name>
    }
    
    """
    login_data = request.get_json()

    return jsonify(google_sign_in(login_data)), 200