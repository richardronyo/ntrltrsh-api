from api import models, db
from datetime import datetime, timedelta
import random

def update_availability(availability_info, user_id, account_type):
    availability = models.Availability(user_id, account_type, availability_info["MONDAY"], availability_info["TUESDAY"], availability_info["WEDNESDAY"], availability_info["THURSDAY"], availability_info["FRIDAY"], availability_info["SATURDAY"], availability_info["SUNDAY"], availability_info["VACATION"])

    db.session.add(availability)
    db.session.commit()

    return{"SUCCESS": True}


# Function to get a random 2-hour time slot
def get_random_time_slot(window_start_str, window_end_str):
    # Convert the window start and end time strings to datetime objects
    window_start = datetime.strptime(window_start_str, "%H:%M")
    window_end = datetime.strptime(window_end_str, "%H:%M")
    
    # Calculate the latest possible start time for a 2-hour window
    latest_start = window_end - timedelta(hours=2)
    
    # Generate possible start times on the hour or half hour within the valid range
    valid_start_times = []
    current_time = window_start
    
    # Add valid times on the hour or half hour to the list
    while current_time <= latest_start:
        valid_start_times.append(current_time)
        current_time += timedelta(minutes=30)  # Increment by 30 minutes (half hour)
    
    # Randomly choose a start time from the valid start times
    random_start_time = random.choice(valid_start_times)
    
    # Calculate the end time (2 hours after the random start time)
    random_end_time = random_start_time + timedelta(hours=2)
    
    # Return the random start and end times as strings
    return random_start_time.strftime("%H:%M"), random_end_time.strftime("%H:%M")

def matchmaking_algorithm():
    #Getting all the tutor availabilities and subjects
    availability_info = models.Availability.query.all()
    tutor_info = [models.TutorInformation.query.filter(models.TutorInformation.user_id == availability.user_id).one() for availability in availability_info]
    
    #Getting all the student information for the students who have completed registration
    student_info = [models.StudentInformation.query.filter(models.StudentInformation.user_id == completed_student.id).one() for completed_student in models.LoginInformation.query.all() if completed_student.account_type == models.AccountType.STUDENT and completed_student.registration_complete == True]

    #Converting tutor_info and student_info into a single list of subjects for each tutor/client respectively
    tutor_subjects = [tutor.math + tutor.science + tutor.history + tutor.language + tutor.english for tutor in tutor_info]
    student_subjects = [(student.user_id, student.math + student.science + student.history + student.language + student.english) for student in student_info]

    #Determining the scheduling period based off of the current date
    #This algorithm will only run on the last sunday of a two week period
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7
    next_monday = today + timedelta(days = days_until_monday)
    
    next_14_days = [next_monday + timedelta(days = i) for i in range(14)]
    first_week = [date.strftime('%A, %Y-%m-%d') for date in next_14_days[:7]]  # First week
    second_week = [date.strftime('%A, %Y-%m-%d') for date in next_14_days[7:]]  # Second week
    scheduling_period = [first_week, second_week]

    #Converting Availability into a list of tuples (DAY_OF_WEEK, START_TIME, END_TIME) and getting the vacation dates
    vacations = [availability.vacation_days for availability in availability_info] #[[date1, date2, ...], [], ..., []]
    availabilities = []

    for availability in availability_info:
        availability_list = [("MONDAY", availability.mon_avail), ("TUESDAY", availability.tue_avail), ("WEDNESDAY", availability.wed_avail), ("THURSDAY", availability.thurs_avail), ("FRIDAY", availability.fri_avail), ("SATURDAY", availability.sat_avail), ("SUNDAY", availability.sun_avail)]
        availabilities.append(availability_list)

    for i in range(len(tutor_info)):
        #Getting the TutorInformation, availability, subjects they can help with, and vacation date for the current tutor
        tutor = tutor_info[i]
        availability = availabilities[i]
        subjects = tutor_subjects[i]
        vacation = vacations[i]

        #Picking a random day they are available to schedule them
        day_of_session_1, times_1 = random.choice(availability)  # First week
        while times_1 == []:
            day_of_session_1, times_1 = random.choice(availability)

        day_of_session_2, times_2 = random.choice(availability)  # Second week
        while times_2 == []:
            day_of_session_2, times_2 = random.choice(availability)

        #Picking a random choice of subject to find a student to match with
        subject_1 = random.choice(subjects)
        subject_2 = random.choice(subjects)

        appropriate_students_1 = [student for student in student_subjects if subject_1 in student[1]]
        appropriate_students_2 = [student for student in student_subjects if subject_2 in student[1]]
        
        #If there are no students and they can only help with one subject, we are going to continue to the next tutor
        if appropriate_students_1 == [] and len(subjects) == 1:
            continue

        if appropriate_students_2 == [] and len(subjects) == 1:
            continue

        
        #If there are no students, picking another subjects.  Repeating this process 3 times
        if appropriate_students_1 == []:
            new_subject = random.choice(subjects)
            for i in range(3):
                while new_subject == subject:
                    new_subject = random.choice(subjects)
                appropriate_students_1 = [student for student in student_subjects if new_subject in student[1]]

                if appropriate_students_1 != [] and i <= 2:
                    subject = new_subject
                    break
            continue

        if appropriate_students_2 == []:
            new_subject = random.choice(subjects)
            for i in range(3):
                while new_subject == subject:
                    new_subject = random.choice(subjects)
                appropriate_students_2 = [student for student in student_subjects if new_subject in student[1]]

                if appropriate_students_2 != [] and i <= 2:
                    subject = new_subject
                    break
            continue

        # Choosing the first student for the first week
        student_1 = random.choice(appropriate_students_1)
        student_id_1 = student_1[0]
        window_start_1 = times_1[0]
        window_end_1 = times_1[1]

        start_time_1, end_time_1 = get_random_time_slot(window_start_1, window_end_1)

        # Selecting the second student for the second week
        student_2 = random.choice(appropriate_students_2)
        student_id_2 = student_2[0]
        window_start_2 = times_2[0]
        window_end_2 = times_2[1]

        start_time_2, end_time_2 = get_random_time_slot(window_start_2, window_end_2)

        schedule_info = models.Schedule.query.all()
        existing_sessions = [(session.day, session.date, session.start_time, session.end_time) for session in schedule_info]

        possible_dates_1 = [day for day in scheduling_period[0] if day.split(", ")[0].upper() == day_of_session_1 and (day.split(", ")[1] not in vacation or day.split(", ")[1] not in existing_sessions)]
        possible_dates_2 = [day for day in scheduling_period[1] if day.split(", ")[0].upper() == day_of_session_2 and (day.split(", ")[1] not in vacation or day.split(", ")[1] not in existing_sessions)]

        print(possible_dates_1)
        print(possible_dates_2)

        session_date_1 = random.choice(possible_dates_1)
        session_date_2 = random.choice(possible_dates_2)

        day_1 = session_date_1.split(", ")[0]
        date_1 = session_date_1.split(", ")[1]
        
        day_2 = session_date_2.split(", ")[0]
        date_2 = session_date_2.split(", ")[1]


        tutoring_session_1 = models.Schedule(student_id_1, tutor.user_id, datetime.strptime(date_1, "%Y-%m-%d"), start_time_1, end_time_1)
        tutoring_session_2 = models.Schedule(student_id_2, tutor.user_id, datetime.strptime(date_2, "%Y-%m-%d"), start_time_2, end_time_2)

        shifts = models.Shifts(tutor.user_id, scheduling_period[0][0].split(", ")[1], scheduling_period[1][-1].split(", ")[1])
        shifts.add_shift()

        print(tutoring_session_1.to_dict())
        db.session.add(tutoring_session_1)
        db.session.add(tutoring_session_2)
        db.session.add(shifts)
        db.session.commit()

    return {"SUCCESS": True}

def cancel_session(user_id, cancel_data):
    """
    This helper function will cancel a tutoring session
    {
        "DATE": "YYYY-MM-DD",
        "EMAIL": str 
    }
    """

    date = datetime.strptime(cancel_data["DATE"], "%Y-%m-%d")
    email = cancel_data["EMAIL"]

    login = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()

    account_type = login.account_type

    if account_type == models.AccountType.STUDENT: #This means a student is cancelling. We must find the tutor_id to get the correct session
        tutor_account = models.LoginInformation.query.filter(models.LoginInformation.email == email).one_or_none()
        tutor_id = tutor_account.id
        
        tutor_session = models.Schedule.query.filter(models.Schedule.tutor_id == tutor_id, models.Schedule.student_id == user_id, models.Schedule.date == date).one_or_none()

        shifts = models.Shifts.query.filter(models.Shifts.tutor_id == tutor_id).all()
        for shift_period in shifts:
            start_day = datetime.strptime(shift_period.start_day, "%Y-%m-%d")
            end_day = datetime.strptime(shift_period.end_day, "%Y-%m-%d")

            if start_day <= date and end_day >= date:
                shift = shift_period
                break

    else:
        student_account = models.LoginInformation.query.filter(models.LoginInformation.email == email).one_or_none()
        student_id = student_account.id

        tutor_session = models.Schedule.query.filter(models.Schedule.tutor_id == user_id, models.Schedule.student_id == student_id, models.Schedule.date == date).one_or_none()
        shifts = models.Shifts.query.filter(models.Shifts.tutor_id == user_id).all()
        for shift_period in shifts:
            start_day = datetime.strptime(shift_period.start_day, "%Y-%m-%d")
            end_day = datetime.strptime(shift_period.end_day, "%Y-%m-%d")

            if start_day <= date and end_day >= date:
                shift = shift_period
                break
    shift.num_of_shifts -= 1
    db.session.delete(tutor_session)
    db.session.commit()

    return {"SUCCESS": True}







