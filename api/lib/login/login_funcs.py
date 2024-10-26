from api import models, db

import jwt
import datetime
from flask import current_app
from api.lib.Security.AESPython import hash_password_with_salt, split_salt_and_password

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
    password = user["PASSWORD"] #this is the current plaintext password, so we need to hash it so we can compare with the one in the database

    # Check if username/email exists
    user_email = models.LoginInformation.query.filter(models.LoginInformation.email == username_or_email).one_or_none()
    user_username = models.LoginInformation.query.filter(models.LoginInformation.username == username_or_email).one_or_none()

    #To compare passwords, first we will need to get the correct password field from the database
    if(user_email is not None):
        #Get password associated with email in database
        database_password = user_email.password
    elif(user_username is not None):
        #Get password associated with username in database
        database_password = user_username.password
    else:
        return {"LOGIN": False} #Username / Email does not exist in the database

    #Now, lets break the salt and password hash apart
    database_salt, database_password_hash = split_salt_and_password(database_password)
    #Now, hash the the user input password using the database salt
    user_password_hash = hash_password_with_salt(database_salt, password)
    
    #Verify password
    if (user_email is not None and database_password_hash == user_password_hash) or (user_username is not None and database_password_hash == user_password_hash):
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

    return {"LOGIN": False} #Username or email exist, but password doesn't match
