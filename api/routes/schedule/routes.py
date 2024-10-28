from api.routes.schedule import schedule_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from api.lib.schedule.schedule_funcs import update_availability

@schedule_route.route('/update', methods=["POST"])
@jwt_required()
def update():
    """
    This route updates a Tutor's availability. The user must send a valid JWT token, 
    which contains the user_id. The user also posts a JSON to the server with this format:
    {
        "MONDAY": [<start_time>, <end_time>],
        "TUESDAY": [<start_time>, <end_time>],
        "WEDNESDAY": [<start_time>, <end_time>],
        "THURSDAY": [<start_time>, <end_time>],
        "FRIDAY": [<start_time>, <end_time>],
        "SATURDAY": [<start_time>, <end_time>],
        "SUNDAY": [<start_time>, <end_time>],
        "VACATION": [<day1>, <day2>, ..., <dayk>]
    }
    """

    # Access `current_user` directly to get the user ID
    user_id = current_user.id
    account_type = current_user.account_type

    # Get the JSON payload with availability information
    availability_info = request.get_json()

    # Call the update function with availability info and user_id
    return jsonify(update_availability(availability_info, user_id, account_type)), 200


