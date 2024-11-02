from api import models, db
from sqlalchemy.sql import text
from api.lib.Security.AESPython import hash_password_with_salt, split_salt_and_password

def reset_password(password_info, user_id):
    """
    This function will allow a user to reset their password
    {
        "CURRENT_PASSWORD": str,
        "NEW_PASSWORD": str
    }
    """
    current_password = password_info["CURRENT_PASSWORD"]

    if models.LoginInformation.query.filter(models.LoginInformation.password == current_password).one_or_none() is not None:
        user = models.LoginInformation.query.filter(models.LoginInformation.password == current_password).one_or_none()
        new_password = password_info["NEW_PASSWORD"]

        user.password = new_password
        db.session.commit()

        return {"SUCCESS": True}
        

    return {"SUCCESS": False, "msg": "Incorrect value for current password"}

def remove_personal_info(user_id):
    """
    This function will allow a user to remove their personal information to general information to provide privacy
    """
    user_login = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()
    user_personal = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == user_id).one_or_none()

    if user_login is not None and user_personal is not None:
        user_personal.first_name = "General"

        if user_login.account_type == models.AccountType.TUTOR:
            user_personal.last_name = "Student"
        else:
            user_personal.last_name = "Tutor"
        
        db.session.commit()
    
        return {"SUCCESS": True}
    
    return {"SUCCESS": False}

def get_profile_info(profile_info, user_id):
    """
    This function will get a profile from an email address
    {
        "EMAIL": str
    }
    """
    email = profile_info["EMAIL"]
    #When the scheduling is complete, before sending back the information, the server will check if the user they're searching for has a session with them

    user_login = models.LoginInformation.query.filter(models.LoginInformation.email == email).one_or_none()
    other_id = user_login.id

    if user_login is not None:

        username = user_login.username

        if user_login.account_type == models.AccountType.STUDENT:
            account_type = "Student"
        else:
            account_type = "Tutor"
        
        user_personal = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == other_id).one_or_none()
        first_name = user_personal.first_name
        last_name = user_personal.last_name

        full_name = f"{first_name} {last_name}"

        return {"SUCCESS": True, "FULL_NAME": full_name, "USERNAME": username, "ACCOUNT_TYPE": account_type}
    
    
    return {"SUCCESS": False}

def edit_user_info(edit_info, user_id):
    """
    This function will allow a user to edit their own info
    {
        "FIRST_NAME": str,
        "LAST_NAME": str,
        "EMAIL": str,
        "BIO": str
    }
    """
    user_login = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()
    user_personal = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == user_id).one_or_none()
    
    if edit_info["FIRST_NAME"] is not None and edit_info["FIRST_NAME"] != "":
        user_personal.first_name = edit_info["FIRST_NAME"]
    
    if edit_info["LAST_NAME"] is not None and edit_info["LAST_NAME"] != "":
        user_personal.last_name = edit_info["LAST_NAME"]

    if edit_info["EMAIL"] is not None and edit_info["EMAIL"] != "":
        user_login.email = edit_info["EMAIL"]

    if edit_info["BIO"] is not None and edit_info["BIO"] != "":
        if user_login.account_type == models.AccountType.TUTOR:
            user_tutor = models.TutorInformation.query.filter(models.TutorInformation.user_id == user_id).one_or_none()
            user_tutor.bio = edit_info["BIO"]
        else:
            user_student = models.StudentInformation.query.filter(models.StudentInformation.user_id == user_id).one_or_none()
            user_student.bio = edit_info["BIO"]

    db.session.commit()

    return {"SUCCESS": True}

def delete_user(user_id):

    
    db.session.execute(text('SET CONSTRAINTS ALL IMMEDIATE'))

    models.PersonalInformation.query.filter(models.PersonalInformation.user_id == user_id).delete()
    models.StudentInformation.query.filter(models.StudentInformation.user_id == user_id).delete()
    models.TutorInformation.query.filter(models.TutorInformation.user_id == user_id).delete()
    models.Schedule.query.filter(models.Schedule.tutor_id == user_id).delete()
    models.Availability.query.filter(models.Availability.user_id == user_id).delete()
    models.Messaging.query.filter(models.Messaging.sender_id == user_id).delete()
    models.Messaging.query.filter(models.Messaging.receiver_id == user_id).delete()

    models.LoginInformation.query.filter(models.LoginInformation.id == user_id).delete()        
    db.session.commit()

    return {"SUCCESS": True}
