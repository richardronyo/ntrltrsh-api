from api.routes.user import user_route

from flask_jwt_extended import current_user, jwt_required
from flask import request, jsonify

from api.lib.user.user_funcs import reset_password, remove_personal_info, get_profile_info, edit_user_info, delete_user, send_bugreport

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

@user_route.route('/remove_personal', methods=["PUT"])
@jwt_required()
def remove():
    """
    This route will allow a user to set their personal information to general information to provide privacy
    """
    user_id = current_user.id

    return jsonify(remove_personal_info(user_id)) 

@user_route.route('/get_profile', methods=["GET"])
@jwt_required()
def get_profile():
    """
    This route will get a profile for the current user
    """
    user_id = current_user.id
    
    return jsonify(get_profile_info(user_id))

@user_route.route('/edit', methods=["PUT"])
@jwt_required()
def edit():
    """
    This route will allow a user to edit their own info
    {
        "FIRST_NAME": str,
        "LAST_NAME": str,
        "EMAIL": str,
        "BIO": str
    }
    """

    user_id = current_user.id
    edit_info = request.get_json()

    return jsonify(edit_user_info(edit_info, user_id)), 200

@user_route.route('/delete', methods=["DELETE"])
@jwt_required()
def delete():
    """
    This route will delete the current user
    {
        "PASSWORD": str
    }
    """

    user_id = current_user.id

    return jsonify(delete_user(user_id))


@user_route.route('/bugreport', methods=["POST"])
@jwt_required()
def bugreport():
        """
        The route will send a bug report to the admin account
        {
            "REPORTER_ID": str,
            "TITLE": str,
            "DESCRIPTION": str,
        }
        """

        user_id = current_user.id
        bugreport_info = request.get_json()

        return jsonify(send_bugreport(user_id, bugreport_info)), 200