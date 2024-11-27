from api.routes.messaging import messaging_route

from flask import request, jsonify
from flask_jwt_extended import current_user, jwt_required
from api.lib.messaging.messaging_funcs import send_message, get_all_messages

@messaging_route.route('/send', methods = ["POST"])
@jwt_required()
def send():
    """
    This route will send a message to the specified username
    {
        "USERNAME": str,
        "MESSAGE": str
    }
    """

    user_id = current_user.id
    message_info = request.get_json()

    return jsonify(send_message(user_id, message_info))

@messaging_route.route('/inbox', methods=["GET"])
@jwt_required()
def inbox():
    """
    This route will get the inbox of the current user
    """

    user_id = current_user.id
    return jsonify(get_all_messages(user_id)), 200

    