from api import models, db
from flask import current_app
from flask_jwt_extended import create_access_token, jwt_required

from datetime import datetime

from azure.storage.blob import BlobServiceClient



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
        return {"SUCCESS": False}
    
    user = models.LoginInformation(user['EMAIL'], user['USERNAME'], user['PASSWORD'], account_type)

    db.session.add(user)
    db.session.commit()

    return {"SUCCESS": True}

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
        return {"SUCCESS": False}
    
    #Adding Personal Information to the database
    info = models.PersonalInformation(user['FIRST_NAME'], user['LAST_NAME'], user_id)
    db.session.add(info)
    db.session.commit()

    return {"SUCCESS": True}

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
    This function adds subjects to the TutorInformation table (students in the future)
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

    return {"SUCCESS": True}

def add_education_info(ed_info, user_id):
    """
    This function adds education info the the TutorInformation table
    {
        "UNDERGRAD_COLLEGE": STR,
        "UNDERGRAD_MAJOR": STR,
        "GRAD_COLLEGE_1": STR,
        "GRAD_TYPE_1": STR,
        "GRAD_COLLEGE_2": STR,
        "GRAD_TYPE_2": STR,
        "CERTIFICATION": STR
    }
    """

    undergrad_college = ed_info["UNDERGRAD_COLLEGE"]
    undergrad_major = ed_info["UNDERGRAD_MAJOR"]

    grad_college = [ed_info[key] for key in ["GRAD_COLLEGE_1", "GRAD_COLLEGE_2"] if ed_info[key] != ""]
    grad_major = [ed_info[key] for key in ["GRAD_TYPE_1", "GRAD_TYPE_2"] if ed_info[key] != ""]

    teaching_certification = ed_info["CERTIFICATION"]
    tutor = models.TutorInformation.query.filter(models.TutorInformation.user_id == user_id).one_or_none()

    if tutor is None:
        return {"SUCCESS": False}

    tutor.undergrad_college = undergrad_college
    tutor.undergrad_major = undergrad_major
    tutor.graduate_college = grad_college
    tutor.graduate_major = grad_major
    tutor.teaching_certification = teaching_certification

    db.session.commit()

    return {"SUCCESS": True}
            


def add_profile_info(profile_info, user_id):
    """
    This function adds profile information to the TutorInformation table
    {
        "HEADLINE": str,
        "BIO": str
    }
    """
    profile_headline = profile_info["HEADLINE"]
    bio = profile_info["BIO"]

    tutor = models.TutorInformation.query.filter(models.TutorInformation.user_id == user_id).one_or_none()

    if tutor is None:
        return {"SUCCESS": False}    
    
    tutor.profile_headline = profile_headline
    tutor.bio = bio
    db.session.commit()

    return {"SUCCESS": True}

def onboarding_complete(completion_info, user_id):
    """
    This function completes the columns related to profile registration in the LoginInformation table
    {
        "COMPLETE": Boolean,
        "DATE": String
    }
    """
    complete = completion_info["COMPLETE"]
    date = completion_info["DATE"]
    
    tutor = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()

    if complete and tutor is not None:
        tutor.registration_complete = True
        tutor.date_complete = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        db.session.commit()

        return {"SUCCESS": True}
    
    return {"SUCCESS": False}


def upload_files(files, user_id):
    """
    This function uploads files into Azure Blob Storage
    {
        "FILES": [list of files]
    }

    A users files will be saved in a folder with their username
    """
    CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=ntrltrshblob;AccountKey=i3H1VXstjf0GIotcMctbTsiwKnTcgEJBiUYGEakvKAfH1g7GbXYPVaOIHrAthxcHYmErrjrBoFcG+AStWm/5bA==;EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client("user-files")

    user = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()
    username = user.username

    for file in files:
        data = file.read()
        
        container_client.upload_blob(name = f"{username}/{file.filename}", data = data, overwrite=True)

    return {"SUCCESS": True}

