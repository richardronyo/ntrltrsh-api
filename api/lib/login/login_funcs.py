from api import models, db

def login_verification(user):
    """
    This function will check if the username and password sent in the JSON is the same as one in the database. Called by accessing the api/login/ route
    {
        "USERNAME_OR_EMAIL": <username or email>,
        "PASSWORD": <password>
    }

    Will return a JSON with the following format:
    {
        "LOGIN": True or False
    }
    """
    username_or_email = user["USERNAME_OR_EMAIL"]
    password = user["PASSWORD"]

    #These lines will return the row that the username or email provided by the user is found. They will return None if otherwise
    user_email = models.LoginInformation.query.filter(models.LoginInformation.email == username_or_email).one_or_none()
    user_username = models.LoginInformation.query.filter(models.LoginInformation.username == username_or_email).one_or_none()

    #If the username/email is correct, and it matches the stored password, the user can successfully login
    if ((user_email is not None and user_email.password == password) or (user_username is not None and user_username.password == password)):
        return {"LOGIN": True}
    
    return {"LOGIN": False}    
