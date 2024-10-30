from api import models, db
from flask import current_app
from flask_jwt_extended import create_access_token, jwt_required

def add_login_information(user):
    """
    This function adds a row to the LoginInformation table. Called by accessing /api/signup/logininformation
    {
        "ACCOUNT_TYPE": <account_type>,
        "USERNAME": <username>,
        "EMAIL": <email>,
        "PASSWORD": <password>,
        "FIRST_NAME": <first_name>,
        "LAST_NAME": <last_name>
    }
    """
    account_type = models.AccountType(user['ACCOUNT_TYPE'])

    #If there is a user with the same username or email, return False
    if len(models.LoginInformation.query.filter(models.LoginInformation.username == user["USERNAME"]).all()) == 1 or len(models.LoginInformation.query.filter(models.LoginInformation.email == user["EMAIL"]).all()) == 1:
        return False
    
    user = models.LoginInformation(user['EMAIL'], user['USERNAME'], user['PASSWORD'], account_type)

    db.session.add(user)
    db.session.commit()

    return True

def add_personal_information(user):
    """
    This function adds a row to the PersonalInformation table.
        {
        "ACCOUNT_TYPE": <account_type>,
        "USERNAME": <username>,
        "EMAIL": <email>,
        "PASSWORD": <password>,
        "FIRST_NAME": <first_name>,
        "LAST_NAME": <last_name>
    }
    """
    #Getting the user ID from the database
    user_id = models.LoginInformation.query.filter(models.LoginInformation.username == user['USERNAME']).one_or_none().id
    if user_id is None:
        return False
    
    #Adding Personal Information to the database
    info = models.PersonalInformation(user['FIRST_NAME'], user['LAST_NAME'], user_id)
    db.session.add(info)
    db.session.commit()

    return True

def generate_token(user):
    """
    This function generates 
    {
        "ACCOUNT_TYPE": <account_type>,
        "USERNAME": <username>,
        "EMAIL": <email>,
        "PASSWORD": <password>,
        "FIRST_NAME": <first_name>,
        "LAST_NAME": <last_name>
    }
    """

    user_id = models.LoginInformation.query.filter(models.LoginInformation.username == user['USERNAME']).one_or_none().id

    if user_id is None:
        return {"SIGNUP": False}
    
    token = create_access_token(identity = user_id)
    
    return {
        "SIGNUP": True,
        "token": token
    }

def add_subjects(subjects, user_id):
    """
    This function adds subjects to the tables of tutors (students in the future)
    {
        "MATH": [<int>, ..., <int>]
        "SCIENCE": [<int>, ..., <int>]
        "LANGUAGE": [<int>, ..., <int>]
        "ENGLISH": [<int>, ..., <int>]
        "HISTORY": [<int>, ..., <int>]

    }
    """

    math = [models.Math(value) for value in subjects['MATH']]
    science = [models.Science(value) for value in subjects['SCIENCE']]
    language = [models.Language(value) for value in subjects['LANGUAGE']]
    english = [models.English(value) for value in subjects['ENGLISH']]
    history = [models.History(value) for value in subjects['HISTORY']]

    tutor = models.TutorInformation(user_id, math=math, science=science, language=language, english=english, history=history)

    db.session.add(tutor)
    db.session.commit()

    return True
            






