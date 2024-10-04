from api import models, db

def add_login_information(user):
    """
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

    user = models.LoginInformation(user['EMAIL'], user['USERNAME'], user['PASSWORD'], account_type)

    db.session.add(user)
    db.session.commit()

    return True
