from api.routes.schedule import schedule_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from api.lib.schedule.schedule_funcs import update_availability, matchmaking_algorithm, cancel_session, check_conflict, check_students, get_sessions as gs, get_session_users

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

@schedule_route.route('/match', methods = ["PUT"])
def match():
    """
    This route will run the matchmaking algorithm
    """
    matchmaking_algorithm()
    check_conflict()
    
    return jsonify(check_students()), 200

@schedule_route.route('/cancel', methods = ["DELETE"])
@jwt_required()
def cancel():
    """
    This route will cancel a tutoring session
    {
        "DATE": "YYYY-MM-DD",
        "EMAIL": str 
    }
    """

    user_id = current_user.id
    cancel_data = request.get_json()

    return jsonify(cancel_session(user_id, cancel_data)), 200


@schedule_route.route('/get', methods = ["GET"])
@jwt_required()
def get_sessions():
    """
    This route gets all the sessions for a user that are on or after the current day
    """

    user_id = current_user.id
    return jsonify(gs(user_id)), 200

@schedule_route.route('/get_match_names', methods = ["GET"])
@jwt_required()
def get_session_matches():
    """
    This route gets all names and usernames of users you're matched with on or after the current day
    """

    user_id = current_user.id
    return jsonify(get_session_users(user_id)), 200