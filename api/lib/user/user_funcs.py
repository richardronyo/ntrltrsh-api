from api import models, db

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
