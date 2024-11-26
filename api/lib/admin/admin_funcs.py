from api import models, db
from sqlalchemy.sql import text


def retrieve_all_users():
    users = db.session.query(models.LoginInformation).all()
    user_list = []

    for user in users:
        user_list.append(user.to_dict())

    return user_list

def clear_database():
    db.session.execute(text('SET CONSTRAINTS ALL IMMEDIATE'))

    #Clearing all the users in the database
    personal_info = db.session.query(models.PersonalInformation).delete()
    schedules = db.session.query(models.Availability).delete()
    students = db.session.query(models.StudentInformation).delete()
    tutors = db.session.query(models.TutorInformation).delete()
    messages = db.session.query(models.Messaging).delete()
    bugs = db.session.query(models.Bugs).delete()
    users = db.session.query(models.LoginInformation).delete()



        
    db.session.commit()

    return True

def delete_user(user_id):
    login = db.session.query.filter(models.LoginInformation.id == user_id).one_or_none()
    personal = db.session.query.filter(models.PersonalInformation.user_id == user_id).one_or_none()

    if login.account_type == models.AccountType.STUDENT:
        specific_account = db.session.query.filter(models.StudentInformation.user_id == user_id).one_or_none()
    elif login.account_type == models.AccountType.TUTOR:
        specific_account = db.session.query.filter(models.TutorInformation.user_id == user_id).one_or_none()

    availability = db.session.query.filter(models.Availability.user_id == user_id).one_or_none()

    db.session.execute(text('SET CONSTRAINTS ALL IMMEDIATE'))

    db.session.delete(availability)
    db.session.delete(specific_account)
    db.session.delete(personal)
    db.session.delete(login)

def change_account_type(user_id):
    account = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()

    account.account_type = models.AccountType.ADMIN
    db.session.commit()
    return {"SUCCESS": True}
