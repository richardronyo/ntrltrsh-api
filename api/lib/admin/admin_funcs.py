from api import models, db
from sqlalchemy.sql import text

from api.lib.Security.AESPython import update_password_field



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
    db.session.query(models.Schedule).delete()
    db.session.query(models.Shifts).delete()

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
    schedule = db.session.query.filter(models.Schedule.user_id == user_id).all()
    bug = db.session.query.filter(models.Bugs.reporter_id == user_id).one_or_none()
    shifts = db.session.query.filter(models.Shifts.tutor_id == user_id).one_or_none()
    messages = db.session.query.filter(models.Messaging.sender_id == user_id or models.Messaging.receiver_id == user_id).all()

    db.session.execute(text('SET CONSTRAINTS ALL IMMEDIATE'))

    db.session.delete(availability)
    db.session.delete(schedule)
    db.session.delete(bug)
    db.session.delete(shifts)
    db.session.delete(messages)
    db.session.delete(specific_account)
    db.session.delete(personal)

    db.session.delete(login)
\
def change_account_type(user_id):
    account = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()

    account.account_type = models.AccountType.ADMIN
    account.registration_complete = True
    db.session.commit()
    return {"SUCCESS": True}

def create_admin():
    password = {"PASSWORD": "admin"}
    password = update_password_field(password)
    password = password["PASSWORD"]

    admin = models.LoginInformation(email="admin@studycycle.com", username="admin", password = password, account_type= models.AccountType.ADMIN)
    db.session.add(admin)
    db.session.commit()
    return {"SUCCESS": True}

def clear_schedule_and_shifts():
    db.session.query(models.Schedule).delete()
    db.session.query(models.Shifts).delete()

    db.session.commit()

    return {"SUCCESS": True}

def retrieve_all_bugreports():
    bugreports = db.session.query(models.Bugs).all()
    bugreport_list = []

    for bugreport in bugreports:
        bugreport_list.append(bugreport.to_dict())

    return bugreport_list

def get_all_students():
    all_students = models.LoginInformation.query.filter(models.LoginInformation.account_type == models.AccountType.STUDENT).all()

    student_info = []
    for student in all_students:
        student_personal = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == student.id).one_or_none()

        if student_personal:
            student_info.append(
                {
                    "EMAIL": student.email,
                    "USERNAME": student.username,
                    "FIRST_NAME": student_personal.first_name,
                    "LAST_NAME": student_personal.last_name
                }
            )

    return {
        "SUCCESS": True,
        "STUDENTS": student_info
    }

def get_all_tutors():
    all_tutors = models.LoginInformation.query.filter(models.LoginInformation.account_type == models.AccountType.TUTOR).all()

    tutor_info = []
    for tutor in all_tutors:
        tutor_personal = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == tutor.id).one_or_none()

        if tutor_personal:
            tutor_info.append(
                {
                    "EMAIL": tutor.email,
                    "USERNAME": tutor.username,
                    "FIRST_NAME": tutor_personal.first_name,
                    "LAST_NAME": tutor_personal.last_name
                }
            )
    
    return {
        "SUCCESS": True,
        "TUTORS": tutor_info
    }