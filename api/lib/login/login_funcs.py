from api import models, db

import jwt
import datetime
from flask import current_app

def login_verification(user):
    """
    Verifies the username and password and returns a JWT token if login is successful.
    {
        "USERNAME_OR_EMAIL": <username or email>,
        "PASSWORD": <password>
    }

    Returns:
    {
        "LOGIN": True or False,
        "token": <jwt_token> (only if login is successful)
    }
    """
    username_or_email = user["USERNAME_OR_EMAIL"]
    password = user["PASSWORD"]

    # Check if username/email exists and verify password
    user_email = models.LoginInformation.query.filter(models.LoginInformation.email == username_or_email).one_or_none()
    user_username = models.LoginInformation.query.filter(models.LoginInformation.username == username_or_email).one_or_none()

    if (user_email is not None and user_email.password == password) or (user_username is not None and user_username.password == password):
        # User authenticated successfully, generate JWT token
        payload = {
            "user_id": user_email.id if user_email else user_username.id  # Include user_id or any user info you need
        }
        secret_key = current_app.config['SECRET_KEY']  # Use the Flask app's secret key
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return {
            "LOGIN": True,
            "token": token
        }

    return {"LOGIN": False}
