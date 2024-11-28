from api import models, db

import jwt
import datetime
from flask import current_app
from flask_jwt_extended import create_access_token, jwt_required
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
        registration = user_email.registration_complete
    elif(user_username is not None):
        #Get password associated with username in database
        database_password = user_username.password
        registration = user_username.registration_complete
    else:
        return {"LOGIN": False} #Username / Email does not exist in the database

    #Now, lets break the salt and password hash apart
    database_salt, database_password_hash = split_salt_and_password(database_password)
    #Now, hash the the user input password using the database salt
    user_password_hash = hash_password_with_salt(database_salt, password)
    

    #Verify password
    if (user_email is not None and database_password_hash == user_password_hash) or (user_username is not None and database_password_hash == user_password_hash):
        # User authenticated successfully, generate JWT token
        if user_email is not None:
            token = create_access_token(identity=user_email.id)
        else:
            token = create_access_token(identity=user_username.id)

        return {
            "LOGIN": True,
            "token": token,
            "REGISTRATION_COMPLETE": registration
        }

    return {"LOGIN": False} #Username or email exist, but password doesn't match

def google_sign_in(login_data):
    """
    This method creates a new user/logs in an existing user with their google credentials. It will return a login token and if the registration is complete.

    If the user's information isn't already in the database, it will add the user to the database.
    {
        "EMAIL": <email>,
        "FIRST_NAME": <first_name>,
        "LAST_NAME": <last_name>
    }
    
    """

    email = login_data['EMAIL']
    first_name = login_data["FIRST_NAME"]
    last_name = login_data["LAST_NAME"]

    if models.LoginInformation.query.filter(models.LoginInformation.email == email).one_or_none() is None:
        #Create the student user:
        username = email.split("@")[0]
        user = models.LoginInformation(email, username, None, models.AccountType.STUDENT)
        db.session.add(user)
        db.session.commit()

        #Getting the user_id from the LoginInformation table to add personal information
        current_user = models.LoginInformation.query.filter(models.LoginInformation.email == email).one_or_none()
        current_user_personal = models.PersonalInformation(first_name, last_name, current_user.id)
        db.session.add(current_user_personal)
        db.session.commit()

    
    user = models.LoginInformation.query.filter(models.LoginInformation.email == email).one_or_none()
    registration = user.registration_complete
    token = create_access_token(identity=email)

    return{
        "LOGIN": True,
        "REGISTRATION_COMPLETE": registration,
        "token": token
    }