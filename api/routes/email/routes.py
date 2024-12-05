from api.routes.email import email_route

from flask import request, jsonify
from flask_mail import Mail, Message
from api.lib.email.email_funcs import send_email_login_failure, find_email


@email_route.route('/send_email/<email>', methods=['POST'])
def email_login_failure(email):
    """
    The route will send an email to a provided email address
    """
    send_email_login_failure(email)
    return 'Email sent to {}'.format(email)

@email_route.route('/find_email/<email>', methods=['GET'])
def get_user_email(email):
    """
    The route will get the email if it exists,
    Then return the email
    """
    result = find_email(email)
    return result