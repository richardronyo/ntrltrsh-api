from api.routes.signup import signup_route

from flask import request, jsonify

from api.lib.signup.signup_funcs import add_login_information


@signup_route.route('/logininformation', methods=["POST"])
def new_user():
    """
    This route adds a row to the LoginInformation table.
    {
        "ACCOUNT_TYPE": <account_type>,
        "USERNAME": <username>,
        "EMAIL": <email>,
        "PASSWORD": <password>
    }
    """
    user = request.get_json()
    return jsonify(add_login_information(user)), 200

