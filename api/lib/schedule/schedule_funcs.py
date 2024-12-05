from api import models, db
from datetime import datetime, timedelta
import random
import calendar

def update_availability(availability_info, user_id, account_type):
    availability = models.Availability(user_id, account_type, availability_info["MONDAY"], availability_info["TUESDAY"], availability_info["WEDNESDAY"], availability_info["THURSDAY"], availability_info["FRIDAY"], availability_info["SATURDAY"], availability_info["SUNDAY"], availability_info["VACATION"])

    db.session.add(availability)
    db.session.commit()

    return{"SUCCESS": True}

def map_subject_to_string(subject):
    if subject == models.Math.ALGEBRA:
        string_subject = "Algebra"
    elif subject == models.Math.CALCULUS:
        string_subject = "Calculus"
    elif subject == models.Math.GEOMETRY:
        string_subject = "Geometry"
    elif subject == models.Math.TRIGONOMETRY:
        string_subject = "Trigonometry"
    elif subject == models.Math.STATISTICS:
        string_subject = "Statistics"
    elif subject == models.Math.PROBABILITY:
        string_subject = "Probability"
    elif subject == models.Math.DIFFERENTIAL_EQUATIONS:
        string_subject = "Differential Equations"
    elif subject == models.Math.LINEAR_ALGEBRA:
        string_subject = "Linear Algebra"
    elif subject == models.Math.GENERAL_MATH:
        string_subject = "General Math"
        
    elif subject == models.Science.PHYSICS:
        string_subject = "Physics"
    elif subject == models.Science.CHEMISTRY:
        string_subject = "Chemistry"
    elif subject == models.Science.BIOLOGY:
        string_subject = "Biology"
    elif subject == models.Science.EARTH_SCIENCE:
        string_subject = "Earth Science"
    elif subject == models.Science.ASTRONOMY:
        string_subject = "Astronomy"
    elif subject == models.Science.ENVIRONMENTAL_SCIENCE:
        string_subject = "Environmental Science"
    elif subject == models.Science.BOTANY:
        string_subject = "Botany"
    elif subject == models.Science.ZOOLOGY:
        string_subject = "Zoology"
    elif subject == models.Science.GENERAL_SCIENCE:
        string_subject = "General Science"

    elif subject == models.Language.FRENCH:
        string_subject = "French"
    elif subject == models.Language.SPANISH:
        string_subject = "Spanish"
    elif subject == models.Language.GERMAN:
        string_subject = "German"
    elif subject == models.Language.CHINESE:
        string_subject = "Chinese"
    elif subject == models.Language.JAPANESE:
        string_subject = "Japanese"
    elif subject == models.Language.RUSSIAN:
        string_subject = "Russian"
    elif subject == models.Language.ITALIAN:
        string_subject = "Italian"
    elif subject == models.Language.ARABIC:
        string_subject = "Arabic"
    
    elif subject == models.English.LITERATURE:
        string_subject = "Literature"
    elif subject == models.English.GRAMMAR:
        string_subject = "Grammar"
    elif subject == models.English.WRITING:
        string_subject = "Writing"
    elif subject == models.English.POETRY:
        string_subject = "Poetry"
    elif subject == models.English.DRAMA:
        string_subject = "Drama"
    elif subject == models.English.ESSAY_WRITING:
        string_subject = "Essay Writing"
    elif subject == models.English.CRITICAL_ANALYSIS:
        string_subject = "Critical Analysis"
    elif subject == models.English.CREATIVE_WRITING:
        string_subject = "Creative Writing"
    elif subject == models.English.GENERAL_ENGLISH:
        string_subject = "General English"
        
    elif subject == models.History.ANCIENT:
        string_subject = "Ancient History"
    elif subject == models.History.MEDIEVAL:
        string_subject = "Medieval History"
    elif subject == models.History.MODERN:
        string_subject = "Modern History"
    elif subject == models.History.WORLD_WAR_I:
        string_subject = "World War I"
    elif subject == models.History.WORLD_WAR_II:
        string_subject = "World War II"
    elif subject == models.History.AMERICAN_REVOLUTION:
        string_subject = "American Revolution"
    elif subject == models.History.INDUSTRIAL_REVOLUTION:
        string_subject = "Industrial Revolution"
    elif subject == models.History.COLD_WAR:
        string_subject = "Cold War"
    elif subject == models.History.SOCIAL_STUDIES:
        string_subject = "Social Studies"
    
    return string_subject


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

        print("Existing Sessions: ", existing_sessions)
        print("Possible Days 1: ", possible_dates_1)
        print("Possible Days 2: ", possible_dates_2)

        session_date_1 = random.choice(possible_dates_1)
        session_date_2 = random.choice(possible_dates_2)

        day_1 = session_date_1.split(", ")[0]
        date_1 = session_date_1.split(", ")[1]
        
        day_2 = session_date_2.split(", ")[0]
        date_2 = session_date_2.split(", ")[1]

        tutoring_session_1 = models.Schedule(student_id_1, tutor.user_id, datetime.strptime(date_1, "%Y-%m-%d"), start_time_1, end_time_1, map_subject_to_string(subject_1))
        tutoring_session_2 = models.Schedule(student_id_2, tutor.user_id, datetime.strptime(date_2, "%Y-%m-%d"), start_time_2, end_time_2, map_subject_to_string(subject_2))

        shifts = models.Shifts(tutor.user_id, scheduling_period[0][0].split(", ")[1], scheduling_period[1][-1].split(", ")[1])
        shifts.add_shift()

        print(tutoring_session_1.to_dict())
        db.session.add(tutoring_session_1)
        db.session.add(tutoring_session_2)
        db.session.add(shifts)
        db.session.commit()

    return {"SUCCESS": True}

# Helper function to check if two time periods overlap
def time_conflict(start_time_1, end_time_1, start_time_2, end_time_2):
    """Check if two time periods [start_time_1, end_time_1] and [start_time_2, end_time_2] overlap."""
    return not (end_time_1 <= start_time_2 or end_time_2 <= start_time_1)

# Function to find an available time slot for rescheduling
def find_available_slot_for_reschedule(tutor_id, date, start_time, end_time):
    """Find a suitable available time slot in the tutor's schedule."""
    tutor_availability = models.Availability.query.filter_by(user_id=tutor_id).first()
    day_of_week = date.strftime('%A').upper()

    # Retrieve availability based on the day of the week
    if day_of_week == "MONDAY":
        available_slots = tutor_availability.mon_avail
    elif day_of_week == "TUESDAY":
        available_slots = tutor_availability.tue_avail
    elif day_of_week == "WEDNESDAY":
        available_slots = tutor_availability.wed_avail
    elif day_of_week == "THURSDAY":
        available_slots = tutor_availability.thurs_avail
    elif day_of_week == "FRIDAY":
        available_slots = tutor_availability.fri_avail
    elif day_of_week == "SATURDAY":
        available_slots = tutor_availability.sat_avail
    elif day_of_week == "SUNDAY":
        available_slots = tutor_availability.sun_avail

    # Check if available_slots is a list of tuples (start_time, end_time)
    print("Available slots before filtering:", available_slots)  # Debugging line

    print("Available slots after filtering:", available_slots)  # Debugging line

    if not available_slots:
        return None  # No available slots found

    # Randomly choose an available slot
    new_start_time, new_end_time = get_random_time_slot(available_slots[0], available_slots[1])

    return new_start_time, new_end_time


# Function to update the session in the Schedule table after rescheduling
def reschedule_session(session_2, new_start_time, new_end_time):
    """Update session_2 with the new times in the database."""
    session_2.start_time = new_start_time
    session_2.end_time = new_end_time
    db.session.commit()
    print(f"Session {session_2.id} has been rescheduled to {new_start_time} - {new_end_time}")

# Function to check for conflicts and reschedule if necessary
def check_conflict():
    """Query the Schedule table, check for conflicts, and reschedule conflicting sessions."""
    # Query all sessions
    sessions = models.Schedule.query.all()

    # Group sessions by tutor to easily find conflicts
    tutor_sessions = {}
    for session in sessions:
        tutor_id = session.tutor_id
        if tutor_id not in tutor_sessions:
            tutor_sessions[tutor_id] = []
        tutor_sessions[tutor_id].append(session)

    # Check for conflicts within each tutor's schedule
    for tutor_id, tutor_sessions_list in tutor_sessions.items():
        # Sort sessions by date (if needed, depending on your format)
        tutor_sessions_list.sort(key=lambda x: x.date)

        # Check for conflicts
        for i in range(len(tutor_sessions_list)):
            session_1 = tutor_sessions_list[i]
            for j in range(i + 1, len(tutor_sessions_list)):
                session_2 = tutor_sessions_list[j]

                # If the sessions conflict (overlap), we need to reschedule session_2
                if session_1.date == session_2.date and time_conflict(session_1.start_time, session_1.end_time, session_2.start_time, session_2.end_time):
                    print(f"Conflict found between session {session_1.id} and session {session_2.id}")

                    # Find a new available slot for session_2
                    new_start_time, new_end_time = find_available_slot_for_reschedule(tutor_id, session_2.date, session_2.start_time, session_2.end_time)
                    
                    if new_start_time and new_end_time:
                        # Reschedule session_2 to the new time slot
                        reschedule_session(session_2, new_start_time, new_end_time)
                    else:
                        print(f"No available slots found to reschedule session {session_2.id}.")

    return {"SUCCESS": True}


def check_students():
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7
    next_monday = today + timedelta(days = days_until_monday)
    
    next_14_days = [next_monday + timedelta(days = i) for i in range(14)]
    scheduling_period = [date.strftime('%A, %Y-%m-%d') for date in next_14_days]
    print(scheduling_period)
    registered_students = models.LoginInformation.query.filter(models.LoginInformation.registration_complete == True, models.LoginInformation.account_type == models.AccountType.STUDENT).all()
    scheduled_students= [session.student_id for session in models.Schedule.query.all()]
    
    non_scheduled_students = [student for student in registered_students if student.id not in scheduled_students]
    non_scheduled_student_info = [models.StudentInformation.query.filter(models.StudentInformation.user_id == student.id).one() for student in non_scheduled_students]

    for student in non_scheduled_student_info:
        subjects = student.math + student.science + student.language + student.english + student.history
        subject = random.choice(subjects)

        print("Subject of choice: ", subject)
        tutors = models.TutorInformation.query.all()
        available_tutors = [tutor for tutor in tutors if subject in tutor.math + tutor.science + tutor.language + tutor.english + tutor.history]
        print("Available tutors: ", available_tutors)
        if available_tutors == []:
            continue
        tutor = random.choice(available_tutors)
    
        print("Chosen Tutor: ", tutor.to_dict())

        tutor_id = tutor.user_id
        sessions = models.Schedule.query.filter(models.Schedule.tutor_id == tutor_id).all()
        session_days = [calendar.day_name[int(session.day)].upper() for session in sessions]

        print("Weekdays with existing sessions: ", session_days)

        availability = models.Availability.query.filter(models.Availability.user_id == tutor_id).one_or_none()
        if availability is None:
            continue
        print("Availability: ", availability.to_dict())
        availability_list = [("MONDAY", availability.mon_avail), ("TUESDAY", availability.tue_avail), ("WEDNESDAY", availability.wed_avail), ("THURSDAY", availability.thurs_avail), ("FRIDAY", availability.fri_avail), ("SATURDAY", availability.sat_avail), ("SUNDAY", availability.sun_avail)]
        vacation = availability.vacation_days

        available_days= [available_day[0] for available_day in availability_list if available_day[1] != []]
        available_session_equal = True

        for day in available_days:
            if day not in session_days:
                available_session_equal = False

        if available_session_equal:
            print("\tAvailable Days: ", available_days)
            print("\tSession Days: ", session_days)
            continue

        new_session_day = random.choice(availability_list)
        while new_session_day[0] in session_days or new_session_day[1] == []:
            new_session_day = random.choice(availability_list)

        print("Chosen day for new session: ", new_session_day)

        potential_days = [date for date in scheduling_period if date.split(", ")[0].upper() == new_session_day[0]]
        print("Potential Session Days: ", potential_days)
        
        days_to_choose_from = [availability[0] for availability in availability_list if availability[1] != []]
        existing_session_weekdays = []
        [existing_session_weekdays.append(weekday) for weekday in session_days if weekday not in existing_session_weekdays]

        print("\tWeekdays we are choosing from: ", days_to_choose_from)
        print("\tWeekdays with a session already: ", existing_session_weekdays)
        if days_to_choose_from == existing_session_weekdays:
            continue

        if potential_days[0] in vacation and potential_days[1] in vacation:
            session_days.append(new_session_day[0])

            new_session_day = random.choice(availability_list)
            while new_session_day[0] in session_days:
                new_session_day = random.choice(availability_list)
        
        window_start = new_session_day[1][0]
        window_end = new_session_day[1][1]
        start_time, end_time = get_random_time_slot(window_start, window_end)

        date = random.choice(potential_days)
        print("New Session Day: ", date)

        while date.split(", ")[1] in vacation:
            date = random.choice(potential_days)
        session = models.Schedule(student.user_id, tutor_id, datetime.strptime(date.split(", ")[1], "%Y-%m-%d"), start_time, end_time, map_subject_to_string(subject))
        shift = models.Shifts.query.filter(models.Shifts.tutor_id == tutor_id, models.Shifts.start_day == scheduling_period[0].split(", ")[1]).one_or_none()

        if shift is None:
            shift = models.Shifts(tutor_id, scheduling_period[0].split(", ")[1], scheduling_period[-1].split(", ")[1])
            db.session.add(shift)
        else:
            shift.add_shift()

        
        db.session.add(session)
        db.session.commit()

        

    return {"SUCCESS": True}

def cancel_session(user_id, cancel_data):
    """
    This helper function will cancel a tutoring session
    {
        "DATE": "YYYY-MM-DD",
    }
    """

    date = datetime.strptime(cancel_data["DATE"], "%Y-%m-%d")

    login = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()

    account_type = login.account_type

    if account_type == models.AccountType.STUDENT: #This means a student is cancelling. We must find the tutor_id to get the correct session
        tutor_session = models.Schedule.query.filter(models.Schedule.student_id == user_id, models.Schedule.date == date).one_or_none()
    else:
        tutor_session = models.Schedule.query.filter(models.Schedule.tutor_id == user_id, models.Schedule.date == date).one_or_none()

    db.session.delete(tutor_session)
    db.session.commit()

    return {"SUCCESS": True}


from datetime import datetime, timedelta

def get_sessions(user_id):
    """
    This method gets all of the tutoring sessions that belong to a user
    """
    login_info = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()
    account_type = login_info.account_type
    
    if account_type == models.AccountType.STUDENT:
        all_sessions = models.Schedule.query.filter(models.Schedule.student_id == user_id).all()
    elif account_type == models.AccountType.TUTOR:
        all_sessions = models.Schedule.query.filter(models.Schedule.tutor_id == user_id).all()
    else:
        all_sessions = models.Schedule.query.all()

    # Ensure the date comparison only considers the date part (ignores the time)
    yesterday = (datetime.today() - timedelta(days=1)).date()

    # Filter sessions from the past 24 hours
    sessions = [session for session in all_sessions if session.date.date() >= yesterday]

    # Log sessions for debugging
    print(sessions)

    session_info = []

    for session in sessions:
        if session.date < datetime.now():
                continue
        if account_type == models.AccountType.STUDENT:

            tutor_login_info = models.LoginInformation.query.filter(models.LoginInformation.id == session.tutor_id).one_or_none()
            tutor_personal_info = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == session.tutor_id).one_or_none()

            email = tutor_login_info.email
            date = session.date.strftime("%Y-%m-%d")
            start_time = session.start_time
            end_time = session.end_time
            location = session.location
            subject = session.subject
            first_name = tutor_personal_info.first_name
            last_name = tutor_personal_info.last_name


            session_info.append({
                "EMAIL": email,
                "DATE": date,
                "START_TIME": start_time,
                "END_TIME": end_time,
                "LOCATION": location,
                "FULL_NAME": f"{first_name} {last_name}",
                "SUBJECT": subject
            })
        elif account_type == models.AccountType.TUTOR:
            student_login_info = models.LoginInformation.query.filter(models.LoginInformation.id == session.student_id).one_or_none()
            student_personal_info = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == session.student_id).one_or_none()

            email = student_login_info.email
            date = session.date.strftime("%Y-%m-%d")
            start_time = session.start_time
            end_time = session.end_time
            location = session.location
            subject = session.subject
            first_name = student_personal_info.first_name
            last_name = student_personal_info.last_name


            session_info.append({
                "EMAIL": email,
                "DATE": date,
                "START_TIME": start_time,
                "END_TIME": end_time,
                "LOCATION": location,
                "FULL_NAME": f"{first_name} {last_name}",
                "SUBJECT": subject
            })

    return session_info


    
def get_session_users(user_id):
    """
    This method gets all of the users that the current user has a session with in this session period
    """
    login_info = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()
    account_type = login_info.account_type
    
    if account_type == models.AccountType.STUDENT:
        all_sessions = models.Schedule.query.filter(models.Schedule.student_id == user_id).all()
    elif account_type == models.AccountType.TUTOR:
        all_sessions = models.Schedule.query.filter(models.Schedule.tutor_id == user_id).all()
    else:
        all_sessions = models.Schedule.query.all() # I guess we can keep this so admin can message people too

    # Log sessions for debugging
    print(all_sessions)

    session_users = []

    for session in all_sessions:
        if account_type == models.AccountType.STUDENT:
            tutor_login_info = models.LoginInformation.query.filter(models.LoginInformation.id == session.tutor_id).one_or_none()
            tutor_personal_info = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == session.tutor_id).one_or_none()

            fname = tutor_personal_info.first_name
            lname = tutor_personal_info.last_name
            username = tutor_login_info.username

            session_users.append({
                "FIRST_NAME": fname,
                "LAST_NAME": lname,
                "USERNAME": username
            })
        elif account_type == models.AccountType.TUTOR:
            student_login_info = models.LoginInformation.query.filter(models.LoginInformation.id == session.student_id).one_or_none()
            student_personal_info = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == session.student_id).one_or_none()

            fname = student_personal_info.first_name
            lname = student_personal_info.last_name
            username = student_login_info.username

            session_users.append({
                "FIRST_NAME": fname,
                "LAST_NAME": lname,
                "USERNAME": username
            })

    return session_users


def map_string_to_subject(string_subject):
    subject_map = {
        "ALGEBRA": ("MATH", models.Math.ALGEBRA),
        "CALCULUS": ("MATH", models.Math.CALCULUS),
        "GEOMETRY": ("MATH", models.Math.GEOMETRY),
        "TRIGONOMETRY": ("MATH", models.Math.TRIGONOMETRY),
        "STATISTICS": ("MATH", models.Math.STATISTICS),
        "PROBABILITY": ("MATH", models.Math.PROBABILITY),
        "DIFFERENTIAL EQUATIONS": ("MATH", models.Math.DIFFERENTIAL_EQUATIONS),
        "LINEAR ALGEBRA": ("MATH", models.Math.LINEAR_ALGEBRA),
        "GENERAL MATH": ("MATH", models.Math.GENERAL_MATH),

        "PHYSICS": ("SCIENCE", models.Science.PHYSICS),
        "CHEMISTRY": ("SCIENCE", models.Science.CHEMISTRY),
        "BIOLOGY": ("SCIENCE", models.Science.BIOLOGY),
        "EARTH SCIENCE": ("SCIENCE", models.Science.EARTH_SCIENCE),
        "ASTRONOMY": ("SCIENCE", models.Science.ASTRONOMY),
        "ENVIRONMENTAL SCIENCE": ("SCIENCE", models.Science.ENVIRONMENTAL_SCIENCE),
        "BOTANY": ("SCIENCE", models.Science.BOTANY),
        "ZOOLOGY": ("SCIENCE", models.Science.ZOOLOGY),
        "GENERAL SCIENCE": ("SCIENCE", models.Science.GENERAL_SCIENCE),

        "FRENCH": ("LANGUAGE", models.Language.FRENCH),
        "SPANISH": ("LANGUAGE", models.Language.SPANISH),
        "GERMAN": ("LANGUAGE", models.Language.GERMAN),
        "CHINESE": ("LANGUAGE", models.Language.CHINESE),
        "JAPANESE": ("LANGUAGE", models.Language.JAPANESE),
        "RUSSIAN": ("LANGUAGE", models.Language.RUSSIAN),
        "ITALIAN": ("LANGUAGE", models.Language.ITALIAN),
        "ARABIC": ("LANGUAGE", models.Language.ARABIC),

        "LITERATURE": ("ENGLISH", models.English.LITERATURE),
        "GRAMMAR": ("ENGLISH", models.English.GRAMMAR),
        "WRITING": ("ENGLISH", models.English.WRITING),
        "POETRY": ("ENGLISH", models.English.POETRY),
        "DRAMA": ("ENGLISH", models.English.DRAMA),
        "ESSAY WRITING": ("ENGLISH", models.English.ESSAY_WRITING),
        "CRITICAL ANALYSIS": ("ENGLISH", models.English.CRITICAL_ANALYSIS),
        "CREATIVE WRITING": ("ENGLISH", models.English.CREATIVE_WRITING),
        "GENERAL ENGLISH": ("ENGLISH", models.English.GENERAL_ENGLISH),

        "ANCIENT HISTORY": ("HISTORY", models.History.ANCIENT),
        "MEDIEVAL HISTORY": ("HISTORY", models.History.MEDIEVAL),
        "MODERN HISTORY": ("HISTORY", models.History.MODERN),
        "WORLD WAR I": ("HISTORY", models.History.WORLD_WAR_I),
        "WORLD WAR II": ("HISTORY", models.History.WORLD_WAR_II),
        "AMERICAN REVOLUTION": ("HISTORY", models.History.AMERICAN_REVOLUTION),
        "INDUSTRIAL REVOLUTION": ("HISTORY", models.History.INDUSTRIAL_REVOLUTION),
        "COLD WAR": ("HISTORY", models.History.COLD_WAR),
        "SOCIAL STUDIES": ("HISTORY", models.History.SOCIAL_STUDIES)
    }

    # Convert input string to uppercase
    string_subject_upper = string_subject.upper()

    # Look up subject and larger topic
    subject_info = subject_map.get(string_subject_upper)

    if subject_info is None:
        raise ValueError(f"Invalid subject string: {string_subject}")

    larger_topic, subject_enum = subject_info

    return larger_topic, subject_enum

def add_minutes_to_datetime(start_time_str, duration_hours):
    # Parse the start time string into a datetime object
    start_time = datetime.strptime(start_time_str, "%H:%M")
    
    # Convert the duration from hours to minutes
    duration_minutes = duration_hours * 60
    
    # Add the duration to the start time
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    # Return the end time in HH:mm format
    return end_time.strftime("%H:%M")

def book_a_session(user_id, session_info):
    """
    This method books a tutoring session manually
    {
        "START_TIME": <str>,
        "DURATION": <str>,
        "SUBJECT": <str>,
        "LOCATION": <str>,
        "DATE": <str>
    }
    """

    student_id = user_id
    start_time = session_info["START_TIME"]
    duration = session_info["DURATION"]

    string_subject = session_info["SUBJECT"]
    topic, subject = map_string_to_subject(session_info["SUBJECT"].upper())
    location = session_info["LOCATION"]
    date = session_info["DATE"]
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    end_time = add_minutes_to_datetime(start_time, float(duration))

    unavailable = {
        "SUCCESS": False,
        "MSG": "No available tutors"
    }

    print(subject)

    if topic == "MATH": 
        possible_tutors = models.TutorInformation.query.filter(models.TutorInformation.math.any(subject))
    elif topic == "SCIENCE":
        possible_tutors = models.TutorInformation.query.filter(models.TutorInformation.science != {}).all()
    elif topic == "HISTORY":
        possible_tutors = models.TutorInformation.query.filter(models.TutorInformation.history != {}).all()
    elif topic ==  "ENGLISH":
        possible_tutors = models.TutorInformation.query.filter(models.TutorInformation.english != {}).all()
    elif topic == "LANGUAGE":
        possible_tutors = models.TutorInformation.query.filter(models.TutorInformation.language != {}).all()

    
    if possible_tutors == []:
        print("No possible tutors")
        return unavailable
    
    available_tutors = []
    for tutor in possible_tutors:
        tutor_availability = models.Availability.query.filter(models.Availability.user_id == tutor.user_id).one_or_none()
        
        #Checking if the tutor even uploaded thier availability
        if tutor_availability is None:
            continue
        vacation = tutor_availability.vacation_days

        #Checking if the date chosen for a session is in the tutors vacation days
        if date in vacation:
            continue

        #Checking if the tutor already has a session on that day
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday = date_obj.strftime("%A").upper()
        
        tutor_sessions = models.Schedule.query.filter(models.Schedule.tutor_id == tutor.user_id).all()
        for session in tutor_sessions:
            if session.date == date_obj:
                print("Conflicting dates", date)
                return unavailable

        #Checking if the date chosen for a session is in the tutors availability
        if weekday == "MONDAY":
            time_slots = tutor_availability.mon_avail
        elif weekday == "TUESDAY":
            time_slots = tutor_availability.tue_avail
        elif weekday == "WEDNESDAY":
            time_slots = tutor_availability.wed_avail
        elif weekday == "THURSDAY":
            time_slots = tutor_availability.thurs_avail
        elif weekday == "FRIDAY":
            time_slots = tutor_availability.fri_avail
        elif weekday == "SATURDAY":
            time_slots = tutor_availability.sat_avail
        elif weekday == "SUNDAY":
            time_slots = tutor_availability.sun_avail
        
        if time_slots == []:
            continue


        tutor_start = time_slots[0]
        tutor_end = time_slots[1]

        #Checking if the start and end times align
        time_format = "%H:%M"
        tutor_start_obj = datetime.strptime(tutor_start, time_format)
        tutor_end_obj = datetime.strptime(tutor_end, time_format)

        student_start_obj = datetime.strptime(start_time, time_format)
        student_end_obj = datetime.strptime(end_time, time_format)

        #Creating a list of all possible tutors
        if tutor_start_obj > student_start_obj or tutor_end_obj < student_end_obj:
            continue
        else:
            available_tutors.append(tutor)

    if available_tutors == []:
        print("Weekday does not work")
        return unavailable, "No tutor ID"

    tutor = random.choice(available_tutors)

    booking = models.Schedule(student_id, tutor.user_id, date_obj, start_time, end_time, string_subject, location)
    db.session.add(booking)
    db.session.commit()

    return {
        "SUCCESS": True,
        "MSG": f"Session on {date} from {start_time} - {end_time} added"
    }, tutor.user_id
    












