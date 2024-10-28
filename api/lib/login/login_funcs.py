from api import models, db

import jwt
import datetime
from flask import current_app
from flask_jwt_extended import create_access_token, jwt_required

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
        if user_email is not None:
            token = create_access_token(identity=user_email.id)
        else:
            token = create_access_token(identity=user_username.id)

        return {
            "LOGIN": True,
            "token": token
        }

    return {"LOGIN": False}
