from api.routes.schedule import schedule_route
from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from api.lib.schedule.schedule_funcs import update_availability, matchmaking_algorithm, cancel_session, check_conflict, check_students, get_sessions as gs, get_session_users, book_a_session, add_minutes_to_datetime
from api.lib.email.email_funcs import send_message
from api import models, db, mail

from datetime import datetime
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

@schedule_route.route('/cancel', methods = ["PUT"])
@jwt_required()
def cancel():
    """
    This route will cancel a tutoring session
    {
        "DATE": "YYYY-MM-DD",
    }
    """

    user_id = current_user.id
    cancel_data = request.get_json()
    date_obj = datetime.strptime(cancel_data["DATE"], "%Y-%m-%d")

    #Sending an email that tells the users that their session has been cancelled
    initiator_email = current_user.email
    initiator_account_type = current_user.account_type

    if initiator_account_type == models.AccountType.STUDENT:
        session = models.Schedule.query.filter(models.Schedule.student_id == user_id, models.Schedule.date == date_obj).one_or_none()
        tutor_id = session.tutor_id
        tutor = models.LoginInformation.query.filter(models.LoginInformation.id == tutor_id).one_or_none()
        tutor_email = tutor.email

        msg1 = send_message(tutor_email, f"Cancelled Session", f"Your session on {cancel_data["DATE"]} has been cancelled")
        msg2 = send_message(initiator_email, f"Cancelled Session", f"Your session on {cancel_data["DATE"]} has been cancelled")
    elif initiator_account_type == models.AccountType.TUTOR:
        session = models.Schedule.query.filter(models.Schedule.tutor_id == user_id, models.Schedule.date == date_obj).one_or_none()
        student_id = session.student_id
        student = models.LoginInformation.query.filter(models.LoginInformation.id == student_id).one_or_none()
        student_email = student.email

        msg1 = send_message(student_email, f"Cancelled Session", f"Your session on {cancel_data["DATE"]} has been cancelled")
        msg2 = send_message(initiator_email, f"Cancelled Session", f"Your session on {cancel_data["DATE"]} has been cancelled")

    mail.send(msg1)
    mail.send(msg2)

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

@schedule_route.route('/book', methods = ["POST"])
@jwt_required()
def book():
    """
    This method books a tutoring session manually
    {
        "START_TIME": <str>,
        "DURATION": <str>,
        "SUBJECT": <str>,
        "LOCATION": <str>,
        "DATE": <str>
    }
    """

    session_info = request.get_json()
    user_id = current_user.id

    response, tutor_id = book_a_session(user_id, session_info)

    if tutor_id != "No tutor ID":
        tutor = models.LoginInformation.query.filter(models.LoginInformation.id == tutor_id).one_or_none()
        tutor_email = tutor.email
        student_email = current_user.email

        msg1 = send_message(tutor_email, f"New Session", f"You have a new session on {session_info["DATE"]} from {session_info["START_TIME"]} - {add_minutes_to_datetime(session_info["START_TIME"], float(session_info["DURATION"]))}")
        msg2 = send_message(student_email, f"New Session", f"You have a new session on {session_info["DATE"]} from {session_info["START_TIME"]} - {add_minutes_to_datetime(session_info["START_TIME"], float(session_info["DURATION"]))}")
        mail.send(msg1)
        mail.send(msg2)
    
    return jsonify(response), 200