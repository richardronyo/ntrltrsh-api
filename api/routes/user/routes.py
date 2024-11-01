from api.routes.user import user_route

from flask_jwt_extended import current_user, jwt_required
from flask import request, jsonify

from api.lib.user.user_funcs import reset_password, remove_personal_info, get_profile_info

@user_route.route('/reset_password', methods=["PUT"])
@jwt_required()
def reset():
    """
    This route will allow a user to reset their password
    {
        "CURRENT_PASSWORD": str,
        "NEW_PASSWORD": str
    }
    """
    user_id = current_user.id
    password_info = request.get_json()

    return jsonify(reset_password(password_info, user_id)), 200

@user_route.route('remove_personal', methods=["PUT"])
@jwt_required()
def remove():
    """
    This route will allow a user to set their personal information to general information to provide privacy
    """
    user_id = current_user.id

    return jsonify(remove_personal_info(user_id)) 

@user_route.route('get_profile', methods=["GET"])
@jwt_required()
def get_profile():
    """
    This route will get a profile from an email address
    {
        "EMAIL": str
    }
    """
    user_id = current_user.id
    profile_info = request.get_json()
    
    return jsonify(get_profile_info(profile_info, user_id))