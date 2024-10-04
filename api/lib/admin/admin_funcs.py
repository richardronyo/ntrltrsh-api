from api import models, db

def retrieve_all_users():
    users = db.session.query(models.LoginInformation).all()
    user_list = []

    for user in users:
        user_list.append(user.to_dict())

    return user_list

def clear_users():
    users = db.session.query(models.LoginInformation).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

    return True