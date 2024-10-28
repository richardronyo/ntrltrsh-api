from api import models, db

def update_availability(availability_info, user_id):
    availability = models.Availability(user_id, availability_info["MONDAY"], availability_info["TUESDAY"], availability_info["WEDNESDAY"], availability_info["THURSDAY"], availability_info["FRIDAY"], availability_info["SATURDAY"], availability_info["SUNDAY"], availability_info["VACATION"])

    db.session.add(availability)
    db.session.commit()

    return{"SUCCESS": True}