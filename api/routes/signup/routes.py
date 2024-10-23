from api.routes.signup import signup_route

from flask import request, jsonify

from api.lib.signup.signup_funcs import add_login_information, add_personal_information, generate_token


@signup_route.route('/page1', methods=["POST"])
def new_user():
    """
    This route adds a row to the LoginInformation table.
    {
        "ACCOUNT_TYPE": <account_type>,
        "USERNAME": <username>,
        "EMAIL": <email>,
        "PASSWORD": <password>,
        "FIRST_NAME": <first_name>,
        "LAST_NAME": <last_name>
    }
    """
    user = request.get_json()

    added_login_info = add_login_information(user)
    added_personal_info = add_personal_information(user)

    result = generate_token(user)

    if result["SIGNUP"]:
        return jsonify(result), 200
    
    return jsonify(result), 401
    


