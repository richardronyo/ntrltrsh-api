from api import models, db

def add_login_information(user):
    """
    This function adds a row to the LoginInformation table. Called by accessing /api/signup/logininformation
    {
        "ACCOUNT_TYPE": <account_type>,
        "USERNAME": <username>,
        "EMAIL": <email>,
        "PASSWORD": <password>
    }
    """
    if user['ACCOUNT_TYPE'] == 1:
        account_type = models.AccountType.TUTOR
    elif user['ACCOUNT_TYPE'] == 2:
        account_type = models.AccountType.STUDENT

    #If there is a user with the same username or email, return False
    if len(models.LoginInformation.query.filter(models.LoginInformation.username == user["USERNAME"]).all()) == 1 or len(models.LoginInformation.query.filter(models.LoginInformation.email == user["EMAIL"]).all()) == 1:
        return False
    
    user = models.LoginInformation(user['EMAIL'], user['USERNAME'], user['PASSWORD'], account_type)

    db.session.add(user)
    db.session.commit()

    return True


