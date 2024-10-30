from api.routes.signup import signup_route

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from api.lib.signup.signup_funcs import add_login_information, add_personal_information, generate_token, add_subjects

from api.lib.Security.AESPython import update_password_field


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
    user = request.get_json() #Convert json to a dictionary
    user = update_password_field(user) #This function hashs the password, and joins the salt and hashed password together
    added_login_info = add_login_information(user)
    added_personal_info = add_personal_information(user)

    if added_login_info and added_personal_info:
        result = generate_token(user)

    if result["SIGNUP"]:
        return jsonify(result), 200
    
    return jsonify(result), 401

@signup_route.route('/subjects', methods=["POST"])
@jwt_required()
def subjects():
    """
    This function adds subjects to the TutorInformation table (students in the future)
    {
        "MATH": [<int>, ..., <int>]
        "SCIENCE": [<int>, ..., <int>]
        "LANGUAGE": [<int>, ..., <int>]
        "ENGLISH": [<int>, ..., <int>]
        "HISTORY": [<int>, ..., <int>]

    }
    """

    user_id = current_user.id
    subjects = request.get_json()

    return jsonify(add_subjects(subjects, user_id))


    


